"""
LLM-powered financial insights service.

Supports multiple LLM providers (priority order):
  1. Google Gemini (free tier — recommended)
  2. OpenAI GPT (paid)
  3. Smart rule-based fallback (no API key needed)

When GEMINI_API_KEY is set in .env, uses Gemini to generate
personalized financial advice. Falls back to mock insights on error.
"""

import json
import hashlib
from decimal import Decimal
from datetime import date, timedelta

from django.conf import settings

from finance.models import Transaction, Budget, Category
from finance.currency_utils import get_user_preferred_currency, convert_amount


def _gather_financial_context(user):
    """
    Gather the user's financial data for AI analysis.
    Returns a structured summary of income, expenses, budgets, and patterns.
    """
    preferred = get_user_preferred_currency(user)
    today = date.today()
    thirty_days_ago = today - timedelta(days=30)

    recent_txs = Transaction.objects.filter(
        user=user,
        date__gte=thirty_days_ago,
    ).select_related('category', 'currency').order_by('-date')

    income_total = Decimal('0.00')
    expense_total = Decimal('0.00')
    investment_total = Decimal('0.00')
    category_spending = {}

    for tx in recent_txs:
        converted = convert_amount(abs(tx.amount), tx.currency, preferred)
        if tx.type == 'INCOME':
            income_total += converted
        elif tx.type == 'EXPENSE':
            expense_total += converted
            cat_name = tx.category.name
            category_spending[cat_name] = category_spending.get(cat_name, Decimal('0.00')) + converted
        elif tx.type == 'INVESTMENT':
            investment_total += converted

    budgets = Budget.objects.filter(
        user=user,
        month__year=today.year,
        month__month=today.month,
    ).select_related('category')

    budget_info = []
    for b in budgets:
        budget_info.append({
            'category': b.category.name,
            'limit': float(b.limit_amount),
            'spent': float(b.spent),
            'percentage': float(b.percentage_used),
        })

    return {
        'currency_symbol': preferred.symbol,
        'currency_code': preferred.code,
        'income': float(income_total),
        'expenses': float(expense_total),
        'investments': float(investment_total),
        'savings': float(income_total - expense_total - investment_total),
        'savings_rate': round(float((income_total - expense_total - investment_total) / income_total * 100), 1) if income_total > 0 else 0,
        'top_categories': sorted(
            [{'name': k, 'total': float(v)} for k, v in category_spending.items()],
            key=lambda x: x['total'], reverse=True
        )[:5],
        'budgets': budget_info,
        'transaction_count': recent_txs.count(),
        'period': f'{thirty_days_ago.strftime("%b %d")} – {today.strftime("%b %d, %Y")}',
    }


def _generate_mock_insights(context):
    """
    Generate intelligent financial insights based on actual user data
    without using OpenAI API. Provides meaningful, data-driven advice.
    """
    insights = []
    sym = context['currency_symbol']

    # 1. Savings analysis
    rate = context['savings_rate'] if context['income'] > 0 else 0
    if rate >= 20:
        insights.append({
            'title': '🟢 Stellar Savings Rate',
            'body': f'You are saving {rate}% of your income this month, amounting to {sym}{context["savings"]:.2f}. This is excellent! A high savings rate provides a strong safety net and accelerates your long-term wealth building goals. Keep up this momentum.',
            'type': 'positive',
        })
    elif rate > 0:
        insights.append({
            'title': '🟡 Room for More Savings',
            'body': f'Your savings rate is currently {rate}% ({sym}{context["savings"]:.2f}). While you are in the positive, try to identify discretionary expenses to cut back on. Pushing your savings rate above 20% will significantly improve your financial resilience.',
            'type': 'warning',
        })
    else:
        insights.append({
            'title': '🔴 Deficit Spending Alert',
            'body': f'You are spending more than you earn this month, with a deficit of {sym}{abs(context["savings"]):.2f}. Review your recent transactions immediately to cut non-essential expenses and prevent long-term debt accumulation.',
            'type': 'danger',
        })

    # 2. Top spending category
    if context['top_categories'] and context['expenses'] > 0:
        top = context['top_categories'][0]
        pct = round(top['total'] / context['expenses'] * 100, 1)
        insights.append({
            'title': '🟠 High Spending Area',
            'body': f'"{top["name"]}" is your largest expense category, taking up {pct}% of your total spending ({sym}{top["total"]:.2f}). Consider setting a strict budget limit for this category next month to keep costs under control.',
            'type': 'warning' if pct > 40 else 'neutral',
        })

    # 3. Budget health
    if context['budgets']:
        worst_budget = max(context['budgets'], key=lambda b: b['percentage'])
        remaining = max(worst_budget['limit'] - worst_budget['spent'], 0)
        insights.append({
            'title': '🟡 Budget Utilization',
            'body': f'You have used {worst_budget["percentage"]}% of your "{worst_budget["category"]}" budget. You only have {sym}{remaining:.2f} remaining. Track your remaining purchases carefully to avoid an overrun before the month ends.',
            'type': 'danger' if worst_budget['percentage'] >= 100 else 'warning',
        })

    # 4. Investment check
    if context['investments'] > 0:
        inv_pct = round(context['investments'] / context['income'] * 100, 1) if context['income'] > 0 else 0
        insights.append({
            'title': '🟣 Investment Strategy',
            'body': f'You have invested {inv_pct}% of your income ({sym}{context["investments"]:.2f}) this month. Consistent investing is key to beating inflation and building wealth. Keep investing a fixed percentage of your income every month.',
            'type': 'positive' if inv_pct >= 15 else 'neutral',
        })

    return insights


def _generate_openai_insights(context):
    """
    Generate financial insights using OpenAI API.
    Falls back to mock insights on any error.
    """
    try:
        import openai
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

        prompt = _build_llm_prompt(context)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor. Return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1000,
        )

        content = response.choices[0].message.content.strip()
        # Strip markdown code fences if present
        if content.startswith('```'):
            content = content.split('\n', 1)[1].rsplit('```', 1)[0]
        return json.loads(content)

    except Exception:
        # Fallback to mock insights on any error
        return _generate_mock_insights(context)


def _build_llm_prompt(context):
    """Build the financial analysis prompt for any LLM."""
    return f"""You are a personal finance advisor. Analyze this financial data and provide
4 actionable insights. Be specific with numbers. Use full sentences and professional but encouraging language.

Financial Summary (last 30 days, {context['currency_code']}):
- Income: {context['currency_symbol']}{context['income']:.2f}
- Expenses: {context['currency_symbol']}{context['expenses']:.2f}
- Investments: {context['currency_symbol']}{context['investments']:.2f}
- Net Savings: {context['currency_symbol']}{context['savings']:.2f} ({context['savings_rate']}%)

Top Expense Categories:
{json.dumps(context['top_categories'], indent=2)}

Budget Status:
{json.dumps(context['budgets'], indent=2)}

Return ONLY a valid JSON array (no markdown, no code fences). Each object must have:
- "title": short insight title with one relevant emoji at the start
- "body": 2-3 sentence actionable financial advice, referencing specific numbers.
- "type": exactly one of "positive", "neutral", "warning", "danger"

Example format: [{{"title": "🎯 Great Savings", "body": "Your advice here.", "type": "positive"}}]"""


def _generate_gemini_insights(context):
    """
    Generate financial insights using Google Gemini API (free tier).
    Falls back to mock insights on any error.
    """
    try:
        import google.generativeai as genai

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')

        prompt = _build_llm_prompt(context)

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1000,
            ),
        )

        content = response.text.strip()
        # Strip markdown code fences if present
        if content.startswith('```'):
            content = content.split('\n', 1)[1].rsplit('```', 1)[0].strip()

        return json.loads(content)

    except Exception:
        return _generate_mock_insights(context)


def get_ai_insights(user):
    """
    Get AI-powered financial insights for a user.

    Priority: Gemini → OpenAI → Rule-based fallback.

    Returns:
        dict with:
            - insights: list of insight dicts (title, body, type)
            - context: financial summary data
            - ai_powered: bool indicating if real AI was used
            - provider: name of the LLM provider used
    """
    context = _gather_financial_context(user)

    from django.core.cache import cache
    context_hash = hashlib.md5(f"{context['transaction_count']}_{context['savings']}".encode()).hexdigest()
    cache_key = f"ai_insights_{user.id}_{context_hash}"
    
    cached_data = cache.get(cache_key)
    if cached_data:
        # Restore cached context (which might have minor time differences)
        cached_data['context'] = context
        return cached_data

    gemini_key = getattr(settings, 'GEMINI_API_KEY', None)
    openai_key = getattr(settings, 'OPENAI_API_KEY', None)

    if gemini_key:
        insights = _generate_gemini_insights(context)
        ai_powered = True
        provider = 'Google Gemini'
    elif openai_key:
        insights = _generate_openai_insights(context)
        ai_powered = True
        provider = 'OpenAI GPT'
    else:
        insights = _generate_mock_insights(context)
        ai_powered = False
        provider = 'Smart Analysis'

    result = {
        'insights': insights,
        'context': context,
        'ai_powered': ai_powered,
        'provider': provider,
    }
    
    # Cache for 24 hours (will auto-invalidate if context hash changes)
    cache.set(cache_key, result, timeout=86400)
    
    return result

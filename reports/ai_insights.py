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
    if context['income'] > 0:
        rate = context['savings_rate']
        if rate >= 30:
            insights.append({
                'title': '🎯 Excellent Savings Rate',
                'body': f'You\'re saving {rate}% of your income ({sym}{context["savings"]:.2f}). '
                        f'This is above the recommended 20% benchmark. Consider directing '
                        f'the surplus into investments or an emergency fund.',
                'type': 'positive',
            })
        elif rate >= 15:
            insights.append({
                'title': '👍 Good Savings Habit',
                'body': f'Your savings rate is {rate}% ({sym}{context["savings"]:.2f}). '
                        f'You\'re on track. Try to push toward 25-30% by reducing '
                        f'discretionary spending in your top expense categories.',
                'type': 'neutral',
            })
        elif rate > 0:
            insights.append({
                'title': '⚠️ Low Savings Rate',
                'body': f'You\'re only saving {rate}% of your income ({sym}{context["savings"]:.2f}). '
                        f'Financial experts recommend saving at least 20%. Review your '
                        f'top spending categories below for areas to cut back.',
                'type': 'warning',
            })
        else:
            insights.append({
                'title': '🚨 Spending Exceeds Income',
                'body': f'You\'re spending more than you earn — net position is '
                        f'{sym}{context["savings"]:.2f}. This is unsustainable. '
                        f'Prioritize essential expenses and pause discretionary spending.',
                'type': 'danger',
            })

    # 2. Top spending category
    if context['top_categories']:
        top = context['top_categories'][0]
        if context['expenses'] > 0:
            pct = round(top['total'] / context['expenses'] * 100, 1)
            insights.append({
                'title': f'📊 Top Expense: {top["name"]}',
                'body': f'"{top["name"]}" accounts for {pct}% of your expenses '
                        f'({sym}{top["total"]:.2f}). '
                        + (f'This is a large concentration — diversifying expenses '
                           f'or finding cheaper alternatives could save you significantly.'
                           if pct > 40 else
                           f'This seems well-balanced with your other spending.'),
                'type': 'warning' if pct > 40 else 'neutral',
            })

    # 3. Budget health
    overrun_budgets = [b for b in context['budgets'] if b['percentage'] > 100]
    warning_budgets = [b for b in context['budgets'] if 80 <= b['percentage'] <= 100]

    if overrun_budgets:
        names = ', '.join(b['category'] for b in overrun_budgets)
        insights.append({
            'title': '🔴 Budget Overruns Detected',
            'body': f'You\'ve exceeded your budget in: {names}. '
                    f'Consider revising your budget limits to be more realistic, '
                    f'or reduce spending in these categories next month.',
            'type': 'danger',
        })
    elif warning_budgets:
        names = ', '.join(b['category'] for b in warning_budgets)
        insights.append({
            'title': '🟡 Approaching Budget Limits',
            'body': f'You\'re close to your budget limit in: {names}. '
                    f'Monitor your spending carefully for the rest of the month.',
            'type': 'warning',
        })
    elif context['budgets']:
        insights.append({
            'title': '✅ All Budgets on Track',
            'body': 'Great job! All your budgets are within limits. '
                    'Keep maintaining this discipline.',
            'type': 'positive',
        })

    # 4. Investment check
    if context['investments'] > 0:
        inv_pct = round(context['investments'] / context['income'] * 100, 1) if context['income'] > 0 else 0
        insights.append({
            'title': '💼 Investment Activity',
            'body': f'You\'re investing {inv_pct}% of your income '
                    f'({sym}{context["investments"]:.2f}). '
                    + ('Consider increasing to 15-20% for long-term wealth building.'
                       if inv_pct < 15 else
                       'Excellent investment discipline!'),
            'type': 'positive' if inv_pct >= 15 else 'neutral',
        })
    elif context['income'] > 0:
        insights.append({
            'title': '💡 Start Investing',
            'body': 'You have no investment transactions this month. '
                    'Even small, regular investments grow significantly over time '
                    'thanks to compound returns.',
            'type': 'neutral',
        })

    # 5. Overall summary
    if context['transaction_count'] > 0:
        insights.append({
            'title': '📈 Monthly Overview',
            'body': f'In the last 30 days ({context["period"]}): '
                    f'Income {sym}{context["income"]:.2f} | '
                    f'Expenses {sym}{context["expenses"]:.2f} | '
                    f'Investments {sym}{context["investments"]:.2f} | '
                    f'Net {sym}{context["savings"]:.2f}.',
            'type': 'neutral',
        })
    else:
        insights.append({
            'title': '📝 No Recent Transactions',
            'body': 'No transactions found in the last 30 days. '
                    'Start logging your income and expenses to get personalized insights.',
            'type': 'neutral',
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

        prompt = f"""You are a personal finance advisor. Analyze this financial data and provide 
4-5 actionable insights. Be specific with numbers.

Financial Summary (last 30 days, {context['currency_code']}):
- Income: {context['currency_symbol']}{context['income']:.2f}
- Expenses: {context['currency_symbol']}{context['expenses']:.2f}  
- Investments: {context['currency_symbol']}{context['investments']:.2f}
- Savings: {context['currency_symbol']}{context['savings']:.2f} ({context['savings_rate']}%)

Top Expense Categories:
{json.dumps(context['top_categories'], indent=2)}

Budget Status:
{json.dumps(context['budgets'], indent=2)}

Return a JSON array where each object has:
- "title": short insight title with emoji
- "body": 2-3 sentence actionable advice
- "type": one of "positive", "neutral", "warning", "danger"
"""
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
4-5 actionable insights. Be specific with numbers. Keep each insight concise (2-3 sentences).

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
- "body": 2-3 sentence actionable financial advice
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

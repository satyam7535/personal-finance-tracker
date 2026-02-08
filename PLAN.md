# Personal Finance Tracker — Execution Plan
## Assignment: FJ-BE-R2 | Django + PostgreSQL + DTL

---

## PRE-BUILD: Architecture Decisions (LOCKED)

| Decision               | Choice                                          |
|------------------------|--------------------------------------------------|
| Framework              | Django + DRF + DTL                               |
| DB                     | PostgreSQL                                       |
| Precision              | DecimalField(max_digits=12, decimal_places=2)    |
| Transaction types      | INCOME / EXPENSE / INVESTMENT                    |
| Refunds                | Negative amount on expense                       |
| Category deletion      | PROTECT — block if transactions exist            |
| Currency               | Stored per transaction, converted in selectors   |
| Auth ownership         | Every model has user = FK(User)                  |
| Code structure         | Views → Services → ORM. Aggregations in Selectors|

### App Structure
```
finance_tracker/          ← Django project
├── core/                 ← Auth, profile, base templates
├── finance/              ← Models, services, transaction/category/budget CRUD
├── reports/              ← Selectors, dashboard, report views
├── templates/            ← All DTL templates
├── static/               ← CSS, Chart.js
├── media/                ← Receipt uploads
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## BLOCK 1 — DAY 1 (~10 hrs): All Core Part A

### Phase 1: Project Init (1 hr)
- [ ] django-admin startproject finance_tracker
- [ ] Create apps: core, finance, reports
- [ ] Settings: PostgreSQL, env vars via python-decouple, static/media config
- [ ] Base template (base.html) with nav
- [ ] requirements.txt
- [ ] .gitignore, .env.example
- **COMMIT:** `chore: initialize project structure and settings`
- **>>> PUSH TO GITHUB <<<**

### Phase 2: Auth + Profile (1.5 hrs)
- [ ] User registration (form + view + template)
- [ ] Login / Logout (Django auth views)
- [ ] UserProfile model: preferred_currency (default USD), FK to User (OneToOne)
- [ ] Profile edit view (change name, preferred currency)
- [ ] @login_required on all financial views
- [ ] Redirect unauthenticated → login
- **COMMIT:** `feat: user authentication and profile management`
- **>>> PUSH TO GITHUB <<<**

### Phase 3: Financial Models (1.5 hrs)
- [ ] Currency model: code, name, symbol, exchange_rate_to_usd
- [ ] Category model: user, name, type (INCOME/EXPENSE/INVESTMENT), created_at
- [ ] Transaction model: user, category, amount (Decimal), currency (FK), date, description, receipt (FileField nullable), created_at, updated_at
- [ ] Budget model: user, category (expense only), limit_amount (Decimal), month (DateField), created_at
- [ ] Validations in clean()
- [ ] Indexes on: (user, date), (user, category)
- [ ] Category deletion: on_delete=PROTECT on Transaction FK
- [ ] Seed currencies management command: USD, EUR, GBP, INR, JPY
- [ ] Makemigrations + migrate
- **COMMIT:** `feat: financial data models with validations and constraints`
- **>>> PUSH TO GITHUB <<<**

### Phase 4: Transaction CRUD + Service Layer (2 hrs)
- [ ] finance/services.py:
  - create_transaction(user, data)
  - update_transaction(user, tx_id, data)
  - delete_transaction(user, tx_id)
- [ ] Views: list (with filters), create, edit, delete
- [ ] Templates: transaction list, form, delete confirm
- [ ] Edge cases:
  - Negative amount allowed (refund)
  - Unauthorized access → 403
  - Invalid category for type → form error
  - Decimal precision enforced
- **COMMIT:** `feat: transaction CRUD with service layer and edge case handling`
- **>>> PUSH TO GITHUB <<<**

### Phase 5: Category + Budget CRUD (1 hr)
- [ ] Category: list, create, delete (block if transactions exist)
- [ ] Budget: create/edit per expense category per month
- [ ] Budget progress: SUM(transactions) vs limit_amount, show % used
- **COMMIT:** `feat: category management and budget goals with progress tracking`
- **>>> PUSH TO GITHUB <<<**

### Phase 6: Multi-Currency Support (1 hr)
- [ ] Currency selector on transaction form
- [ ] convert_amount(amount, from_currency, to_currency)
- [ ] All selectors accept target_currency param
- [ ] Reports show amounts in user's preferred currency
- **COMMIT:** `feat: multi-currency transaction support with conversion`
- **>>> PUSH TO GITHUB <<<**

### Phase 7: Aggregation Selectors (1 hr)
- [ ] reports/selectors.py:
  - get_total_income(user, month, currency)
  - get_total_expense(user, month, currency)
  - get_total_investment(user, month, currency)
  - get_savings(user, month, currency)
  - get_category_breakdown(user, type, month)
  - get_monthly_report(user, year)
  - get_insights(user) — savings rate, top category, trend
- [ ] All use annotate()/aggregate() — no Python loops
- **COMMIT:** `feat: optimized aggregation and query layer`
- **>>> PUSH TO GITHUB <<<**

### Phase 8: Dashboard + Reports (1 hr)
- [ ] Dashboard view:
  - Totals: income / expense / investment / savings
  - Insights: savings rate %, top expense category, trend
  - Charts: income vs expense bar, category pie, savings line
- [ ] Reports view:
  - Monthly income vs expense table + chart
  - Date range filter
  - Currency selector
- **COMMIT:** `feat: financial dashboard with charts and monthly reports`
- **>>> PUSH TO GITHUB <<<**

---

## BLOCK 2 — DAY 2 (~8-10 hrs): Day 3 Features + Deployment

### Phase 9: Google OAuth (2 hrs)
- [ ] Install django-allauth
- [ ] Configure Google OAuth provider
- [ ] Login page: "Sign in with Google" + normal login
- [ ] Link Google account to existing profile
- **COMMIT:** `feat: Google OAuth authentication via django-allauth`
- **>>> PUSH TO GITHUB <<<**

### Phase 10: Receipt Upload (1 hr)
- [ ] Upload in transaction form (image/PDF)
- [ ] View/download receipt from transaction detail
- [ ] Media storage config
- **COMMIT:** `feat: receipt upload and storage for transactions`
- **>>> PUSH TO GITHUB <<<**

### Phase 11: Budget Overrun Notifications (2 hrs)
- [ ] Notification model: user, message, type, is_read, created_at, budget FK
- [ ] Detection: after expense transaction, check budget exceeded
- [ ] In-app notification list (unread count in nav)
- [ ] Email via Sendgrid/SMTP (one per breach, track last_notified)
- **COMMIT:** `feat: budget overrun detection with email notifications`
- **>>> PUSH TO GITHUB <<<**

### Phase 12: Deployment (2-3 hrs)
- [ ] Platform: Render (free PostgreSQL addon)
- [ ] Production settings:
  - DEBUG=False, ALLOWED_HOSTS, SECRET_KEY from env
  - SECURE_SSL_REDIRECT, CSRF_COOKIE_SECURE, SESSION_COOKIE_SECURE
  - SECURE_HSTS_SECONDS
- [ ] Static: WhiteNoise
- [ ] Media: production config
- [ ] Procfile / render.yaml
- [ ] End-to-end test on deployed URL
- **COMMIT:** `chore: production deployment with security hardening`
- **>>> PUSH TO GITHUB <<<**

### Phase 13: Part B — Pick ONE (1-2 hrs, if time)
- [ ] Option A: Anomaly Detection — mean + std_dev per category, flag > 2 std deviations
- [ ] Option B: OpenAI Integration — spending summary → GPT → financial advice
- **COMMIT:** `feat: spending anomaly detection` OR `feat: AI-powered financial insights`
- **>>> PUSH TO GITHUB <<<**

---

## BLOCK 3 — DAY 3 morning (~5-6 hrs): Testing + Docs + Submit

### Phase 14: Testing (3 hrs)
- [ ] Model tests: validation, decimal, PROTECT
- [ ] Service tests: CRUD, ownership, refund
- [ ] Selector tests: totals, conversion, monthly report
- [ ] Integration tests: auth flow, transaction lifecycle, budget notification
- [ ] Edge case tests: unauthorized, category deletion, zero amount
- **COMMIT:** `test: comprehensive test coverage`
- **>>> PUSH TO GITHUB <<<**

### Phase 15: Documentation (1.5 hrs)
- [ ] README.md:
  - Project overview, architecture diagram
  - Model relationships
  - Setup instructions (local + prod)
  - Environment variables list
  - Edge cases handled
  - Tradeoffs made
  - Features completed checklist
- **COMMIT:** `docs: comprehensive README with architecture and setup guide`
- **>>> PUSH TO GITHUB <<<**

### Phase 16: Final Polish + Submit (1 hr)
- [ ] Custom 404/500 pages
- [ ] Form validation messages
- [ ] Production smoke test
- [ ] Record Loom video (~15-20 min)
- [ ] Fill submission Google Form
- [ ] Verify repo shared with @mahim37
- **COMMIT:** `chore: final polish and submission prep`
- **>>> PUSH TO GITHUB <<<**

---

## COMPLETE CHECKLIST vs ASSIGNMENT

| #  | Requirement                          | Phase |
|----|--------------------------------------|-------|
| 1  | User register/login/logout           | 2     |
| 2  | Manage profiles                      | 2     |
| 3  | Income tracking                      | 3,4   |
| 4  | Expense tracking                     | 3,4   |
| 5  | Investment tracking                  | 3,4   |
| 6  | Transaction: date, amount, desc      | 3     |
| 7  | Add/edit/delete transactions         | 4     |
| 8  | Negative amounts / refunds           | 4     |
| 9  | Category deletion with transactions  | 5     |
| 10 | Decimal precision                    | 3,4   |
| 11 | Dashboard with graphs                | 8     |
| 12 | Monthly income vs expense report     | 8     |
| 13 | Budget goals + progress              | 5     |
| 14 | Google OAuth                         | 9     |
| 15 | Email notifications (budget overrun) | 11    |
| 16 | Receipt upload                       | 10    |
| 17 | Multi-currency in transactions       | 6     |
| 18 | Multi-currency in reports            | 6,7   |
| 19 | Deployment (secure + optimized)      | 12    |
| 20 | Testing                              | 14    |
| 21 | Part B (at least 1)                  | 13    |
| 22 | Loom video                           | 16    |
| 23 | README / docs                        | 15    |
| 24 | Regular Git commits                  | All   |

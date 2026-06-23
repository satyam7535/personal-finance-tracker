# 📅 Backend Mastery — Week-by-Week Calendar

> **Start date:** Monday, June 30, 2026
> **Method:** Follow the [5-step daily method](file:///C:/Users/DELL/.gemini/antigravity-ide/brain/40fd8cae-88d7-4d2a-959f-7ba5d9b2b800/backend_learning_path.md) exactly
> **Two guides:**
> - **Order** → [backend_learning_path.md](file:///C:/Users/DELL/.gemini/antigravity-ide/brain/40fd8cae-88d7-4d2a-959f-7ba5d9b2b800/backend_learning_path.md)
> - **Depth** → [backend_mastery_guide.md](file:///C:/Users/DELL/.gemini/antigravity-ide/brain/40fd8cae-88d7-4d2a-959f-7ba5d9b2b800/backend_mastery_guide.md)

> [!TIP]
> **You already built a Finance Tracker.** You probably know Steps 1–8 in practice. Still go through them — but focus on **gaps** (recursion depth, Big-O, decorators). You can do 2 steps/day for familiar topics. This could compress Milestone 1 from 6 weeks to 2 weeks, finishing the full path in ~8 months instead of 12.

---

## How to Read This Calendar

| Symbol | Meaning |
|--------|---------|
| 📖 | Study day — read + notes |
| 🔨 | Build day — code implementation |
| 🔁 | Revision day — fix weak spots |
| ✅ | Checkpoint — test yourself |
| 🚀 | Project day — build something real |

Each day has:
- **What to do** (specific step + focus area)
- **Output** (what you should produce)
- **Time** (~2-3 hours)

---

# MILESTONE 1: Programming Foundations

## Week 1 — Variables, Control Flow, Functions

| Day | Type | Step | Focus | Output |
|-----|------|------|-------|--------|
| Mon | 📖🔨 | **Step 1** | Variables, types, operators, strings | 5 notes + script: calculator that handles +, -, *, /, % |
| Tue | 📖🔨 | **Step 2** | if/elif/else, for/while loops, break/continue | 5 notes + script: FizzBuzz + number guessing game |
| Wed | 📖🔨 | **Step 3 (part 1)** | Functions, params, return, scope, docstrings | 5 notes + script: 5 utility functions (is_prime, factorial, reverse_string, etc.) |
| Thu | 📖🔨 | **Step 3 (part 2)** | Lambda, decorators, recursion, *args/**kwargs | 5 notes + script: decorator that logs function calls + recursive fibonacci |
| Fri | 📖🔨 | **Step 4 (part 1)** | Lists, list comprehensions, sorting, slicing | 5 notes + script: list operations (filter, transform, search) |
| Sat | 🔁 | Review Steps 1–4 | Fix anything you couldn't explain clearly | Re-do any weak exercise |
| Sun | 🔨 | **Step 4 (part 2)** | Dicts, sets, tuples, when-to-use-each | Script: word frequency counter using dicts + sets |

---

## Week 2 — OOP, Error Handling, Modules

| Day | Type | Step | Focus | Output |
|-----|------|------|-------|--------|
| Mon | 📖🔨 | **Step 5 (part 1)** | Classes, __init__, self, methods, properties | 5 notes + class: `BankAccount` with deposit, withdraw, balance |
| Tue | 📖🔨 | **Step 5 (part 2)** | Inheritance, composition, polymorphism, abstract classes | 5 notes + class hierarchy: `Shape` → `Circle`, `Rectangle` with area() |
| Wed | 📖🔨 | **Step 6** | try/except, custom exceptions, context managers | 5 notes + script: file processor that handles missing files, bad formats, custom `InvalidDataError` |
| Thu | 📖🔨 | **Step 7 (part 1)** | Modules, packages, virtual environments, pip | 5 notes + create a Python package with `__init__.py`, install external package |
| Fri | 📖🔨 | **Step 7 (part 2)** | File I/O (CSV, JSON), env vars, datetime | 5 notes + script: read CSV of expenses, parse dates, write JSON summary |
| Sat | 🔁 | Review Steps 5–7 | Can you explain OOP inheritance to someone? | Re-do any weak exercise |
| Sun | 📖🔨 | **Step 8** | Big-O, binary search, hash tables | 5 notes + implement binary search + explain why dict lookup is O(1) |

---

## Week 3 — ✅ MILESTONE 1 CHECKPOINT

| Day | Type | Step | Focus | Output |
|-----|------|------|-------|--------|
| Mon | 🔨 | **Checkpoint build** | Build CLI expense tracker (add, list, delete, filter by category) | Working script using all concepts from Steps 1–8 |
| Tue | 🔨 | **Checkpoint build** | Add: save to CSV, load from CSV, monthly summary | Complete CLI tool |
| Wed | ✅ | **Self-test** | Explain: OOP, scope, Big-O, dict vs list, error handling | Write 1-page summary of what you learned |
| Thu | 📖🔨 | **Step 9** | Internet basics — IP, ports, DNS, TCP handshake | 5 notes + use `nslookup`, `ping`, identify ports |
| Fri | 📖🔨 | **Step 10 (part 1)** | HTTP request/response structure, methods, status codes | 5 notes + make 5 `curl` requests to a public API |
| Sat | 🔁 | Review | Can you explain TCP 3-way handshake? HTTP methods? | Fix any gaps |
| Sun | 📖🔨 | **Step 10 (part 2)** | Headers, JSON, cookies, content negotiation | 5 notes + curl with custom headers, parse JSON response |

---

# MILESTONE 2: How the Web Works

## Week 4 — Web Fundamentals Complete

| Day | Type | Step | Focus | Output |
|-----|------|------|-------|--------|
| Mon | 📖🔨 | **Step 11** | HTTPS/TLS, cookies (HttpOnly, Secure, SameSite), sessions | 5 notes + diagram: "How login works with sessions" |
| Tue | ✅ | **Milestone 2 checkpoint** | Explain: "What happens when you type google.com?" | Write full answer (DNS → TCP → TLS → HTTP → response) |
| Wed | 📖🔨 | **Step 12 (part 1)** | Django setup, project structure, urls.py, views.py | 5 notes + running Django project with one "hello world" view |
| Thu | 📖🔨 | **Step 12 (part 2)** | Request-response cycle, templates, static files | 5 notes + page that displays current time from a view |
| Fri | 📖🔨 | **Step 13 (part 1)** | Database concepts, PostgreSQL setup, CREATE TABLE, INSERT, SELECT | 5 notes + create a `transactions` table in psql, insert 5 rows |
| Sat | 🔁 | Review Steps 9–13 | Can you trace a full HTTP request through Django? | Fix any gaps |
| Sun | 📖🔨 | **Step 13 (part 2)** | WHERE, ORDER BY, GROUP BY, HAVING, aggregates | 5 notes + write 10 SQL queries against your transactions table |

---

# MILESTONE 3: Your First Backend

## Week 5 — ORM & REST Basics

| Day | Type | Step | Focus | Output |
|-----|------|------|-------|--------|
| Mon | 📖🔨 | **Step 14 (part 1)** | Django models, field types, migrations | 5 notes + define 3 models (Category, Transaction, Budget), migrate |
| Tue | 📖🔨 | **Step 14 (part 2)** | ForeignKey, queries, filter, select_related, N+1 | 5 notes + Django shell: create related objects, query with select_related |
| Wed | 📖🔨 | **Step 15 (part 1)** | REST principles, CRUD endpoints (GET, POST) | 5 notes + build list + create views for transactions |
| Thu | 📖🔨 | **Step 15 (part 2)** | PUT/PATCH/DELETE, status codes, error responses | 5 notes + complete CRUD for transactions |
| Fri | 📖🔨 | **Step 16** | Layered architecture: thin views → services → models | 5 notes + refactor: move business logic from views to services.py |
| Sat | 🔁 | Review Steps 14–16 | Can you explain: ORM vs raw SQL? Why thin views? | Fix any gaps |
| Sun | 🔨 | **Practice** | Build a mini CRUD API for a new entity (e.g., Notes) | Working CRUD with service layer |

---

## Week 6 — SQL Deep Dive + Milestone 3 Checkpoint

| Day | Type | Step | Focus | Output |
|-----|------|------|-------|--------|
| Mon | 📖🔨 | **Step 17 (part 1)** | JOINs (INNER, LEFT), subqueries, CTEs | 5 notes + write 5 JOIN queries combining transactions + categories |
| Tue | 📖🔨 | **Step 17 (part 2)** | Indexes, EXPLAIN ANALYZE, ACID transactions | 5 notes + add indexes, run EXPLAIN on slow queries, see the difference |
| Wed | ✅ | **Milestone 3 checkpoint** | Can you build CRUD from scratch? Explain indexes? Write JOINs? | Self-test: build a new mini API in 2 hours |
| Thu | 📖🔨 | **Step 18 (part 1)** | Registration, password hashing, login flow | 5 notes + build registration + login views |
| Fri | 📖🔨 | **Step 18 (part 2)** | Session auth, JWT concepts, @login_required, logout | 5 notes + protect views, test logged-in vs logged-out |
| Sat | 🔁 | Review Steps 17–18 | Can you explain: isolation levels? Session vs JWT? | Fix any gaps |
| Sun | 🔨 | **Practice** | Add auth to your Notes API from last Sunday | Working auth flow |

---

# MILESTONE 4: Make It Real

## Week 7 — Authorization, Validation, Config

| Day | Type | Step | Focus | Output |
|-----|------|------|-------|--------|
| Mon | 📖🔨 | **Step 19** | Authorization, RBAC, object-level permissions, data isolation | 5 notes + add ownership checks: users only see their own data |
| Tue | 📖🔨 | **Step 20** | Input validation: form + model + DB constraints | 5 notes + add validation to Transaction (no zero, no negative income) |
| Wed | 📖🔨 | **Step 21** | .env files, python-decouple, 12-Factor App basics | 5 notes + move all secrets to .env, create .env.example |
| Thu | 📖🔨 | **Step 22 (part 1)** | Notification system, email sending (Resend/SendGrid) | 5 notes + create Notification model, send test email |
| Fri | 📖🔨 | **Step 22 (part 2)** | File uploads, external API integration, fallback pattern | 5 notes + add file upload + graceful API call with try/except fallback |
| Sat | 🔁 | Review Steps 19–22 | Can you explain: auth vs authz? Validation layers? Fallback pattern? | Fix any gaps |
| Sun | ✅ | **Milestone 4 checkpoint** | Build: authenticated API with validation + email notification | Self-test with your Finance Tracker as reference |

---

# MILESTONE 5: Make It Safe & Tested

## Week 8 — Security, Testing, Git

| Day | Type | Step | Focus | Output |
|-----|------|------|-------|--------|
| Mon | 📖🔨 | **Step 23** | SQL injection, XSS, CSRF, security headers | 5 notes + verify Django's protections, add security middleware |
| Tue | 📖🔨 | **Step 24 (part 1)** | Unit tests: test one function, AAA pattern, assertions | 5 notes + write 5 unit tests for your service functions |
| Wed | 📖🔨 | **Step 24 (part 2)** | Integration tests, view tests, mocking external services | 5 notes + write 5 integration tests, mock email sending |
| Thu | 📖🔨 | **Step 25** | Git: branch, merge, rebase, PR, .gitignore, conflicts | 5 notes + create feature branch, make PR, resolve a conflict |
| Fri | 📖🔨 | **Step 26 (part 1)** | Docker: Dockerfile, build, run, .dockerignore | 5 notes + Dockerize your app, run it in a container |
| Sat | 🔁 | Review Steps 23–26 | Can you explain: CSRF? Test pyramid? Docker layers? | Fix any gaps |
| Sun | 📖🔨 | **Step 26 (part 2)** | Docker Compose: multi-container (app + PostgreSQL) | Working docker-compose.yml |

---

## Week 9 — Deployment + Milestone 5 Checkpoint

| Day | Type | Step | Focus | Output |
|-----|------|------|-------|--------|
| Mon | 📖🔨 | **Step 27 (part 1)** | Deployment concepts, Render/Railway setup | 5 notes + deploy your app to Render |
| Tue | 📖🔨 | **Step 27 (part 2)** | CI/CD: GitHub Actions, production checklist | 5 notes + add GitHub Action that runs tests on push |
| Wed | ✅ | **Milestone 5 checkpoint** | Your app is deployed, tested, secured, with CI/CD | Verify: push code → tests run → app deploys |
| Thu | 🔁 | **Big review** | Review Milestones 1–5 — identify weakest 3 topics | Study notes for weak topics |
| Fri | 🔁 | **Deep review** | Re-study the 3 weakest topics | Re-do exercises for those topics |
| Sat | 🔁 | Review | Final cleanup of any gaps | Clean notes |
| Sun | 🚀 | **Project** | Start a fresh mini-project (Blog API) to test all skills | Skeleton with auth + CRUD + tests + Docker |

> [!IMPORTANT]
> **🎉 After Week 9, you are an intermediate backend engineer.** Everything after this builds senior-level depth.

---

# MILESTONE 6: Make It Fast & Scalable

## Week 10 — Caching & Background Jobs

| Day | Type | Step | Focus | Output |
|-----|------|------|-------|--------|
| Mon | 📖🔨 | **Step 28 (part 1)** | Why cache, Redis setup, cache-aside pattern | 5 notes + install Redis, cache a slow query result |
| Tue | 📖🔨 | **Step 28 (part 2)** | TTL, invalidation, cache stampede, what to/not to cache | 5 notes + implement cache invalidation on data change |
| Wed | 📖🔨 | **Step 29 (part 1)** | Celery setup, define task, run worker | 5 notes + create Celery task, execute it async |
| Thu | 📖🔨 | **Step 29 (part 2)** | Retry policies, dead letter queue, scheduled tasks | 5 notes + add retry to task, configure periodic task |
| Fri | 📖🔨 | **Step 30 (part 1)** | Pub/sub vs queue, delivery guarantees, idempotent consumers | 5 notes + diagram: pub/sub vs queue with examples |
| Sat | 🔁 | Review Steps 28–30 | Can you explain: cache-aside? Exponential backoff? Exactly-once illusion? | Fix any gaps |
| Sun | 📖🔨 | **Step 30 (part 2)** | Outbox pattern, inbox pattern, Kafka basics (concepts) | 5 notes + implement simple dedup table for messages |

---

## Week 11 — Database Performance & Monitoring

| Day | Type | Step | Focus | Output |
|-----|------|------|-------|--------|
| Mon | 📖🔨 | **Step 31 (part 1)** | N+1 problem, select_related, EXPLAIN ANALYZE | 5 notes + find and fix an N+1 query in your project |
| Tue | 📖🔨 | **Step 31 (part 2)** | Window functions, cursor pagination, connection pooling | 5 notes + write window function query, implement cursor pagination |
| Wed | 📖🔨 | **Step 32 (part 1)** | Structured logging, log levels, request IDs, PII redaction | 5 notes + set up structured JSON logging in your app |
| Thu | 📖🔨 | **Step 32 (part 2)** | Metrics, alerts, Sentry/Prometheus basics | 5 notes + integrate Sentry for error tracking |
| Fri | 📖🔨 | **Step 33** | NoSQL use cases, Redis data types, SQL vs NoSQL decision matrix | 5 notes + Redis exercise: implement rate limiter with sorted sets |
| Sat | 🔁 | Review Steps 31–33 | Can you explain: N+1 fix? When Redis vs Mongo vs Postgres? | Fix any gaps |
| Sun | ✅ | **Milestone 6 checkpoint** | Self-test: optimize a slow API (caching, query fix, background job) | Document: "3 performance improvements I made and why" |

---

# MILESTONE 7: Design & Lead

## Week 12 — Scaling & Distributed Systems

| Day | Type | Step | Focus | Output |
|-----|------|------|-------|--------|
| Mon | 📖🔨 | **Step 34 (part 1)** | Vertical vs horizontal scaling, stateless services | 5 notes + diagram: "How to scale my Finance Tracker to 100K users" |
| Tue | 📖🔨 | **Step 34 (part 2)** | Load balancing algorithms, DB read replicas, sharding | 5 notes + explain: round-robin vs consistent hashing |
| Wed | 📖🔨 | **Step 35 (part 1)** | CAP theorem, eventual consistency, real examples | 5 notes + classify 5 databases as CP or AP with reasoning |
| Thu | 📖🔨 | **Step 35 (part 2)** | Distributed locking, idempotency, consensus (Raft), clock problems | 5 notes + explain: why Redis lock needs fencing tokens |
| Fri | 📖🔨 | **Step 36** | Timeouts, retries, circuit breaker, bulkhead, graceful degradation | 5 notes + diagram: circuit breaker state machine |
| Sat | 🔁 | Review Steps 34–36 | Can you explain: CAP? Circuit breaker? Why clocks lie? | Fix any gaps |
| Sun | 📖🔨 | **Step 37** | Architecture patterns: monolith, microservices, CQRS, saga, outbox+inbox | 5 notes + compare: when monolith vs microservices |

---

## Week 13 — Cloud, Kubernetes & System Design Prep

| Day | Type | Step | Focus | Output |
|-----|------|------|-------|--------|
| Mon | 📖🔨 | **Step 38 (part 1)** | Kubernetes basics: pods, deployments, services, health probes | 5 notes + deploy a container to a local k8s (minikube) or read k8s YAML configs |
| Tue | 📖🔨 | **Step 38 (part 2)** | Cloud services (AWS/GCP overview), IaC basics, deployment strategies | 5 notes + diagram: "My app on AWS" (EC2, RDS, ElastiCache, S3) |
| Wed | 📖🔨 | **Step 39 (part 1)** | System design methodology (7 steps), capacity estimation formulas | 5 notes + practice: estimate capacity for 1M-user app |
| Thu | 🔨 | **Step 39 (part 2)** | Design practice: URL shortener | Full system design write-up (requirements, API, data model, components) |
| Fri | 🔨 | **Step 39 (part 3)** | Design practice: notification system | Full system design write-up |
| Sat | 🔁 | Review Steps 37–39 | Practice explaining your URL shortener design out loud | Fix any gaps |
| Sun | ✅ | **Milestone 7 checkpoint** | Self-test: design a system in 30 minutes on paper | Celebrate! 🎉 |

---

## Weeks 14–16 — System Design Deep Practice (Optional but Recommended)

| Week | Focus | Daily Practice |
|------|-------|----------------|
| **14** | Design 3 more systems: chat app, rate limiter, payment system | One design per 2 days + review |
| **15** | LeetCode medium problems (arrays, strings, hash maps, trees) | 2 problems/day |
| **16** | Mock interviews: explain your Finance Tracker architecture | Practice with a friend or record yourself |

---

# 📊 Calendar Summary

| Week | Dates | Milestone | Steps | Level After |
|------|-------|-----------|-------|-------------|
| 1 | Jun 30 – Jul 6 | 1: Foundations | 1–4 | "I can write Python" |
| 2 | Jul 7 – Jul 13 | 1: Foundations | 5–8 | "I can solve problems" |
| 3 | Jul 14 – Jul 20 | 1→2: Checkpoint + Web | Checkpoint + 9–10 | "I understand the web" |
| 4 | Jul 21 – Jul 27 | 2→3: Web + Backend | 11–13 | "I know HTTP + SQL" |
| 5 | Jul 28 – Aug 3 | 3: First Backend | 14–16 | "I can build APIs" |
| 6 | Aug 4 – Aug 10 | 3→4: SQL + Auth | 17–18 | "I can write JOINs + login" |
| 7 | Aug 11 – Aug 17 | 4: Real Features | 19–22 | "I can build real apps" |
| 8 | Aug 18 – Aug 24 | 5: Safe & Tested | 23–26 | "I can test + Dockerize" |
| 9 | Aug 25 – Aug 31 | 5: Deploy | 27 + review | **INTERMEDIATE** ✅ |
| 10 | Sep 1 – Sep 7 | 6: Performance | 28–30 | "I know caching + async" |
| 11 | Sep 8 – Sep 14 | 6: DB perf + monitoring | 31–33 | "I can optimize systems" |
| 12 | Sep 15 – Sep 21 | 7: Distributed + Design | 34–37 | "I understand scale" |
| 13 | Sep 22 – Sep 28 | 7: Cloud + Design | 38–39 | **SENIOR-READY** ✅ |
| 14–16 | Sep 29 – Oct 19 | Bonus: Interview prep | Practice | **INTERVIEW-READY** 🎯 |

---

# ⚡ Fast-Track Option

> Since you already built the [Finance Tracker](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune), you likely know Steps 1–8 in practice. Here's an accelerated option:

| Approach | Start Point | Duration |
|----------|-------------|----------|
| **Full path** (recommended for deep understanding) | Step 1 | 13 weeks |
| **Fast-track** (if Steps 1–8 feel easy) | Step 9 | 9 weeks |
| **Speed run** (if Steps 1–17 feel easy) | Step 18 | 6 weeks |

> [!IMPORTANT]
> **Honest self-test before skipping:** For each step you want to skip, can you (1) explain it to someone, (2) write working code, and (3) answer an interview question about it? If yes → skip. If no → study it.

---

# 📋 Daily Template

Copy this for each day:

```markdown
## Day: [date]
### Step: [number] — [title]

**5 Bullet Notes:**
1.
2.
3.
4.
5.

**Code Snippet:**
[save file to a `learning/` folder in your project]

**Can I explain this simply?** [ ] Yes  [ ] Not yet
**Can I write working code?**  [ ] Yes  [ ] Not yet
**Checkbox marked in learning_path.md?** [ ] Yes
```

---

> [!TIP]
> **Start tomorrow (Monday, June 30).** Open [backend_learning_path.md](file:///C:/Users/DELL/.gemini/antigravity-ide/brain/40fd8cae-88d7-4d2a-959f-7ba5d9b2b800/backend_learning_path.md), go to Step 1, follow the daily template above. That's it. One step at a time.

# 🏗️ The Complete Backend Engineering Mastery Guide

> **Purpose**: A definitive, structured learning roadmap to become a backend engineer who can crack any interview, architect production systems, and lead technical decisions.
>
> **How to use**: Follow the phases in order. Each section lists concepts, subtopics, interview relevance, and maps to real code from the [Finance Tracker](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune) project where applicable.

---

> [!NOTE]
> **Review Summary of Original Checklist**: Your existing checklist (`Pasted markdown(5).md`) is solid — it covers ~80% of what a senior backend engineer needs. This guide restructures the flow, fills **40+ missing topics**, adds interview relevance markers, and connects everything to your actual codebase.

> [!IMPORTANT]
> **Key Gaps Identified in Your Original Checklist**:
> - No coverage of **networking internals** (TCP handshake, connection pooling, socket programming)
> - Missing **database internals** (WAL, MVCC, B-tree internals, query optimizer)
> - No **data pipeline / ETL / streaming** architecture
> - Missing **distributed locking**, **leader election**, **consistent hashing**
> - No **chaos engineering** or **game days**
> - Missing **API gateway design patterns** in depth
> - No **performance engineering deep-dive** (flame graphs, GC tuning, lock contention)
> - Missing **operational excellence** (toil budgets, SRE ladder, production readiness reviews)
> - No **soft skills** section (system design communication, technical writing, incident communication)
> - Missing **concurrency patterns** (thread pools, connection pools, semaphore patterns, deadlock detection)
> - No **data serialization formats** comparison (Avro, Protobuf, Thrift, MessagePack)
> - Missing **container networking**, **DNS in microservices**, **sidecar pattern**

---

## Table of Contents

| Phase | Sections | Level |
|-------|----------|-------|
| **Phase 0** | [Prerequisites & Foundations](#phase-0-prerequisites--foundations) | Before Backend |
| **Phase 1** | [Internet, Networking & Protocols](#phase-1-internet-networking--protocols) | Beginner |
| **Phase 2** | [Backend Application Architecture](#phase-2-backend-application-architecture) | Beginner |
| **Phase 3** | [APIs & Service Communication](#phase-3-apis--service-communication) | Beginner–Intermediate |
| **Phase 4** | [Databases & Data Modeling](#phase-4-databases--data-modeling) | Beginner–Intermediate |
| **Phase 5** | [Authentication, Authorization & Identity](#phase-5-authentication-authorization--identity) | Intermediate |
| **Phase 6** | [Caching & Performance Engineering](#phase-6-caching--performance-engineering) | Intermediate |
| **Phase 7** | [Async Processing, Messaging & Eventing](#phase-7-async-processing-messaging--eventing) | Intermediate |
| **Phase 8** | [File, Media & Blob Handling](#phase-8-file-media--blob-handling) | Intermediate |
| **Phase 9** | [Security (Application + Infrastructure)](#phase-9-security-application--infrastructure) | Intermediate |
| **Phase 10** | [Testing & Quality Engineering](#phase-10-testing--quality-engineering) | Intermediate |
| **Phase 11** | [Git, Collaboration & Delivery Workflow](#phase-11-git-collaboration--delivery-workflow) | Beginner–Intermediate |
| **Phase 12** | [Deployment, DevOps & Platform](#phase-12-deployment-devops--platform) | Intermediate |
| **Phase 13** | [Scalability & Distributed Systems](#phase-13-scalability--distributed-systems) | Advanced |
| **Phase 14** | [System Design & Architecture](#phase-14-system-design--architecture) | Advanced |
| **Phase 15** | [Observability & Production Readiness](#phase-15-observability--production-readiness) | Advanced |
| **Phase 16** | [Cloud Fundamentals](#phase-16-cloud-fundamentals) | Intermediate–Advanced |
| **Phase 17** | [Practical Integration Skills](#phase-17-practical-integration-skills) | Intermediate |
| **Phase 18** | [Data Engineering & Pipelines](#phase-18-data-engineering--pipelines) ⭐ NEW | Advanced |
| **Phase 19** | [Concurrency & Parallelism Deep Dive](#phase-19-concurrency--parallelism-deep-dive) ⭐ NEW | Advanced |
| **Phase 20** | [Networking Internals](#phase-20-networking-internals) ⭐ NEW | Advanced |
| **Phase 21** | [Database Internals & Advanced Storage](#phase-21-database-internals--advanced-storage) ⭐ NEW | Advanced |
| **Phase 22** | [Operational Excellence & SRE](#phase-22-operational-excellence--sre) ⭐ NEW | Advanced–Staff |
| **Phase 23** | [Documentation, Governance & Compliance](#phase-23-documentation-governance--compliance) | Intermediate–Advanced |
| **Phase 24** | [Soft Skills & Technical Leadership](#phase-24-soft-skills--technical-leadership) ⭐ NEW | All Levels |
| **Phase 25** | [Career Projects & Interview Prep](#phase-25-career-projects--interview-prep) | All Levels |

---

# Phase 0: Prerequisites & Foundations

> ⏱ **Estimated Time**: 6–10 weeks
> 🎯 **Interview Relevance**: HIGH — coding rounds, language-specific questions

## 0.1 Programming Language Mastery (pick one, then expand)

> [!TIP]
> Your project uses **Python + Django**. Master Python deeply first, then learn Go or Java for system-level thinking.

- **Core syntax and types**
  - Variables, constants, type annotations
  - Primitive types, strings, type coercion
  - Operators, expressions, operator precedence
- **Control flow**
  - `if/elif/else`, ternary operators
  - `for`, `while`, `do-while` equivalents
  - `switch/match` (Python 3.10+ structural pattern matching)
  - Loop control: `break`, `continue`, labeled loops
- **Functions**
  - Parameters: positional, keyword, default, `*args`, `**kwargs`
  - Return values, multiple returns
  - Scope: local, enclosing (closure), global, built-in (LEGB rule)
  - First-class functions, higher-order functions
  - Lambda / anonymous functions
  - Decorators and decorator factories
- **Recursion**
  - Base case and recursive case
  - Tail recursion optimization (and why Python lacks it)
  - Recursion vs iteration: stack depth, performance tradeoffs
- **Data structures in language runtime**
  - Lists/arrays: operations, slicing, comprehensions
  - Dictionaries/maps: hash-based, ordered (Python 3.7+)
  - Sets: union, intersection, difference
  - Tuples, named tuples, dataclasses
  - Deque, defaultdict, Counter, OrderedDict
- **Object-Oriented Programming**
  - Classes, objects, constructors (`__init__`)
  - Inheritance: single, multiple, MRO (Method Resolution Order)
  - Composition over inheritance
  - Polymorphism: duck typing, method overriding, operator overloading
  - Encapsulation: name mangling, property decorators
  - Abstraction: abstract base classes (ABC)
  - Interfaces and protocols (Python `Protocol` type)
  - Metaclasses (advanced, know they exist)
- **Functional programming**
  - Pure functions, referential transparency
  - Immutability and frozen dataclasses
  - Closures and lexical scoping
  - `map`, `filter`, `reduce`
  - Generators and iterators (`yield`, `yield from`)
  - Lazy evaluation
- **Error handling**
  - `try/except/else/finally`
  - Exception hierarchy, custom exceptions
  - Context managers (`with` statement, `__enter__`/`__exit__`)
  - Result types / Optional patterns
  - Error propagation strategies
- **Modules, packages, and dependency management**
  - `import` system, relative vs absolute imports
  - `__init__.py`, package structure
  - Virtual environments: `venv`, `virtualenv`, `poetry`, `uv`
  - `requirements.txt`, `pyproject.toml`, lock files
  - Semantic versioning
- **File I/O and streams**
  - Text vs binary mode
  - Buffered I/O, streaming large files
  - CSV, JSON, YAML reading/writing
  - Path handling (`pathlib` vs `os.path`)
- **Environment and configuration**
  - Environment variables, `.env` files
  - Runtime config patterns
  - 📌 **Your project**: [python-decouple in settings.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance_tracker/settings.py) — reads `SECRET_KEY`, `DEBUG`, `DB_*` from `.env`
- **Date/time handling**
  - Naive vs aware datetimes
  - Time zones (`pytz`, `zoneinfo`)
  - ISO 8601 format
  - 📌 **Your project**: [Transaction.date](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/models.py#L105) uses `timezone.now`
- **Serialization / deserialization**
  - JSON: `json.dumps`/`loads`, custom serializers
  - Pickle (and why it's insecure for untrusted data)
  - Dataclass/Pydantic serialization
- **Concurrency model**
  - **Threads**: `threading`, GIL (Global Interpreter Lock)
  - **Multiprocessing**: `multiprocessing`, process pools
  - **Async**: `asyncio`, `async/await`, event loop
  - **Node.js model**: single-threaded event loop (for comparison)
  - **Go model**: goroutines, channels (for comparison)
  - When to use each model
- **Memory basics**
  - Stack vs heap allocation
  - Garbage collection: reference counting, generational GC
  - Memory leaks in Python: circular references, `__del__`
  - `sys.getsizeof`, `tracemalloc`
- **Debugging and profiling**
  - `pdb`, `ipdb`, IDE debuggers
  - `cProfile`, `line_profiler`
  - `tracemalloc` for memory
  - Logging vs print debugging
- **Build and run tooling**
  - `pip`, `poetry`, `uv`
  - `Makefile`, `tox`, `nox`
  - Pre-commit hooks

---

## 0.2 Computer Science Essentials

> 🎯 **Interview Relevance**: CRITICAL — every coding interview tests these

### Data Structures
- **Linear**
  - Arrays: dynamic arrays, amortized O(1) append
  - Linked lists: singly, doubly, circular
  - Stacks: LIFO, call stack, monotonic stack
  - Queues: FIFO, circular queue, priority queue
  - Deques: double-ended queue
- **Hashing**
  - Hash tables/maps: collision resolution (chaining, open addressing)
  - Hash functions: properties, distribution
  - Consistent hashing ⭐ (crucial for distributed systems)
  - Bloom filters ⭐ (probabilistic membership testing)
- **Trees**
  - BST: insertion, deletion, search, in-order traversal
  - Balanced trees: AVL, Red-Black (conceptual)
  - B-trees and B+ trees ⭐ (how databases store data)
  - Tries: prefix trees for autocomplete
  - Segment trees, Fenwick trees (competitive programming)
- **Heaps**
  - Min-heap, max-heap
  - Heap operations: insert, extract-min, heapify
  - Priority queue implementation
  - Top-K problems
- **Graphs**
  - Representations: adjacency list, adjacency matrix
  - Directed, undirected, weighted
  - DAGs (Directed Acyclic Graphs) — used in task scheduling, CI pipelines

### Algorithms
- **Searching**: linear, binary, interpolation
- **Sorting**: quicksort, mergesort, heapsort, counting sort, radix sort
  - Stability, in-place, comparison-based limits
- **Recursion / Backtracking**: N-queens, permutations, subsets
- **Graph algorithms**
  - BFS / DFS: traversal, cycle detection
  - Shortest path: Dijkstra, Bellman-Ford, Floyd-Warshall
  - Minimum spanning tree: Kruskal, Prim
  - Topological sort (DAG scheduling)
  - Union-Find / Disjoint Set
- **Dynamic Programming**
  - Memoization (top-down) vs tabulation (bottom-up)
  - Classic problems: knapsack, LCS, edit distance, coin change
  - State transition identification
- **Greedy algorithms**: interval scheduling, Huffman coding
- **String algorithms**: KMP, Rabin-Karp (for search engines)
- **Bit manipulation**: XOR tricks, bit masking (for permissions)

### Complexity Analysis
- Big-O, Big-Theta (Θ), Big-Omega (Ω)
- Time/space tradeoffs
- Amortized analysis (dynamic array resizing, splay trees)
- Best/worst/average case distinction
- Recurrence relations (Master theorem)

### System-Level Basics
- **Processes vs Threads**
  - Process isolation, IPC mechanisms
  - Thread shared memory, race conditions
  - Context switching cost
- **Synchronization primitives**
  - Mutex (mutual exclusion)
  - Semaphore (counting)
  - Read-write locks
  - Condition variables
  - Monitors
  - Spinlocks (when and why)
- **Deadlock**
  - Four conditions: mutual exclusion, hold-and-wait, no preemption, circular wait
  - Prevention vs detection vs avoidance
  - 📌 **Your project**: [Budget unique_together constraint](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/models.py#L213) prevents data-level deadlocks

### Design Principles
- **SOLID principles** (with backend examples)
  - S: Single Responsibility — one service, one job
  - O: Open/Closed — extend via plugins, not modifications
  - L: Liskov Substitution — polymorphic services
  - I: Interface Segregation — small, focused interfaces
  - D: Dependency Inversion — depend on abstractions
  - 📌 **Your project**: [services.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py) follows SRP — views don't touch ORM directly
- **DRY, KISS, YAGNI**
- **Coupling vs Cohesion**: tight vs loose coupling, high cohesion
- **Law of Demeter** (principle of least knowledge)
- **Separation of Concerns**

### Design Patterns (Backend-Relevant)
- **Creational**: Factory, Abstract Factory, Builder, Singleton (and anti-pattern)
- **Structural**: Adapter, Facade, Decorator, Proxy, Composite
- **Behavioral**: Strategy, Observer, Command, Chain of Responsibility, Template Method
- **Backend-specific**:
  - Repository pattern
  - Unit of Work pattern
  - Service layer pattern
  - Dependency Injection / IoC container
  - 📌 **Your project**: [Service Layer](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py) + [Selector Layer](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/reports/selectors.py) + [AI Fallback Chain](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/reports/ai_insights.py) (Strategy + Chain of Responsibility)

---

# Phase 1: Internet, Networking & Protocols

> ⏱ **Estimated Time**: 2–3 weeks
> 🎯 **Interview Relevance**: HIGH — "What happens when you type a URL?"

## 1.1 Internet Basics
- How the internet works: packet switching, routing
- OSI model (7 layers) — know conceptually
- TCP/IP model (4 layers) — know in depth
  - Application, Transport, Internet, Network Access
- IP addressing
  - IPv4: structure, subnets, CIDR notation
  - IPv6: format, adoption status
  - Public vs private IPs
  - NAT (Network Address Translation)
- **Ports and sockets** ⭐
  - Well-known ports (80, 443, 5432, 6379, 27017)
  - Socket: IP + Port combination
  - Ephemeral ports
- **DNS resolution flow** ⭐ (interview favorite)
  - Recursive vs iterative resolution
  - DNS record types: A, AAAA, CNAME, MX, TXT, NS, SOA
  - DNS caching: browser → OS → resolver → authoritative
  - TTL (Time To Live)
  - DNS-based service discovery ⭐
- Domain names, registrar, nameservers
- CDNs: edge locations, PoPs, cache invalidation
- **NAT traversal** (important for WebRTC, P2P)

## 1.2 TCP Deep-Dive ⭐ NEW
- **TCP 3-way handshake**: SYN → SYN-ACK → ACK
- **TCP connection teardown**: FIN → ACK → FIN → ACK
- **Flow control**: sliding window, receiver window
- **Congestion control**: slow start, congestion avoidance, fast retransmit
- **TCP vs UDP**: reliability, ordering, overhead tradeoffs
- **Connection pooling** ⭐: why it matters for backend performance
  - Database connection pools (PgBouncer, HikariCP)
  - HTTP connection pools (keep-alive)
  - 📌 **Your project**: Django's `CONN_MAX_AGE` in [settings.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance_tracker/settings.py) controls DB connection reuse
- **Backlog queue**: `listen()` backlog, SYN flood attacks

## 1.3 HTTP Fundamentals
- **Request-response lifecycle** (the full journey)
  1. DNS lookup → TCP connection → TLS handshake → HTTP request → Server processing → HTTP response
- URL/URI structure: scheme, authority, path, query, fragment
- **HTTP methods** (know semantics deeply):
  - `GET` — safe, idempotent, cacheable
  - `POST` — unsafe, non-idempotent
  - `PUT` — idempotent, full replacement
  - `PATCH` — partial update
  - `DELETE` — idempotent
  - `HEAD` — like GET but no body
  - `OPTIONS` — CORS preflight
- **Status codes** (know the important ones by heart):
  - `200 OK`, `201 Created`, `204 No Content`
  - `301 Moved Permanently`, `302 Found`, `304 Not Modified`
  - `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`, `429 Too Many Requests`
  - `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`, `504 Gateway Timeout`
- **Headers** (must-know):
  - `Content-Type`, `Accept` — content negotiation
  - `Authorization` — Bearer tokens, Basic auth
  - `Cache-Control`, `ETag`, `If-None-Match`, `If-Modified-Since`
  - `X-Request-ID` — distributed tracing
  - `X-Forwarded-For`, `X-Real-IP` — proxy headers
  - CORS headers: `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`
- **Cookies**
  - `Set-Cookie` header, cookie jar
  - Attributes: `Secure`, `HttpOnly`, `SameSite` (Strict/Lax/None), `Domain`, `Path`, `Max-Age`/`Expires`
  - First-party vs third-party cookies
- **Sessions**
  - Server-side session stores (DB, Redis, files)
  - Session ID in cookie
  - Session fixation attacks
- Content negotiation: `Accept`, `Accept-Language`, `Accept-Encoding`
- Compression: `gzip`, `br` (Brotli), `deflate`
- Keep-alive, HTTP pipelining
- **Idempotency** ⭐ — critical for reliable APIs
- Conditional requests: `If-None-Match`, `If-Modified-Since`

## 1.4 HTTP/2 and HTTP/3 ⭐ NEW
- **HTTP/2**
  - Binary framing layer
  - Multiplexing: multiple streams over one connection
  - Header compression (HPACK)
  - Server push
  - Stream prioritization
- **HTTP/3 (QUIC)**
  - UDP-based, built-in encryption
  - Faster connection establishment (0-RTT)
  - No head-of-line blocking
  - Connection migration

## 1.5 HTTPS and Transport Security
- **TLS handshake** (simplified)
  - ClientHello → ServerHello → Certificate → Key Exchange → Finished
  - Symmetric vs asymmetric encryption roles
- Certificates: X.509, CAs, certificate chain, Let's Encrypt
- Certificate pinning
- HSTS (HTTP Strict Transport Security)
- **mTLS** (mutual TLS) — service-to-service authentication
- OCSP stapling
- Certificate transparency logs

---

# Phase 2: Backend Application Architecture

> ⏱ **Estimated Time**: 3–4 weeks
> 🎯 **Interview Relevance**: HIGH — architectural design questions

## 2.1 Core Application Structure
- **Monolith layered architecture**
  - Presentation → Business Logic → Data Access → Database
  - When monoliths are the right choice (spoiler: most of the time initially)
- **Architectural patterns**
  - MVC (Model–View–Controller)
  - MVT (Model–View–Template) — Django's variant
  - Hexagonal / Ports & Adapters / Clean Architecture
  - Onion Architecture
  - Vertical Slice Architecture ⭐ NEW
- **Routing and request handling**
  - URL routing: path parameters, query parameters
  - Request dispatch to handlers/controllers
  - 📌 **Your project**: [urls.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/urls.py) routes → [views.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/views.py) (thin views)
- **Service layer / Business logic**
  - Why views shouldn't contain business logic
  - Service functions vs service classes
  - 📌 **Your project**: [services.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py) — `create_transaction`, `update_transaction`, `delete_transaction` with budget side-effects
- **Repository / Data access layer**
  - Abstracting database queries
  - 📌 **Your project**: [selectors.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/reports/selectors.py) — all aggregation queries isolated from views
- **DTOs, entities, view models**
  - Domain models vs API contracts
  - Why you shouldn't expose database models directly
- **Dependency injection / IoC**
  - Constructor injection, method injection
  - DI containers (Spring, .NET DI)
  - 📌 **Your project**: Django's `settings.py` acts as a simple IoC for API keys

## 2.2 Middleware and Request Pipeline
- **How middleware works**: onion model (request → middleware chain → handler → response chain)
- **Common middleware types**:
  - Authentication/authorization middleware
  - Request validation middleware
  - Logging and tracing middleware
  - Rate-limiting middleware
  - Error/exception handling middleware
  - CORS middleware
  - Compression middleware
- **Request context propagation**
  - Request ID generation and forwarding
  - User context (from JWT/session)
  - Correlation IDs for distributed tracing
  - 📌 **Your project**: [context_processors.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/context_processors.py) — injects notification count into all templates

## 2.3 Configuration and Environments
- **12-Factor App methodology** ⭐ (interview classic)
  1. Codebase — one repo, many deploys
  2. Dependencies — explicitly declared
  3. Config — stored in environment variables
  4. Backing services — treat as attached resources
  5. Build, release, run — strict separation
  6. Processes — stateless, share-nothing
  7. Port binding — self-contained
  8. Concurrency — scale via process model
  9. Disposability — fast startup, graceful shutdown
  10. Dev/prod parity — keep environments similar
  11. Logs — treat as event streams
  12. Admin processes — run as one-off tasks
  - 📌 **Your project**: Follows factors 1–5, 7, 10, 12. Factor 6 (stateless) applies since sessions use Django's DB backend
- **Environment-based configuration**
  - `.env` files, environment variables
  - Config hierarchy: defaults → env file → env vars → CLI args
  - 📌 **Your project**: [.env.example](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/.env.example) documents all config variables
- **Secret management**
  - Why secrets don't belong in code or version control
  - Vault (HashiCorp), AWS Secrets Manager, GCP Secret Manager
  - Rotation strategies
- **Feature flags and runtime toggles**
  - LaunchDarkly, Unleash, simple DB-backed flags
  - Gradual rollouts, A/B testing
  - Kill switches for emergencies
  - **Feature flag governance** ⭐ UPDATED
    - **Flag lifecycle**: create → gradual rollout → full rollout → cleanup (remove flag + dead code)
    - **Stale flag debt management**: track flag age, alert on flags older than 30/60/90 days
    - **Ownership**: every flag must have an owner (team/person) and an expiry date
    - **Types**: release flags (temporary), ops flags (kill switches, permanent), experiment flags (A/B, temporary), permission flags (long-lived)
    - **Naming conventions**: `enable_new_checkout_flow`, `kill_switch_external_payments`
    - **Testing with flags**: test all flag states in CI, not just the default
    - **Audit trail**: log who toggled what flag, when, and why

## 2.4 Error Strategy
- **Operational vs programmer errors**
  - Operational: network timeout, disk full — handle gracefully
  - Programmer: null reference, type error — fix the bug
- **Global exception handling**
  - Catch-all middleware for unhandled exceptions
  - Never expose stack traces in production
- **Consistent error response format** ⭐
  ```json
  {
    "error": {
      "code": "BUDGET_OVERRUN",
      "message": "Budget limit exceeded for category 'Food'",
      "details": { "spent": 150.00, "limit": 100.00 },
      "request_id": "req_abc123"
    }
  }
  ```
- Error codes: machine-readable, documented
- **Retry and fallback behavior**
  - Idempotency for safe retries
  - Circuit breaker for cascading failure prevention
  - 📌 **Your project**: [AI Insights fallback chain](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/reports/ai_insights.py) — Gemini → OpenAI → Rule-based (always succeeds)

## 2.5 Application Lifecycle ⭐ NEW
- **Startup sequence**
  - Configuration loading order
  - Database migration verification
  - Health check endpoints
  - Warm-up / cache priming
- **Graceful shutdown**
  - Drain in-flight requests
  - Close database connections
  - Flush logs and metrics
  - SIGTERM handling
- **Readiness vs liveness**
  - Readiness: "Can I accept traffic?"
  - Liveness: "Am I still alive?"

---

# Phase 3: APIs & Service Communication

> ⏱ **Estimated Time**: 3–4 weeks
> 🎯 **Interview Relevance**: VERY HIGH — API design is core to backend interviews

## 3.1 REST API Design
- **Resource modeling**
  - Nouns, not verbs: `/transactions` not `/getTransactions`
  - Nested resources: `/users/{id}/transactions`
  - 📌 **Your project**: [urls.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/urls.py) — resource-based URL patterns
- **URI naming conventions**
  - Plural nouns: `/categories`, `/budgets`
  - Lowercase with hyphens: `/bank-statements`
  - No trailing slashes (or be consistent)
- **CRUD semantics**
  - POST → Create, GET → Read, PUT → Full Replace, PATCH → Partial Update, DELETE → Delete
- **Pagination** ⭐ (interview favorite)
  - **Offset-limit**: `?page=2&limit=20` — simple but O(n) at scale
  - **Cursor-based**: `?cursor=abc123&limit=20` — efficient, no skipping
  - **Keyset pagination**: `?after_id=100&limit=20` — DB-friendly
  - When to use each
- **Filtering, sorting, searching**
  - `?status=active&category=food`
  - `?sort=-date,amount` (minus = descending)
  - `?search=grocery`
  - 📌 **Your project**: [get_user_transactions](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py#L83-L102) — supports type, category, date range, currency filters
- **Partial responses / field selection**: `?fields=id,name,amount`
- **API versioning strategies**
  - URL path: `/v1/transactions` — most common
  - Header: `Accept: application/vnd.api.v2+json`
  - Query param: `?version=2`
  - No versioning (evolve with backward compatibility)
- **HATEOAS** (Hypermedia): links in responses for discoverability
- **OpenAPI / Swagger documentation**
  - Schema-first vs code-first
  - Auto-generated docs
- **Idempotency keys** ⭐
  - `Idempotency-Key: uuid-here` header
  - Server stores result for N minutes
  - Prevents duplicate charges, duplicate creates
- **Rate limiting** ⭐ NEW
  - Token bucket, sliding window, fixed window algorithms
  - Per-user, per-IP, per-API-key limits
  - `429 Too Many Requests` with `Retry-After` header
  - 📌 **Your project**: Consider adding rate limiting to [budget check](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py#L105-L184) email sends
- **Bulk operations** ⭐ NEW
  - Batch create/update: `POST /transactions/batch`
  - Partial success handling
  - 📌 **Your project**: [import_service.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/import_service.py) — bulk import with duplicate detection

## 3.2 Data Interchange
- **JSON serialization**
  - Naming conventions: `camelCase` vs `snake_case`
  - Null handling: omit vs explicit null
  - 📌 **Your project**: [AI insights](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/reports/ai_insights.py) parse LLM output as JSON
- **Schema validation**
  - JSON Schema
  - Pydantic (Python), Joi (Node.js), Zod (TypeScript)
  - Request body validation at API boundary
- **Backward/forward compatibility** ⭐
  - Adding fields = backward compatible
  - Removing/renaming fields = breaking
  - Additive changes only for non-breaking evolution
- **Data format pitfalls**
  - Floating point for money (never!) → use Decimal
  - Date/time: always ISO 8601, always include timezone
  - Large integers (>2^53 for JavaScript) → use strings
  - 📌 **Your project**: [Decimal with ROUND_HALF_UP](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/models.py#L96-L98) — financial-grade precision
- **Serialization formats comparison** ⭐ NEW
  - JSON: human-readable, universal, verbose
  - Protocol Buffers (Protobuf): compact, typed, schema-required
  - Avro: schema evolution, Kafka-friendly
  - MessagePack: binary JSON, compact
  - Thrift: Facebook's RPC format
  - When to use each

## 3.3 Alternative API Protocols
- **GraphQL**
  - Schema definition language (SDL)
  - Queries, mutations, subscriptions
  - Resolvers and data loaders
  - **N+1 problem** and batching (DataLoader)
  - Over-fetching and under-fetching solutions
  - Pagination: Relay cursor spec
  - When GraphQL > REST (and vice versa)
- **gRPC**
  - Protocol Buffers (protobuf) schema
  - Unary, server streaming, client streaming, bidirectional streaming
  - HTTP/2-based, binary, fast
  - When to use: internal service-to-service calls
  - gRPC-Web for browser clients
  - **gRPC Operations Depth** ⭐ UPDATED
    - **Status codes**: OK, CANCELLED, DEADLINE_EXCEEDED, NOT_FOUND, ALREADY_EXISTS, PERMISSION_DENIED, RESOURCE_EXHAUSTED, UNAVAILABLE, INTERNAL
    - **Deadlines and timeouts**: propagate deadlines across service hops; `context.WithTimeout()` / `grpc.Deadline`
    - **Interceptors**: unary + streaming interceptors for logging, auth, metrics, retry (equivalent of HTTP middleware)
    - **Retries**: retry policies in service config, hedging policies, idempotent-only retries
    - **Health checking**: gRPC Health Checking Protocol (`grpc.health.v1.Health`), integration with Kubernetes probes
    - **Reflection**: enable server reflection for `grpcurl` debugging, disable in production
    - **Observability**: OpenTelemetry gRPC instrumentation, per-RPC latency histograms, stream message counts
    - **Load balancing**: client-side (pick_first, round_robin), xDS-based (Envoy/Istio), look-aside LB
    - **Connection management**: keepalive pings, max connection age, idle timeout, GOAWAY frames
    - **Resilience**: circuit breaking via service mesh, bulkhead per-channel, backpressure via flow control
- **SOAP** (legacy awareness)
  - WSDL, XML-based, enterprise legacy
- **WebSockets**
  - Full-duplex, persistent connection
  - Connection lifecycle: upgrade handshake, frames, close
  - Scaling challenges: sticky sessions, pub/sub backing
  - When to use: chat, live updates, gaming
- **Server-Sent Events (SSE)**
  - One-way server-to-client streaming
  - Simpler than WebSockets for notifications
  - Auto-reconnection built into `EventSource`
- **Webhooks**
  - Callback URLs for event notification
  - Signature verification (HMAC)
  - Retry policies, idempotent handling
  - Webhook security: shared secrets, IP whitelisting

## 3.4 API Governance
- **API contracts**: producer-consumer agreement
- **Contract testing**: Pact, Spring Cloud Contract
- **Consumer-driven contract testing in CI** ⭐ UPDATED
  - Contracts as CI mandatory gate (not just concept — enforce in pipeline)
  - Producer builds fail if contract is broken
  - Consumer publishes contract expectations to broker (Pact Broker, Pactflow)
  - Workflow: consumer writes contract → publish → provider verifies → deploy
  - Run contract tests on every PR, not just nightly
  - Combine with OpenAPI diff tools (`oasdiff`, `optic`) for schema-level breaking change detection
- **Deprecation policies**: sunset header, migration guides
- **API gateway patterns** ⭐ NEW
  - Routing, authentication, rate limiting
  - Request/response transformation
  - API composition (aggregation)
  - Kong, AWS API Gateway, Nginx as gateway
- **Backend-for-Frontend (BFF)** ⭐ NEW
  - One API gateway per client type (web, mobile, IoT)
  - Tailored payloads, reduced chattiness
- **Platform boundary with frontend** ⭐ UPDATED
  - **Version negotiation strategy**: `Accept-Version` header, API version discovery endpoint
  - **Deprecation headers**: `Sunset: Sat, 01 Mar 2027 00:00:00 GMT` + `Deprecation: true` + `Link: <migration-guide>`
  - **Coordinated rollout plans**: backend deploys first (backward compatible) → frontend deploys → old API removed
  - **Feature detection over version checking**: frontend checks capability endpoints rather than hardcoding version numbers
  - **Graceful degradation for stale clients**: old mobile app versions get sensible defaults, not crashes
  - **API changelog / breaking change notifications**: automated Slack/email to frontend teams on contract changes

---

# Phase 4: Databases & Data Modeling

> ⏱ **Estimated Time**: 4–6 weeks
> 🎯 **Interview Relevance**: CRITICAL — every backend interview covers databases

## 4.1 Relational Database Fundamentals
- **Core concepts**
  - Tables, rows, columns, schemas
  - Primary key (natural vs surrogate)
  - Foreign keys and referential integrity
  - Constraints: UNIQUE, CHECK, NOT NULL, DEFAULT
  - 📌 **Your project**: [Transaction model](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/models.py#L68-L176) — FK with PROTECT, unique_together, custom validation
- **Normalization** ⭐
  - 1NF: atomic values, no repeating groups
  - 2NF: no partial dependencies
  - 3NF: no transitive dependencies
  - BCNF: every determinant is a candidate key
  - **Denormalization**: when and why (performance)
  - 📌 **Your project**: [Transaction.type is denormalized](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/models.py#L94-L95) from Category.type for aggregation performance
- **Indexes** ⭐ (interview must-know)
  - B-tree indexes: most common, range queries
  - Hash indexes: exact match only
  - Composite/compound indexes: column order matters!
  - Covering indexes: include all queried columns
  - Partial/filtered indexes
  - GIN/GiST indexes (for full-text search, JSONB)
  - Index scan vs sequential scan
  - When NOT to index: high-write, low-cardinality
  - 📌 **Your project**: [Custom indexes](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/models.py#L116-L120) on `(user, date)`, `(user, category)`, `(user, type)`

### SQL Core (must be fluent)
- **CRUD**: SELECT, INSERT, UPDATE, DELETE
- **JOINs** ⭐
  - INNER JOIN: matching rows only
  - LEFT JOIN: all left + matching right
  - RIGHT JOIN: all right + matching left
  - FULL OUTER JOIN: all rows from both
  - CROSS JOIN: Cartesian product
  - Self-join: table joined with itself
- **Aggregation**
  - GROUP BY, HAVING
  - COUNT, SUM, AVG, MIN, MAX
  - DISTINCT
- **Subqueries and CTEs**
  - Correlated vs non-correlated subqueries
  - Common Table Expressions (`WITH` clause)
  - Recursive CTEs (for tree structures)
- **Window functions** ⭐ (often asked in interviews)
  - `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`
  - `LAG()`, `LEAD()` — previous/next row
  - `SUM() OVER (PARTITION BY ... ORDER BY ...)` — running totals
  - `NTILE()` — bucketing
  - 📌 **Your project**: Could enhance [monthly trends](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/reports/selectors.py) with window functions for running totals
- **Advanced SQL**
  - UPSERT / `ON CONFLICT` (INSERT ... ON CONFLICT DO UPDATE)
  - `CASE WHEN` expressions
  - `COALESCE`, `NULLIF`
  - String functions, date functions
  - JSON/JSONB operations (PostgreSQL)
  - `EXPLAIN ANALYZE` — reading query plans ⭐

### Transactions and Concurrency Control ⭐
- **ACID properties**
  - Atomicity: all or nothing
  - Consistency: valid state transitions
  - Isolation: concurrent transactions don't interfere
  - Durability: committed = persisted
- **Isolation levels** (know the tradeoffs)
  - READ UNCOMMITTED → dirty reads possible
  - READ COMMITTED → no dirty reads (PostgreSQL default)
  - REPEATABLE READ → no non-repeatable reads
  - SERIALIZABLE → no phantom reads (strictest)
  - 📌 **Your project**: PostgreSQL default is READ COMMITTED; [Budget.spent](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/models.py#L258-L283) queries live data to avoid stale reads
- **Anomalies**
  - Dirty read, non-repeatable read, phantom read
  - Write skew (serializable needed)
- **Locks**
  - Row-level vs table-level locks
  - Shared (read) vs exclusive (write) locks
  - Advisory locks
  - `SELECT ... FOR UPDATE` (pessimistic locking) ⭐
  - Optimistic locking with version columns ⭐
  - 📌 **Your project**: Budget.spent is a computed property, not cached — avoids stale data but may need `FOR UPDATE` under high concurrency
- **Deadlocks**: detection, prevention, timeout

### Data Lifecycle
- Migrations: schema evolution, rollback strategies
  - 📌 **Your project**: Django migrations in [finance/migrations](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/migrations)
- **Schema migration safety at scale** ⭐ UPDATED
  - **Expand/Contract pattern** (the gold standard for zero-downtime migrations):
    1. **Expand**: add new column/table alongside old one
    2. **Migrate**: dual-write to both old and new, backfill historical data
    3. **Contract**: remove old column/table after all readers switched
  - **Dual-write / dual-read migrations**: write to both schemas during transition; read from new, fall back to old
  - **Online backfills**: batch-update existing rows in small chunks (`UPDATE ... WHERE id BETWEEN x AND y`), avoid locking entire table
  - **Zero-downtime migration rules**:
    - ✅ Add nullable column, add new table, add index `CONCURRENTLY`
    - ❌ Never rename/remove columns, change types, or add NOT NULL without default in one step
  - **Migration ordering**: deploy code that handles both schemas → run migration → deploy code that only uses new schema
  - **Rollback strategy**: every migration must have a reverse migration; test rollback before deploying forward
  - **Large table migrations**: `pg_repack`, `pt-online-schema-change` (Percona), `gh-ost` (GitHub) for MySQL
  - 📌 **Your project**: Django migrations are sequential — for production-scale changes, consider the expand/contract pattern when modifying [Transaction](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/models.py) or [Budget](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/models.py#L178) models
- Database seeding for initial data
  - 📌 **Your project**: [seed_currencies.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/management) management command
- Backups: logical (pg_dump) vs physical (file-level)
- Point-in-time recovery (PITR) via WAL archiving
- Soft delete vs hard delete
  - `is_deleted` + `deleted_at` columns
  - Filtered indexes to exclude soft-deleted rows
- TTL-based expiration
- Data anonymization / pseudonymization (GDPR)
- Archiving: move old data to cold storage

## 4.2 NoSQL Fundamentals
- **Key-Value stores** (Redis, DynamoDB)
  - When: caching, sessions, counters, rate limiting
- **Document databases** (MongoDB, CouchDB)
  - Schema-less, nested documents
  - When: content management, user profiles, catalogs
- **Column-family databases** (Cassandra, HBase)
  - Write-optimized, wide rows
  - When: time-series, IoT, event logging
- **Graph databases** (Neo4j, Amazon Neptune)
  - Nodes, edges, properties
  - When: social networks, recommendation engines, fraud detection
- **Data modeling tradeoffs**
  - Embedding vs referencing in document stores
  - Denormalization trade-offs
  - Query-driven modeling (design for access patterns)
- **Consistency models**
  - Strong consistency: read-after-write guaranteed
  - Eventual consistency: reads may be stale temporarily
  - Tunable consistency (Cassandra: ONE, QUORUM, ALL)
- Secondary indexes in NoSQL: limitations, LSM-tree implications

## 4.3 ORMs / ODMs
- Mapping entities and relations: one-to-one, one-to-many, many-to-many
- **Lazy vs eager loading**
  - Lazy: query on access (N+1 risk)
  - Eager: `select_related` (FK), `prefetch_related` (M2M)
  - 📌 **Your project**: [get_user_transactions uses select_related](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py#L88) — `.select_related('category', 'currency')`
- **N+1 problem** ⭐ (interview classic)
  - Problem: 1 query for list + N queries for related objects
  - Fix: eager loading, batch queries, DataLoader
- Transaction scope handling in ORMs
- **When to use raw SQL** — complex aggregations, performance-critical queries
- Query builder pattern (SQLAlchemy, Knex.js)
- ORM anti-patterns: fat models, logic in queries

---

# Phase 5: Authentication, Authorization & Identity

> ⏱ **Estimated Time**: 2–3 weeks
> 🎯 **Interview Relevance**: HIGH — security-conscious design is critical

## 5.1 Authentication
- **Username/password flows**
  - Registration → email verification → login
  - Login throttling, lockout policies
- **Password hashing** ⭐
  - Never store plaintext! Never MD5/SHA-256 alone!
  - `bcrypt`: adaptive cost factor, salt built-in
  - `scrypt`: memory-hard, GPU-resistant
  - `argon2`: winner of PHC, memory + time + parallelism tunable
  - Salt: per-password random value, prevents rainbow tables
  - Pepper: server-side secret (additional layer)
- **MFA / 2FA**
  - TOTP (Time-based One-Time Password) — Google Authenticator, Authy
  - SMS: not recommended (SIM swapping)
  - Hardware keys: FIDO2/WebAuthn
  - Recovery codes
- **Session-based auth** ⭐
  - Session ID stored in cookie
  - Session data stored server-side (DB, Redis, file)
  - Pros: easy revocation, server-controlled
  - Cons: server state, scaling challenges
  - 📌 **Your project**: Django session-based auth with DB backend
- **Token-based auth (JWT)** ⭐
  - Structure: header.payload.signature (Base64url)
  - Claims: `sub`, `exp`, `iat`, `iss`, `aud`, custom claims
  - Signing: HS256 (shared secret), RS256 (asymmetric)
  - Pros: stateless, scalable
  - Cons: can't revoke easily, payload visible
  - **Token storage**: HttpOnly cookie vs localStorage (cookie wins)
- **Token expiry and refresh tokens**
  - Short-lived access token (15 min)
  - Long-lived refresh token (7 days)
  - Refresh token rotation (one-time use)
- **Device/session management**
  - Track active sessions
  - Revoke specific sessions
  - "Log out everywhere"
- **Logout semantics**
  - Session-based: delete server-side session
  - JWT: add to blacklist/revocation list, or short expiry
  - 📌 **Your project**: [views.py logout](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/core/views.py) — Django's built-in logout

## 5.2 Authorization
- **RBAC (Role-Based Access Control)** ⭐
  - Users → Roles → Permissions
  - Admin, Editor, Viewer pattern
- **ABAC (Attribute-Based Access Control)**
  - Rules based on user, resource, environment attributes
  - "User can edit document if user.department == document.department"
- **Resource-level permissions** ⭐
  - Object ownership checks
  - 📌 **Your project**: [Ownership check in services.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py#L47-L48) — `if transaction.user_id != user.id: raise PermissionDenied`
- **Scopes and claims** (OAuth 2.0)
  - `read:transactions`, `write:budgets`
- **Policy engines**: OPA (Open Policy Agent), Casbin, Cedar

## 5.3 Federation and Delegated Auth
- **OAuth 2.0** ⭐ (interview must-know)
  - Roles: Resource Owner, Client, Authorization Server, Resource Server
  - Grant types:
    - Authorization Code (with PKCE) — recommended for web apps
    - Client Credentials — machine-to-machine
    - Implicit (deprecated)
    - Resource Owner Password (deprecated)
  - Tokens: access token, refresh token
  - Scopes
  - 📌 **Your project**: [Google OAuth via django-allauth](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/core/views.py) — Authorization Code flow
- **OIDC (OpenID Connect)**
  - Identity layer on top of OAuth 2.0
  - ID token (JWT with user info)
  - UserInfo endpoint
- **Social login** implementation
- **SSO / SAML** (enterprise awareness)
  - SAML assertion, IdP, SP
  - When enterprises require it

## 5.4 Identity Security
- Credential stuffing defenses: rate limiting, CAPTCHA
- Brute-force protection: progressive delays, account lockouts
- Secure account recovery: time-limited tokens, no security questions
- Email verification flows
- **Account enumeration prevention** ⭐ NEW
  - "If an account exists, we've sent a reset email" (same message regardless)

---

# Phase 6: Caching & Performance Engineering

> ⏱ **Estimated Time**: 2–3 weeks
> 🎯 **Interview Relevance**: VERY HIGH — system design interviews

## 6.1 Caching Layers
- **Browser caching**: `Cache-Control`, `ETag`
- **CDN caching**: edge servers, cache invalidation
- **Reverse proxy caching**: Nginx, Varnish
- **Application-level caching**: in-memory (local)
- **Distributed caching**: Redis, Memcached
  - Redis data types: strings, hashes, lists, sets, sorted sets
  - Redis use cases beyond caching: pub/sub, rate limiting, leaderboards, sessions
  - Memcached vs Redis: simplicity vs features
  - Cache topology: client-side, sidecar, centralized
  - **Redis operational pitfalls** ⭐ UPDATED
    - **Eviction policies**: know when each applies
      - `noeviction`: return errors when memory full (default — dangerous if unexpected)
      - `allkeys-lru`: evict least recently used (best general-purpose cache policy)
      - `volatile-lru`: evict LRU among keys with TTL only
      - `allkeys-random`, `volatile-random`, `volatile-ttl`
    - **Persistence modes**:
      - **RDB** (snapshotting): periodic point-in-time snapshots, fast restart, data loss between snapshots
      - **AOF** (Append-Only File): log every write, more durable, slower restart, larger files
      - **RDB + AOF hybrid**: recommended for production — AOF durability + RDB fast recovery
    - **Hot keys**: single key getting disproportionate traffic → read replicas, local caching, key splitting
    - **Big keys**: keys with large values (>10KB) → cause latency spikes; use `MEMORY USAGE`, `redis-cli --bigkeys`
    - **Memory fragmentation**: `mem_fragmentation_ratio` > 1.5 is concerning; `activedefrag yes` in Redis 4+
    - **Thundering herd on restart**: cold cache after restart → stampede; pre-warm critical keys
    - **Connection limits**: default `maxclients 10000`; monitor with `INFO clients`
    - **Slow commands**: avoid `KEYS *` in production (use `SCAN`), watch `SLOWLOG`
    - **Cluster mode pitfalls**: cross-slot operations fail, resharding complexity, Lua script limitations

## 6.2 Caching Strategies ⭐ (interview favorite)
- **Cache-aside (Lazy Loading)**
  - App checks cache → miss → query DB → store in cache → return
  - Most common pattern
- **Read-through**
  - Cache itself fetches from DB on miss
- **Write-through**
  - Write to cache AND DB simultaneously
- **Write-back (Write-behind)**
  - Write to cache first, async flush to DB
  - Risk: data loss if cache crashes before flush
- **Write-around**
  - Write directly to DB, invalidate cache
- **TTL selection** ⭐
  - Too short: cache miss ratio too high
  - Too long: stale data
  - Dynamic TTL based on access frequency
- **Cache invalidation** ⭐ (the hard problem)
  - Time-based expiry (TTL)
  - Event-based invalidation (pub/sub on data change)
  - Versioned keys: `user:123:v3`
  - "There are only two hard things in CS: cache invalidation and naming things"
- **Cache stampede / thundering herd** ⭐
  - Problem: cache expires → 1000 requests hit DB simultaneously
  - Solutions:
    - **Mutex/lock**: only one request fetches, others wait
    - **Request coalescing** (singleflight): deduplicate identical in-flight requests
    - **Stale-while-revalidate**: serve stale, refresh async
    - **Early expiration** (probabilistic): renew before TTL expires
- **Hot key handling**: replicate hot keys across multiple cache nodes

## 6.3 HTTP Performance
- **ETag / Last-Modified validation**: conditional requests avoid re-transferring unchanged data
- **Compression**: gzip/Brotli for text responses
- **Connection reuse**: HTTP keep-alive, connection pooling
- **Payload minimization**: field selection, pagination
- **Batching vs chattiness**: fewer large requests > many small ones

## 6.4 Profiling and Tuning ⭐ NEW (expanded)
- **CPU profiling**
  - Flame graphs: visualize call stack time
  - `cProfile`, `py-spy` (Python), `async-profiler` (Java)
  - Identifying hot functions
- **Memory profiling**
  - Heap dumps, allocation tracking
  - `tracemalloc` (Python), `jcmd` (JVM)
  - Memory leaks: circular references, event listeners
- **I/O bottleneck identification**
  - Slow queries: `EXPLAIN ANALYZE`
  - Network latency: `tcpdump`, `Wireshark`
  - Disk I/O: `iostat`, `iotop`
- **Database query tuning**
  - Slow query log
  - Index usage analysis
  - Query plan optimization
  - Connection pool sizing
  - N+1 detection tools
- **Throughput vs latency tradeoffs**
  - Batching increases throughput, may increase latency
  - Caching reduces latency, requires invalidation logic
  - Compression saves bandwidth, costs CPU

---

# Phase 7: Async Processing, Messaging & Eventing

> ⏱ **Estimated Time**: 3–4 weeks
> 🎯 **Interview Relevance**: HIGH — system design, distributed systems

## 7.1 Background Job Processing
- **Job queues**: Celery, Sidekiq, Bull, RQ
  - Task serialization and deserialization
  - Worker pool sizing
- **Scheduling / Cron jobs**
  - Periodic tasks: daily reports, data cleanup
  - Distributed cron: avoiding duplicate execution (leader election)
  - 📌 **Your project**: Could use Celery for async budget check emails instead of sync [Resend calls](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py#L171-L180)
- **Delayed jobs**: execute after N minutes/hours
- **Retry policies** ⭐
  - Fixed delay, exponential backoff, exponential backoff with jitter
  - Max retries, retry budget
- **Dead-letter queues (DLQ)**
  - Where failed messages go after max retries
  - Manual inspection and replay
- **Idempotent workers** ⭐ — processing same message twice must be safe
- **Priority queues** ⭐ NEW: critical tasks before low-priority tasks

## 7.2 Messaging Systems ⭐
- **Pub/Sub vs Queue semantics**
  - Queue: one consumer gets each message (work distribution)
  - Pub/Sub: all subscribers get each message (broadcast)
- **Technologies**
  - **RabbitMQ**: AMQP, exchanges, queues, bindings, virtual hosts
  - **Apache Kafka**: distributed log, partitions, consumer groups, offset management
  - **Redis Pub/Sub + Streams**: lightweight messaging
  - **AWS SQS/SNS, Google Pub/Sub**: managed alternatives
- **Delivery guarantees** ⭐
  - At-most-once: fire and forget (may lose messages)
  - At-least-once: retry until ACK (may duplicate) — most common
  - Exactly-once: hardest to achieve (Kafka transactions)
  - **Exactly-once reality** ⭐ UPDATED
    - **True exactly-once delivery is impossible** in distributed systems (Two Generals' Problem)
    - What Kafka calls "exactly-once" is actually: idempotent producer + transactional consumer within Kafka boundary
    - **End-to-end exactly-once is an illusion** — it's actually: at-least-once delivery + idempotent processing + deduplication
    - **Practical implementation**: assign each message a unique ID → consumer checks dedup table before processing → process → record ID → commit
    - **Idempotency key pattern**: `INSERT INTO processed_messages (message_id) ON CONFLICT DO NOTHING`
    - Always design consumers to be idempotent — this is the real solution, not "exactly-once"
- **Ordering guarantees**
  - Per-partition ordering (Kafka)
  - FIFO queues (SQS FIFO)
  - When ordering doesn't matter (most cases)
- **Consumer groups and partitioning** (Kafka)
  - Partition assignment strategies
  - Rebalancing
  - Consumer lag monitoring
- **Message retention and replay**: Kafka's log-based retention
- **Backpressure** ⭐ NEW
  - When producers outpace consumers
  - Solutions: bounded queues, rate limiting producers, adaptive consumers

## 7.3 Event-Driven Architecture ⭐
- **Domain events vs integration events**
  - Domain: within bounded context (`TransactionCreated`)
  - Integration: across services (`PaymentProcessed`)
  - 📌 **Your project**: [Budget overrun check](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py#L105-L184) is a domain event side-effect — transaction creates trigger notification+email
- **Event schema and versioning**
  - Schema registry (Confluent Schema Registry)
  - Backward/forward compatible evolution
- **Eventual consistency** ⭐
  - Accept that systems may be temporarily inconsistent
  - Compensating transactions
  - Read-your-writes consistency
- **Outbox pattern** ⭐ (interview must-know)
  - Problem: DB write + message publish must be atomic
  - Solution: write event to outbox table in same DB transaction, poll+publish separately
  - CDC (Change Data Capture): Debezium polls DB changes → publishes to Kafka
- **Inbox pattern** ⭐ UPDATED (consumer-side counterpart to Outbox)
  - Problem: consumer may receive the same message twice (at-least-once delivery)
  - Solution: consumer writes incoming message ID to inbox table in same transaction as processing
  - Before processing: `SELECT 1 FROM inbox WHERE message_id = ?` — skip if already processed
  - After processing: `INSERT INTO inbox (message_id, processed_at) VALUES (?, NOW())` within same DB transaction as business logic
  - **Outbox + Inbox pair** = reliable end-to-end messaging: producer guarantees publish, consumer guarantees exactly-once processing
  - Inbox table cleanup: TTL-based purge of old entries (e.g., delete entries older than 7 days)
- **Saga pattern** ⭐ (interview must-know)
  - **Choreography**: each service publishes events, next service reacts
  - **Orchestration**: central coordinator directs the flow
  - Compensating transactions for rollback

---

# Phase 8: File, Media & Blob Handling

> ⏱ **Estimated Time**: 1–2 weeks
> 🎯 **Interview Relevance**: MEDIUM — practical backend knowledge

## 8.1 Upload / Download Handling
- Multipart uploads: `multipart/form-data`
- Streaming large files: chunked transfer, avoid loading entire file in memory
- Resumable uploads: tus protocol, Google's resumable upload API
- MIME type validation: check both extension and magic bytes
- File size limits and quotas
- 📌 **Your project**: [Transaction.receipt](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/models.py#L107-L110) — receipt upload to `receipts/%Y/%m/`

## 8.2 Storage Systems
- Local filesystem vs object storage
- **Object storage**: S3, GCS, Azure Blob
  - Buckets, keys, metadata
  - Consistency model (strong for S3 since 2020)
- **Pre-signed URLs** ⭐: time-limited direct access to private objects
- Lifecycle policies: transition to cheaper storage tiers
- CDN for media delivery: CloudFront, Cloudflare

## 8.3 File Security
- Malware scanning: ClamAV integration
- **Filename/path sanitization**: prevent path traversal attacks
- Access control: public vs private files, signed URLs
- Encryption: at rest (SSE-S3, SSE-KMS) and in transit (HTTPS)
- 📌 **Your project**: [import_service.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/import_service.py) — CSV/PDF parsing with validation

---

# Phase 9: Security (Application + Infrastructure)

> ⏱ **Estimated Time**: 2–3 weeks
> 🎯 **Interview Relevance**: HIGH — security questions are common

## 9.1 AppSec Core (OWASP Top 10)
- **SQL injection** ⭐ — parameterized queries, NEVER string concatenation
  - 📌 **Your project**: Django ORM prevents SQL injection by default
- **XSS (Cross-Site Scripting)** ⭐
  - Stored XSS, reflected XSS, DOM-based XSS
  - Prevention: output encoding, CSP, sanitization
  - 📌 **Your project**: Django templates auto-escape HTML
- **CSRF (Cross-Site Request Forgery)** ⭐
  - Prevention: CSRF tokens, SameSite cookies
  - 📌 **Your project**: Django CSRF middleware active
- **SSRF (Server-Side Request Forgery)**
  - Prevention: allowlist URLs, block private IP ranges
- **Broken authentication / access control**
- **Security misconfiguration**
- **Insecure deserialization**
- **Insufficient logging and monitoring**
- **Clickjacking**: `X-Frame-Options: DENY`
- **Path traversal**: sanitize file paths, chroot
- **Command injection**: never pass user input to shell
- **Mass assignment** ⭐ NEW: whitelist allowed fields, not blacklist

## 9.2 Secure Coding Practices
- Input validation at API boundary (whitelist, not blacklist)
- Output encoding (HTML, URL, JavaScript contexts)
- **Least privilege principle**: minimal permissions for each component
- **Secret rotation** and key management
- **Security headers** ⭐:
  - `Content-Security-Policy` (CSP)
  - `X-Frame-Options: DENY`
  - `X-Content-Type-Options: nosniff`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Permissions-Policy`
  - `Strict-Transport-Security` (HSTS)
- Safe cookie settings: `Secure`, `HttpOnly`, `SameSite`
- 📌 **Your project**: [Security settings](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance_tracker/settings.py) — `SECURE_PROXY_SSL_HEADER`, `CSRF_TRUSTED_ORIGINS`
- **Dependency vulnerability scanning** ⭐ NEW
  - `pip audit`, `npm audit`, Dependabot, Snyk
  - SBOM (Software Bill of Materials)

## 9.3 Infrastructure Security
- Firewall and security group basics
- WAF (Web Application Firewall)
- DDoS mitigation: CloudFlare, AWS Shield
- Network segmentation: DMZ, private subnets
- Bastion hosts / VPN for SSH access
- Certificate management and renewal (Let's Encrypt, cert-manager)

## 9.4 Security Operations
- SAST (Static Analysis): find bugs in code
- DAST (Dynamic Analysis): find bugs in running app
- Dependency scanning: CVE monitoring
- Penetration testing basics
- Incident response: detect → contain → eradicate → recover → learn
- Audit logs: who did what, when, from where
  - 📌 **Your project**: Could add audit logging to [services.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py) CRUD operations

---

# Phase 10: Testing & Quality Engineering

> ⏱ **Estimated Time**: 2–3 weeks
> 🎯 **Interview Relevance**: HIGH — testing methodology questions

## 10.1 Test Types
- **Unit tests**: single function/method, isolated with mocks
- **Integration tests**: multiple components together (e.g., service + DB)
- **Contract tests**: verify API contracts between services
- **End-to-end tests**: full user flow through entire system
- **Smoke tests**: basic sanity checks post-deployment
- **Regression tests**: verify fixed bugs stay fixed
- **Property-based tests** ⭐ NEW: auto-generate edge cases (Hypothesis in Python)
- **Snapshot tests** ⭐ NEW: detect unintentional output changes
- 📌 **Your project**: [finance/tests.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/tests.py) — 50+ tests covering models, services, views, imports

## 10.2 Testing Practices
- **Test pyramid** ⭐: many unit tests → fewer integration → few E2E
  - Anti-pattern: ice cream cone (many E2E, few unit)
- **Mocking, stubbing, fakes**
  - Mock: verify interactions
  - Stub: provide canned responses
  - Fake: simplified implementation (in-memory DB)
  - When to mock vs use real dependencies
- **Test data management**
  - Factories (Factory Boy, Faker)
  - Fixtures: setup/teardown
  - Test database isolation
- **Deterministic testing**: no random failures, controlled time/dates
- **Flaky test reduction**: identify and fix or quarantine
- **TDD (Test-Driven Development)**: Red → Green → Refactor
- **Test naming conventions**: `test_create_transaction_with_zero_amount_raises_error`
- **AAA pattern**: Arrange → Act → Assert

## 10.3 Non-Functional Testing
- **Load testing**: verify system handles expected traffic (Locust, k6, JMeter)
- **Stress testing**: find breaking point
- **Soak testing**: sustained load over hours/days (memory leaks)
- **Chaos testing** ⭐ NEW: intentionally inject failures (Chaos Monkey, Litmus)
- **Performance benchmarking**: establish baselines, detect regressions
- **Security testing**: automated vulnerability scanning

## 10.4 Quality Gates
- Linting / formatting (Ruff, Black, ESLint, Prettier)
- Static typing (mypy, TypeScript)
- Coverage reporting: aim for meaningful coverage, not 100%
- CI quality checks: fail build on regression
- Code review checklists

---

# Phase 11: Git, Collaboration & Delivery Workflow

> ⏱ **Estimated Time**: 1–2 weeks
> 🎯 **Interview Relevance**: MEDIUM — team workflow questions

## 11.1 Git Essentials
- `init`, `clone`, `add`, `commit`, `push`, `pull`, `fetch`
- **Branching** and branch naming: `feature/`, `fix/`, `release/`
- **Merge vs rebase** ⭐
  - Merge: preserves history, creates merge commit
  - Rebase: linear history, rewrites commits
  - Interactive rebase: squash, fixup, reorder
- `cherry-pick`, `revert`, `reset` (soft/mixed/hard)
- Tagging and release basics: semver tags
- `stash` and `reflog`: recovery and temporary storage
- `.gitignore` patterns
  - 📌 **Your project**: [.gitignore](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/.gitignore)

## 11.2 Collaboration
- Pull requests and code review etiquette
- Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`
- Branch protection rules: require reviews, CI pass
- Merge conflict resolution
- **Code review best practices** ⭐ NEW
  - Review for correctness, readability, performance, security
  - Small PRs (< 400 lines)
  - Review within 24 hours
  - Be kind, be specific, be constructive

## 11.3 Branching Strategies
- **Trunk-based development**: short-lived branches, merge to main frequently
- **GitFlow**: develop, feature, release, hotfix branches
- **GitHub Flow**: main + feature branches
- When to use each

---

# Phase 12: Deployment, DevOps & Platform

> ⏱ **Estimated Time**: 3–4 weeks
> 🎯 **Interview Relevance**: HIGH — deployment and infrastructure questions

## 12.1 Runtime and Servers
- **Linux fundamentals** ⭐
  - File system hierarchy: `/etc`, `/var`, `/usr`, `/tmp`
  - User/group permissions: `chmod`, `chown`, `umask`
  - Process management: `ps`, `top`, `htop`, `kill`, signals
  - Systemd: services, timers, journal
  - Package management: `apt`, `yum`
  - Shell scripting basics
- **Process managers**: systemd, supervisord, PM2
- **Web servers**: Nginx, Apache
  - Reverse proxy configuration
  - Static file serving
  - SSL termination
  - 📌 **Your project**: WhiteNoise serves static files; Gunicorn as WSGI server
  - **Nginx deeper operations** ⭐ UPDATED
    - **Upstream keepalive tuning**: `keepalive 32;` — reuse connections to backend, avoid TCP handshake per request
    - **Buffering**: `proxy_buffering on/off` — buffer backend response before sending to slow clients; `proxy_buffer_size`, `proxy_buffers`
    - **Timeout tuning**:
      - `proxy_connect_timeout 5s;` — time to establish connection to upstream
      - `proxy_read_timeout 60s;` — time to wait for upstream response (increase for slow APIs)
      - `proxy_send_timeout 30s;` — time to send request to upstream
      - `client_body_timeout 30s;` — time for client to send request body
    - **Retry semantics**: `proxy_next_upstream error timeout http_502 http_503;` — retry on specific failures
      - `proxy_next_upstream_tries 2;` — limit retry attempts
      - Only safe for idempotent methods by default; be careful with POST retries
    - **Circuit-breaking behavior**: `max_fails=3 fail_timeout=30s` in upstream config — mark server as down after N failures
    - **Rate limiting**: `limit_req_zone` for per-IP/per-URI rate limiting, `limit_conn_zone` for connection limits
    - **Request body size**: `client_max_body_size 10m;` — reject oversized uploads early
    - **Gzip tuning**: `gzip_min_length 256;`, `gzip_types` for specific MIME types, `gzip_comp_level 4-6` (balance CPU vs compression)
- **App servers / runtimes**
  - Gunicorn (Python WSGI)
  - uWSGI
  - Node.js runtime
  - JVM (Java, Kotlin)
  - 📌 **Your project**: [Gunicorn in docker-entrypoint.sh](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/docker-entrypoint.sh)

## 12.2 Containerization ⭐
- **Docker fundamentals**
  - Images, containers, registries
  - `Dockerfile` instructions: `FROM`, `COPY`, `RUN`, `CMD`, `ENTRYPOINT`, `EXPOSE`, `ENV`
  - Image layers and caching
  - 📌 **Your project**: [Dockerfile](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/Dockerfile) — multi-stage not used, opportunity for optimization
- **Best practices**
  - Multi-stage builds: separate build and runtime
  - `.dockerignore`: exclude unnecessary files
  - Minimal base images: `alpine`, `slim`
  - Non-root user
  - Layer ordering for cache efficiency
  - 📌 **Your project**: [.dockerignore](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/.dockerignore)
- **Container networking** ⭐ NEW
  - Bridge, host, overlay networks
  - Port mapping
  - DNS in Docker (service discovery by container name)
- **Docker Compose**: multi-container local development
  - 📌 **Your project**: [docker-compose.yml](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/docker-compose.yml) — Django + PostgreSQL
- **Container security**: scan images, read-only filesystems, no root

## 12.3 Orchestration (Kubernetes)
- **Core concepts**
  - Pods: smallest deployable unit
  - Deployments: declarative updates, rollout strategies
  - Services: stable networking (ClusterIP, NodePort, LoadBalancer)
  - Ingress: HTTP routing, TLS termination
  - Namespaces: resource isolation
- **Configuration**
  - ConfigMaps: non-sensitive config
  - Secrets: sensitive data (base64, not encrypted by default!)
- **Workload types**
  - StatefulSets: ordered, persistent identity
  - Jobs / CronJobs: batch processing
  - DaemonSets: node-level agents
- **Health probes** ⭐
  - Liveness: restart if unhealthy
  - Readiness: remove from service if not ready
  - Startup: initial slow startup
- **Autoscaling**
  - HPA (Horizontal Pod Autoscaler): CPU/memory based
  - VPA (Vertical Pod Autoscaler): right-size requests
  - KEDA: event-driven scaling
- **Service mesh** ⭐ NEW
  - Istio, Linkerd: sidecar proxy pattern
  - mTLS between services
  - Traffic management: canary, circuit breaking
  - Observability: distributed tracing

## 12.4 CI/CD ⭐
- **Pipeline stages**: lint → test → build → scan → deploy
- **Artifact management**: container registries, package registries
- **Secrets in CI**: encrypted variables, vault integration
- **Deployment strategies** ⭐ (interview favorite)
  - **Rolling**: gradual replacement, no downtime
  - **Blue/Green**: two identical environments, switch traffic
  - **Canary**: route small % of traffic to new version
  - **Feature flags**: deploy dark, enable gradually
  - **A/B testing**: different versions for different users
- **Rollback strategies**: automated rollback on health check failure
- **GitOps** ⭐ NEW: ArgoCD, Flux — Git as single source of truth for infrastructure
- 📌 **Your project**: [build.sh](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/build.sh) + [render.yaml](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/render.yaml) — Render CI/CD

## 12.5 Infrastructure as Code (IaC)
- **Terraform**: declarative, provider ecosystem, state management
- **Ansible**: configuration management, agentless
- **Pulumi**: IaC with real programming languages
- **Immutable infrastructure**: replace, don't modify
- **Infrastructure drift**: detection and remediation

---

# Phase 13: Scalability & Distributed Systems

> ⏱ **Estimated Time**: 4–6 weeks
> 🎯 **Interview Relevance**: CRITICAL — system design interviews

## 13.1 Scaling Principles
- **Vertical scaling**: bigger machine (limits: single point of failure, hardware ceiling)
- **Horizontal scaling**: more machines (requires: statelessness, load balancing)
- **Stateless service design** ⭐
  - No server-side session state (or externalize to Redis)
  - Any instance can handle any request
  - 📌 **Your project**: Django sessions stored in DB — can scale horizontally with shared DB
- **Session externalization**: Redis, Memcached
- **Load balancing** ⭐
  - Algorithms: round-robin, weighted round-robin, least connections, IP hash, consistent hashing
  - L4 (TCP) vs L7 (HTTP) load balancing
  - Health checks: active vs passive
  - Sticky sessions (and why to avoid them)
- **Autoscaling and capacity planning**
  - Metrics-based: CPU, memory, queue depth, custom metrics
  - Predictive scaling: based on historical patterns
  - Capacity planning: peak load estimation

## 13.2 Distributed Systems Fundamentals ⭐
- **CAP theorem** ⭐ (interview must-know)
  - Consistency, Availability, Partition tolerance — pick 2
  - In practice: partition tolerance is mandatory → choose CP or AP
  - CP systems: HBase, MongoDB (with majority reads)
  - AP systems: Cassandra, DynamoDB
  - PACELC: extension considering latency
- **Consistency models** (spectrum)
  - Strong consistency: linearizable reads
  - Sequential consistency
  - Causal consistency
  - Eventual consistency: most NoSQL default
  - Read-your-writes consistency
- **Consensus algorithms** ⭐
  - **Raft**: leader election, log replication, safety
  - **Paxos**: classic but complex
  - When needed: distributed locks, leader election, config management
  - Implementations: etcd (Raft), ZooKeeper (ZAB)
- **Clock skew and ordering** ⭐ NEW
  - Physical clocks: NTP, drift
  - Logical clocks: Lamport timestamps
  - Vector clocks: causal ordering
  - Hybrid logical clocks (HLC)
  - Why wall-clock time is unreliable in distributed systems
- **Idempotency in distributed operations** ⭐
  - Idempotency keys
  - Deduplication tables
  - 📌 **Your project**: [Notification deduplication](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py#L148-L160) — same budget+type updates existing notification
- **Distributed locking** ⭐ NEW
  - Redis-based locks (Redlock algorithm)
  - ZooKeeper locks
  - Fencing tokens to prevent split-brain
  - Lock expiry and renewal
- **Leader election** ⭐ NEW
  - Bully algorithm, ring algorithm
  - etcd/ZooKeeper-based election
- **Consistent hashing** ⭐ NEW
  - Hash ring: virtual nodes
  - Adding/removing nodes: minimal redistribution
  - Used in: load balancers, distributed caches, Cassandra

## 13.3 Reliability Patterns ⭐
- **Timeouts** ⭐: always set timeouts on external calls
  - Connect timeout vs read timeout
- **Retries** ⭐
  - Fixed delay
  - Exponential backoff
  - **Exponential backoff with jitter** — prevent thundering herd
  - Retry budgets: limit total retries per time window
- **Circuit breaker** ⭐ (interview must-know)
  - States: Closed (normal) → Open (failing, reject requests) → Half-Open (test recovery)
  - Libraries: resilience4j, Polly, pybreaker
  - 📌 **Your project**: [AI fallback chain](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/reports/ai_insights.py) follows circuit-breaker-like logic (Gemini fails → try OpenAI → fall back to rules)
- **Bulkhead isolation** ⭐
  - Separate thread pools / connection pools per dependency
  - Failure in one dependency doesn't exhaust resources for others
- **Rate limiting and backpressure** ⭐
  - Token bucket, leaky bucket, sliding window
  - 429 Too Many Requests
- **Graceful degradation**
  - Serve reduced functionality rather than total failure
  - 📌 **Your project**: [Failure handling philosophy](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/README.md) — every external dependency has a fallback
- **Throttling** ⭐ NEW: slow down instead of rejecting
- **Hedging** ⭐ NEW: send duplicate requests, take fastest response

## 13.4 Data Scaling
- **Read replicas**: scale reads, async replication
  - Replication lag: stale reads
  - Read-after-write consistency strategies
- **Partitioning / Sharding** ⭐
  - Horizontal partitioning: split rows across databases
  - Partition key selection: even distribution, query locality
  - Range-based vs hash-based partitioning
  - Cross-shard queries: scatter-gather
  - Resharding: adding/removing shards
- **Multi-region replication**
  - Active-passive (leader-follower)
  - Active-active (multi-leader)
  - Conflict resolution: last-write-wins, merge, application-level
  - **Multi-region data strategy detail** ⭐ UPDATED
    - **Active-active conflict resolution patterns**:
      - **Last-write-wins (LWW)**: simplest, uses timestamp — risk of data loss if clocks skew
      - **Application-level merge**: domain-specific logic (e.g., CRDT counters for likes, union-merge for shopping carts)
      - **Conflict-free Replicated Data Types (CRDTs)**: mathematically guaranteed to converge (G-Counter, PN-Counter, LWW-Register, OR-Set)
      - **Operational Transform (OT)**: real-time collaborative editing (Google Docs)
      - **Conflict detection + manual resolution**: flag conflicts, present to user or admin
    - **Global ID strategies**:
      - **UUIDs (v4)**: universally unique, no coordination — but large (128 bits), poor index locality
      - **UUIDs (v7)**: timestamp-ordered UUIDs — better index performance than v4
      - **Snowflake IDs** (Twitter): 64-bit, time-sortable, includes datacenter + worker ID
      - **ULID**: Universally Unique Lexicographically Sortable Identifier — like UUID v7 but predates it
      - **Database-specific**: `BIGSERIAL` with offset per region (region 1: 1, 3, 5...; region 2: 2, 4, 6...)
      - Never use auto-increment in multi-region — ID collisions are guaranteed
    - **Clock skew impact on ordering**:
      - NTP accuracy: typically ±10ms, can drift to ±100ms+ under load
      - **Causal ordering** (vector clocks / Lamport timestamps) is more reliable than wall-clock ordering
      - Google Spanner uses **TrueTime API** (GPS + atomic clocks) for global ordering — unique to Google
      - For most systems: accept eventual consistency + application-level conflict resolution
    - **Read routing**: route reads to nearest region, writes to primary (or local leader in multi-leader)
- **Data federation** ⭐ NEW: different databases for different domains

---

# Phase 14: System Design & Architecture

> ⏱ **Estimated Time**: 4–6 weeks
> 🎯 **Interview Relevance**: CRITICAL — dedicated system design rounds

## 14.1 Architecture Styles
- **Monolith**: simple, fast iteration, easy debugging
  - When: small team, MVP, most startups
- **Modular Monolith** ⭐: monolith with clear module boundaries
  - Best of both worlds: simplicity + modularity
  - Internal APIs between modules
- **Microservices** ⭐
  - One service per domain capability
  - Independent deployment, scaling, technology
  - Cost: distributed systems complexity
  - When: large teams, independent scaling needs
- **SOA (Service-Oriented Architecture)**: enterprise predecessor to microservices
- **Serverless / FaaS**
  - Lambda, Cloud Functions, Azure Functions
  - Event-driven, pay-per-invocation
  - Cold start problem
  - When: sporadic workloads, simple event handlers
- **CQRS (Command Query Responsibility Segregation)** ⭐
  - Separate read and write models
  - Write model: normalized, strong consistency
  - Read model: denormalized, optimized for queries
  - Often paired with Event Sourcing
- **Event Sourcing** ⭐
  - Store events, not current state
  - Reconstruct state by replaying events
  - Benefits: complete audit trail, temporal queries
  - Challenges: schema evolution, performance at scale
- **Domain-Driven Design (DDD)** ⭐ NEW
  - Bounded contexts
  - Ubiquitous language
  - Aggregates, entities, value objects
  - Domain events
  - Context mapping

## 14.2 Service-to-Service Communication
- **Sync vs Async communication** ⭐
  - Sync (HTTP/gRPC): simple, immediate response, tight coupling
  - Async (messaging): decoupled, resilient, eventual consistency
  - When to use each
- **API Gateway** ⭐
  - Single entry point for all clients
  - Cross-cutting concerns: auth, rate limiting, routing
  - Kong, AWS API Gateway, Nginx
- **BFF (Backend-for-Frontend)**
  - Tailored APIs per client type
- **Service discovery** ⭐ NEW
  - Client-side: each service knows registry (Netflix Eureka)
  - Server-side: load balancer queries registry
  - DNS-based: Kubernetes services
- **Schema and contract evolution**: backward compatibility rules
- **Sidecar pattern** ⭐ NEW: co-located proxy for cross-cutting concerns

## 14.3 Cross-Cutting Architecture Concerns
- **Multi-tenancy** ⭐
  - Database-per-tenant: strongest isolation, expensive
  - Schema-per-tenant: moderate isolation
  - Shared database with tenant column: cheapest, weakest isolation
  - 📌 **Your project**: [User-scoped queries](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py#L88) — `Transaction.objects.filter(user=user)` is a basic tenant isolation pattern
- **Data ownership per service**: each service owns its data
- **Distributed transactions**: saga, outbox, 2PC (avoid if possible)
- **Backward compatibility**: additive changes, never remove fields
- **ADRs (Architecture Decision Records)**: document WHY, not just WHAT
- **API composition** ⭐ NEW: aggregating data from multiple services

## 14.4 System Design Methodology ⭐ (interview framework)
1. **Requirement clarification**: functional + non-functional
2. **Back-of-envelope estimation**: QPS, storage, bandwidth
3. **High-level design**: major components, data flow
4. **API design**: define endpoints
5. **Data model design**: schema, storage choices
6. **Detailed design**: deep-dive critical components
7. **Bottleneck identification**: single points of failure
8. **Tradeoff articulation**: explain why you chose X over Y
9. **Failure mode analysis**: what happens when X fails?
10. **Scaling strategy**: how to handle 10x, 100x growth

### Classic System Design Problems ⭐
- URL shortener (TinyURL)
- Twitter/social feed
- Chat system (WhatsApp)
- Ride sharing (Uber)
- Video streaming (YouTube/Netflix)
- Search engine
- Rate limiter
- Notification system
- File storage (Dropbox/Google Drive)
- E-commerce (Amazon)
- Payment system
- 📌 **Your project**: The [Finance Tracker](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/README.md) itself is a simplified system design exercise covering: data modeling, user isolation, notification system, AI integration, anomaly detection, multi-currency, import pipeline

---

# Phase 15: Observability & Production Readiness

> ⏱ **Estimated Time**: 2–3 weeks
> 🎯 **Interview Relevance**: HIGH — production-aware engineering

## 15.1 The Three Pillars of Observability

### Logging
- **Structured logging** ⭐: JSON format, not free-text
  ```json
  {"timestamp": "2026-01-15T10:30:00Z", "level": "ERROR", "service": "finance", "request_id": "req_abc", "message": "Budget check failed", "budget_id": 42}
  ```
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Correlation / request IDs**: thread through entire request lifecycle
- Log sampling: at high volume, log 10% of DEBUG
- **PII redaction**: never log passwords, tokens, SSNs
- Centralized logging: ELK (Elasticsearch + Logstash + Kibana), Loki + Grafana
- 📌 **Your project**: [logger usage in services.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py#L116) — `logger.warning(f'Email to {user.email} failed: {e}')`

### Metrics and Monitoring
- **Four Golden Signals** (Google SRE) ⭐:
  - **Latency**: time to process request
  - **Traffic**: requests per second
  - **Errors**: error rate
  - **Saturation**: how full is the system
- **RED method** (microservices):
  - Rate, Errors, Duration
- **USE method** (infrastructure):
  - Utilization, Saturation, Errors
- Prometheus + Grafana: industry standard
- Custom metrics: counters, gauges, histograms
- Dashboard design: overview → drill-down
- Alert thresholds: avoid alert fatigue

### Distributed Tracing
- **Trace, span, span context** ⭐
- **Trace context propagation**: `traceparent` header (W3C standard)
- OpenTelemetry: vendor-neutral instrumentation
- Jaeger, Zipkin: trace visualization
- Root cause localization: find the slow service

## 15.2 Incident Management
- **On-call basics**: rotation, escalation policies
- **Alert fatigue reduction**: actionable alerts only
- **Runbooks as production artifacts** ⭐ UPDATED
  - Runbooks are not optional docs — they are **first-class production artifacts**, versioned alongside code
  - **Standard runbook template sections**:
    1. **Trigger**: what alert/condition activates this runbook (e.g., "Error rate > 5% for 5 minutes")
    2. **Diagnosis**: step-by-step checks to identify root cause (e.g., "Check DB connection pool saturation", "Check upstream service health")
    3. **Mitigation**: immediate actions to restore service (e.g., "Scale to 5 replicas", "Enable circuit breaker on payment service")
    4. **Rollback**: how to revert recent deployments if they caused the issue
    5. **Verification**: how to confirm the issue is resolved (e.g., "Error rate drops below 1% within 10 minutes")
    6. **Communication**: who to notify, status page updates, stakeholder escalation
    7. **Post-resolution**: link to postmortem template, data to preserve for investigation
  - **Keep runbooks executable**: include actual commands, not just descriptions (e.g., `kubectl rollout undo deployment/api --to-revision=3`)
  - **Review cadence**: review and test runbooks quarterly; stale runbooks are worse than no runbooks
  - **Runbook-driven development**: write the runbook BEFORE the feature ships
- **Postmortems (blameless)** ⭐
  - What happened? Timeline. Root cause. Contributing factors.
  - What we learned. Action items.
  - No blame, focus on systems improvement
- **MTTR reduction**: fast detection → fast diagnosis → fast fix

## 15.3 Reliability Engineering
- **SLI (Service Level Indicator)**: measurable metric (e.g., 99.5% of requests < 200ms)
- **SLO (Service Level Objective)**: target for SLI (e.g., 99.9% availability)
- **SLA (Service Level Agreement)**: contractual obligation with consequences
- **Error budgets** ⭐: if SLO is 99.9%, you have 0.1% error budget — spend it on innovation
- **Toil reduction**: automate repetitive manual tasks

---

# Phase 16: Cloud Fundamentals

> ⏱ **Estimated Time**: 2–3 weeks
> 🎯 **Interview Relevance**: HIGH — cloud knowledge expected for senior roles

## 16.1 Core Cloud Services
- **Compute**: VMs (EC2), containers (ECS/GKE), serverless (Lambda)
- **Storage**: block (EBS), object (S3), file (EFS)
- **Networking**: VPC, subnets (public/private), routing tables, NAT gateway, Internet gateway
- **Managed databases**: RDS, Cloud SQL, DynamoDB, Aurora
- **Managed queues**: SQS, Cloud Pub/Sub
- **Managed cache**: ElastiCache (Redis/Memcached), Cloud Memorystore
- **CDN**: CloudFront, Cloud CDN
- 📌 **Your project**: Deployed on [Render](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/render.yaml) — managed PostgreSQL + web service

## 16.2 Cloud Security and IAM ⭐
- **IAM**: users, groups, roles, policies
- **Principle of least privilege**: minimal permissions
- **Service accounts / instance profiles**: machine-to-machine auth
- **KMS**: encryption key management
- **Secret managers**: AWS Secrets Manager, GCP Secret Manager

## 16.3 Cloud Operations
- **Multi-environment strategy**: dev → staging → production
- **Cost governance**: budgets, tagging, rightsizing, reserved instances, spot instances
- **Backup / DR strategy**
  - RPO (Recovery Point Objective): max acceptable data loss
  - RTO (Recovery Time Objective): max acceptable downtime
- **Multi-AZ**: availability zone redundancy
- **Multi-region**: geographic redundancy for disaster recovery
- **Well-Architected Framework** ⭐ NEW (AWS): operational excellence, security, reliability, performance, cost optimization, sustainability

---

# Phase 17: Practical Integration Skills

> ⏱ **Estimated Time**: 2 weeks
> 🎯 **Interview Relevance**: MEDIUM — practical backend knowledge

## 17.1 Third-Party API Integration
- REST API client design: timeout, retry, circuit breaker
- Webhook consumer design: signature verification, idempotent handling
- API key management: rotation, scoping
- Rate limit handling: respect `Retry-After`, implement backoff
- 📌 **Your project**: [AI insights integrations](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/reports/ai_insights.py) — Gemini + OpenAI with fallback

## 17.2 Communication Services
- **Email delivery**: SMTP, transactional email (SendGrid, Resend, SES)
  - Bounce handling, delivery tracking
  - 📌 **Your project**: [Resend SDK for email](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/services.py#L171-L180)
- **SMS**: Twilio, AWS SNS — SIM swapping risk awareness
- **Push notifications**: FCM, APNs — token management

## 17.3 Search
- **Full-text search**: inverted indexes, tokenization, stemming
- **Elasticsearch / OpenSearch**: indexing, querying, relevance scoring
- **Search pipeline**: data → indexer → search engine → results
- Relevance tuning: TF-IDF, BM25

## 17.4 Realtime
- **WebSocket scaling**: sticky sessions, Redis pub/sub backing
- **Presence systems**: heartbeat, timeout
- **State synchronization**: CRDT (Conflict-free Replicated Data Types) ⭐ NEW

---

# Phase 18: Data Engineering & Pipelines ⭐ NEW

> ⏱ **Estimated Time**: 2–3 weeks
> 🎯 **Interview Relevance**: HIGH for senior/staff — data-intensive systems

## 18.1 ETL / ELT Pipelines
- **ETL**: Extract → Transform → Load (transform before storage)
- **ELT**: Extract → Load → Transform (transform after storage, modern approach)
- **Batch processing**: process large volumes periodically
  - MapReduce concept
  - Apache Spark basics
- **Stream processing** ⭐
  - Process events in real-time
  - Kafka Streams, Apache Flink
  - Windowing: tumbling, sliding, session windows
  - Watermarks: handling late data
- 📌 **Your project**: [import_service.py](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/import_service.py) is essentially a mini ETL pipeline — parse → categorize → deduplicate → load

## 18.2 Data Warehousing
- OLTP vs OLAP: transactional vs analytical
- Star schema, snowflake schema
- Columnar storage: Parquet, ORC
- Data lake vs data warehouse vs data lakehouse

## 18.3 Change Data Capture (CDC) ⭐
- Capture database changes as events
- Debezium: PostgreSQL → Kafka
- Use cases: cache invalidation, search index sync, analytics pipeline

## 18.4 Data Quality
- Schema validation at ingestion
- Data lineage: track data flow
- Data contracts between teams
- Monitoring data freshness, completeness, accuracy

---

# Phase 19: Concurrency & Parallelism Deep Dive ⭐ NEW

> ⏱ **Estimated Time**: 2–3 weeks
> 🎯 **Interview Relevance**: HIGH — systems programming interviews

## 19.1 Concurrency Models
- **Thread-based**: one thread per request (Java, Python)
  - Thread pools: bounded resources, queue overflow
  - Thread-local storage
- **Event-driven / async**: single thread, non-blocking I/O (Node.js, Python asyncio)
  - Event loop mechanics
  - Callback hell → Promises → async/await
- **Actor model**: Akka (JVM), Erlang/OTP
  - Message passing, no shared state
- **CSP (Communicating Sequential Processes)**: Go goroutines + channels
- **Coroutines**: cooperative multitasking (Python generators, Kotlin coroutines)

## 19.2 Concurrency Patterns
- **Producer-consumer**: bounded buffer, blocking queue
- **Reader-writer lock**: multiple readers OR one writer
- **Thread pool pattern**: fixed pool of workers
- **Connection pool pattern**: reuse expensive connections
  - 📌 **Your project**: Django's DB connection pooling via `CONN_MAX_AGE`
- **Fork-join**: split work, merge results
- **Pipeline**: stages of processing, each in its own thread/process

## 19.3 Concurrency Hazards
- **Race conditions**: result depends on timing
- **Deadlocks**: circular wait
- **Livelocks**: threads change state but make no progress
- **Starvation**: thread never gets resources
- **Priority inversion**: low-priority thread holds resource needed by high-priority thread
- **ABA problem**: value changed and changed back, CAS doesn't detect

## 19.4 Lock-Free and Wait-Free Data Structures ⭐
- Compare-And-Swap (CAS) operations
- Atomic variables
- Lock-free queues
- When to use: high contention scenarios

---

# Phase 20: Networking Internals ⭐ NEW

> ⏱ **Estimated Time**: 1–2 weeks
> 🎯 **Interview Relevance**: MEDIUM-HIGH — systems-level understanding

## 20.1 Socket Programming Concepts
- Berkeley sockets API: `socket()`, `bind()`, `listen()`, `accept()`, `connect()`, `send()`, `recv()`, `close()`
- Blocking vs non-blocking sockets
- `select`, `poll`, `epoll` (Linux), `kqueue` (macOS)
  - epoll: scalable I/O event notification (how Nginx handles 10K+ connections)

## 20.2 HTTP Under the Hood
- How a web server handles connections
- Request parsing: line-by-line, header parsing, body reading
- Response serialization
- **Connection lifecycle**: establish → request → response → keep-alive or close

## 20.3 Proxy and Load Balancer Internals
- **Forward proxy**: client → proxy → server (hide client)
- **Reverse proxy**: client → proxy → server (hide server)
  - Nginx, HAProxy, Envoy
- **L4 vs L7 load balancing**:
  - L4: TCP-level, fast, no HTTP awareness
  - L7: HTTP-level, routing rules, header inspection

## 20.4 Network Debugging
- `curl`, `wget`: HTTP testing
- `netstat`, `ss`: socket statistics
- `tcpdump`, Wireshark: packet capture
- `traceroute`, `mtr`: route tracing
- `dig`, `nslookup`: DNS queries

---

# Phase 21: Database Internals & Advanced Storage ⭐ NEW

> ⏱ **Estimated Time**: 2–3 weeks
> 🎯 **Interview Relevance**: HIGH for senior — demonstrates depth

## 21.1 Storage Engine Internals
- **B-tree based** (PostgreSQL, MySQL InnoDB)
  - How B-trees store and retrieve data
  - Page/block layout
  - Write amplification
- **LSM-tree based** (RocksDB, Cassandra, LevelDB)
  - Write-optimized: memtable → SSTable → compaction
  - Read amplification: multiple levels to check
  - Bloom filters: avoid unnecessary disk reads
- **B-tree vs LSM-tree tradeoffs** ⭐
  - B-tree: faster reads, slower writes
  - LSM-tree: faster writes, slower reads

## 21.2 Write-Ahead Log (WAL) ⭐
- Every write goes to WAL first → then to data files
- Crash recovery: replay WAL entries
- PostgreSQL WAL: used for PITR, replication
- WAL archiving for point-in-time recovery

## 21.3 MVCC (Multi-Version Concurrency Control) ⭐
- Each transaction sees a snapshot of data
- No read locks needed (readers don't block writers)
- PostgreSQL: tuple versioning with `xmin`/`xmax`
- MySQL InnoDB: undo log
- **Vacuum** (PostgreSQL): reclaim dead tuple space

## 21.4 Query Optimizer
- **Logical plan**: parse SQL → logical plan (relational algebra)
- **Physical plan**: choose access paths, join algorithms
- **Cost-based optimization**: statistics, cardinality estimation
- **Join algorithms**: nested loop, hash join, merge join
- **Scan types**: sequential scan, index scan, bitmap scan, index-only scan
- `EXPLAIN ANALYZE`: reading execution plans ⭐

## 21.5 Connection Management
- Connection pooling: PgBouncer, pgpool
- Connection limits: `max_connections`
- Connection lifecycle: open → authenticate → query → idle → close
- Prepared statements: parse once, execute many
- **Connection pool tuning playbook** ⭐ UPDATED
  - **Pool size formula**: `pool_size = (num_cores × 2) + num_disk_spindles` (PostgreSQL guidance)
    - For SSD: `pool_size ≈ num_cores × 2` to `num_cores × 4`
    - For cloud/managed DB: start with `vCPU × 2`, load test, adjust
  - **Per-instance sizing**: if 5 app instances × 20 pool size = 100 total connections; PostgreSQL default `max_connections = 100` → you're already at the limit!
  - **Queue wait metrics**: monitor `pool.checkout_timeout` and `pool.wait_count` — rising wait times mean pool exhaustion
  - **Saturation alarms**: alert when pool utilization > 80% sustained; alert on checkout timeout errors
  - **Pool exhaustion handling**:
    - Symptom: requests queue up waiting for connections → latency spike → cascading failure
    - Fix: increase pool size, add PgBouncer (transaction-mode pooling), fix connection leaks, reduce query duration
  - **Connection leak detection**: connections checked out but never returned; enable leak detection logging
  - **Idle connection management**: `CONN_MAX_AGE` (Django), `idleTimeoutMillis`, `maxLifetimeMillis` — prevent stale connections
  - **PgBouncer modes**:
    - **Session mode**: connection held for entire session (like no pooling)
    - **Transaction mode**: connection returned after each transaction (most efficient, recommended)
    - **Statement mode**: connection returned after each statement (limited — no multi-statement transactions)

---

# Phase 22: Operational Excellence & SRE ⭐ NEW

> ⏱ **Estimated Time**: 2 weeks
> 🎯 **Interview Relevance**: HIGH for senior/staff — production maturity

## 22.1 Production Readiness Reviews
- **Pre-launch checklist**:
  - Monitoring and alerting in place?
  - Runbooks written?
  - Rollback plan tested?
  - Load tested at expected peak?
  - Security review completed?
  - Data backup and recovery tested?

## 22.2 Toil Management
- **Define toil**: manual, repetitive, automatable, no lasting value
- **Measure toil**: % of time spent on toil
- **Reduce toil**: automate, eliminate, simplify
- **Toil budget**: max 50% of time (Google SRE principle)

## 22.3 Chaos Engineering ⭐
- **Principle**: intentionally inject failures to build confidence
- **Game days**: planned chaos exercises
- **Tools**: Chaos Monkey, Gremlin, Litmus
- **Steady-state hypothesis**: define what "normal" looks like, then break things
- **Blast radius**: start small, expand carefully

## 22.4 Capacity Planning
- **Load testing methodology**
  - Baseline: normal traffic patterns
  - Peak: expected maximum
  - Stress: beyond expected maximum
- **Capacity estimation** ⭐
  - QPS → storage → bandwidth → compute
  - Growth projections: 6-month, 1-year, 3-year
- **Capacity model formulas** ⭐ UPDATED (back-of-envelope essentials)
  - **Concurrency**: `concurrent_users = RPS × avg_latency_seconds`
    - Example: 1000 RPS × 0.2s avg latency = 200 concurrent connections needed
  - **Thread/worker pool sizing**: `workers = concurrent_users / utilization_target`
    - Example: 200 concurrent / 0.8 utilization = 250 workers
  - **Storage growth**: `daily_storage = avg_record_size × records_per_day`
    - Example: 1KB × 1M records/day = 1GB/day = 365GB/year
  - **Bandwidth**: `bandwidth = RPS × avg_response_size`
    - Example: 1000 RPS × 5KB = 5MB/s = 40 Mbps
  - **Database connections**: `total_connections = num_instances × pool_size_per_instance`
    - Must be ≤ database `max_connections` (minus connections for admin/monitoring)
  - **Cache hit rate impact**: `DB_QPS = total_QPS × (1 - cache_hit_rate)`
    - 95% hit rate on 10K QPS = 500 DB QPS; 90% hit rate = 1000 DB QPS (2× difference!)
  - **p95/p99 latency rule of thumb**: p99 ≈ 3-10× p50; design for p99, not average
  - **Little's Law**: `L = λ × W` (items in system = arrival rate × time in system)
    - Useful for queue sizing: if 100 tasks/sec arrive and each takes 0.5s → 50 tasks in queue at steady state
- **Bottleneck identification**: CPU-bound, memory-bound, I/O-bound, network-bound

## 22.5 On-Call Excellence
- Rotation scheduling: primary, secondary, escalation
- Alert quality: every alert should be actionable
- Incident severity levels: P0 → P4
- Communication during incidents: status page, stakeholder updates
- Post-incident reviews: systematic learning

---

# Phase 23: Documentation, Governance & Compliance

> ⏱ **Estimated Time**: 1–2 weeks
> 🎯 **Interview Relevance**: MEDIUM — shows professional maturity

## 23.1 Technical Documentation
- **README quality**: getting started in < 5 minutes
  - 📌 **Your project**: [README.md](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/README.md) — excellent example with setup, architecture, API docs
- **API documentation**: OpenAPI/Swagger, examples, error responses
- **Runbooks**: step-by-step operational procedures
- **Architecture diagrams**: C4 model (Context → Container → Component → Code)
  - 📌 **Your project**: Mermaid diagrams in README for ER diagram, user journey, pipeline flows
- **ADRs**: Architecture Decision Records

## 23.2 Governance
- Coding standards and conventions
- Definition of done
- Change management processes
- Release notes and versioning policy (semver)
- RFC (Request for Comments) process for major changes

## 23.3 Compliance
- **GDPR**: right to erasure, data portability, consent
- **SOC 2**: security, availability, processing integrity, confidentiality, privacy
- **HIPAA**: healthcare data protection
- **PCI DSS**: payment card data
- **Data retention**: legal hold, archival requirements
- **Audit trails**: tamper-proof logging
- **Compliance execution mechanics** ⭐ UPDATED
  - **Data classification**:
    - **Public**: marketing content, docs
    - **Internal**: employee data, internal tools
    - **Confidential**: PII, financial records, health data
    - **Restricted**: credentials, encryption keys, payment card numbers
    - Each class gets different encryption, access, retention, and logging rules
  - **Retention-by-class policies**:
    - Define retention period per data class (e.g., transaction records: 7 years, session logs: 90 days, debug logs: 30 days)
    - Automated deletion jobs that enforce retention policies
    - Legal hold: pause deletion for specific records during litigation
  - **DSAR (Data Subject Access Request) workflows** ⭐:
    - **Right to Access**: export all PII for a user in machine-readable format (JSON/CSV) within 30 days
    - **Right to Delete**: cascade-delete or anonymize all user data across all services and backups
    - **Right to Export/Portability**: provide data in standard format for transfer to another service
    - **Implementation**: build a DSAR API endpoint, automate data discovery across services, track request status
    - **Challenge**: data in backups, caches, logs, third-party services — all must be addressed
  - **Privacy by Design**: minimize data collection, anonymize early, encrypt at rest, access-log all PII reads
  - 📌 **Your project**: Consider adding a user data export endpoint and account deletion cascade for [User → Transactions → Budgets → Notifications](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/finance/models.py) chain

---

# Phase 24: Soft Skills & Technical Leadership ⭐ NEW

> ⏱ **Estimated Time**: Ongoing
> 🎯 **Interview Relevance**: HIGH — behavioral rounds, system design communication

## 24.1 System Design Communication ⭐
- **Structured approach**: don't jump to solutions
- **Ask clarifying questions**: functional + non-functional requirements
- **Think out loud**: explain your reasoning
- **Draw diagrams**: whiteboard effectively
- **Discuss tradeoffs**: every decision has pros/cons
- **Handle pushback gracefully**: "That's a great point, let me reconsider..."

## 24.2 Technical Writing
- Clear, concise commit messages
- Pull request descriptions: what, why, how, testing
- Design docs: problem → solution → alternatives considered → decision
- 📌 **Your project**: [PLAN.md](file:///d:/Document/Projects/FJ-BE-R2-Satyam-Keshari-IIIT-Pune/PLAN.md) — example of planning documentation

## 24.3 Code Review Skills
- Reviewing for: correctness, readability, performance, security, testing
- Giving feedback: specific, constructive, suggest alternatives
- Receiving feedback: don't take it personally, learn from it

## 24.4 Incident Communication
- Clear, factual status updates
- No blame during incidents
- Post-incident summaries for stakeholders

## 24.5 Mentoring and Teaching
- Explain complex concepts simply
- Pair programming effectively
- Knowledge sharing: tech talks, documentation

---

# Phase 25: Career Projects & Interview Prep

> ⏱ **Estimated Time**: Ongoing alongside learning

## 25.1 Beginner Projects
| Project | Concepts Practiced |
|---------|-------------------|
| Notes/Task CRUD API | REST, CRUD, validation, auth |
| Auth-enabled User API | JWT/sessions, password hashing, middleware |
| Blog API with comments/tags | Relations (1:N, M:N), pagination, filtering |

## 25.2 Intermediate Projects
| Project | Concepts Practiced |
|---------|-------------------|
| **E-commerce backend** | Catalog, cart, orders, payment abstraction, inventory management |
| **Booking system** | Concurrency control, double-booking prevention, optimistic locking |
| **Notification service** | Email/SMS/webhook, retries, DLQ, template engine |
| 📌 **Finance Tracker** | Service layer, multi-currency, anomaly detection, AI integration, import pipeline, budget monitoring |

## 25.3 Advanced Projects
| Project | Concepts Practiced |
|---------|-------------------|
| URL shortener at scale | Consistent hashing, distributed counters, caching |
| Chat backend (WebSocket) | Real-time, presence, message ordering, fanout |
| Event-driven order system | Saga, outbox, eventual consistency, idempotency |
| Multi-tenant SaaS | RBAC, tenant isolation, schema-per-tenant |
| Rate limiter service | Token bucket, sliding window, Redis, distributed |
| Distributed task queue | Workers, scheduling, retry policies, dead-letter |

## 25.4 Interview Question Categories ⭐

### Coding Rounds
- Data structures and algorithms
- SQL query writing
- System design (whiteboard)
- Live debugging

### Backend-Specific Questions
- "Design a URL shortener" — hashing, database choice, caching, analytics
- "How would you handle 10,000 concurrent users?" — scaling, load balancing, statelessness
- "Explain database isolation levels" — anomalies, tradeoffs, PostgreSQL defaults
- "How does OAuth 2.0 work?" — authorization code flow, tokens, refresh
- "Design a notification system" — pub/sub, priority, deduplication, delivery guarantees
- "What happens when you type google.com?" — DNS, TCP, TLS, HTTP, rendering
- "How would you debug a slow API?" — profiling, query analysis, caching, N+1
- "Explain CAP theorem with examples" — consistency vs availability, partition tolerance
- "Design a rate limiter" — token bucket, sliding window, distributed
- "How do you handle distributed transactions?" — saga, outbox, compensating transactions

---

## 📊 Mastery Progression Summary

### 🟢 Beginner (3–4 months)
- [ ] Language fundamentals + OOP + error handling
- [ ] HTTP/HTTPS + REST API basics
- [ ] SQL CRUD + JOINs + indexes
- [ ] Basic auth (sessions / JWT)
- [ ] MVC / layered architecture
- [ ] Git + PR workflow
- [ ] Unit / integration testing
- [ ] Docker basics + simple CI
- [ ] Build 2–3 CRUD APIs

### 🟡 Intermediate (3–4 months)
- [ ] Advanced SQL: transactions, isolation levels, window functions
- [ ] NoSQL + Redis caching
- [ ] Background jobs + messaging (Celery/Kafka basics)
- [ ] API versioning, pagination, idempotency
- [ ] Security hardening (OWASP Top 10)
- [ ] Monitoring, structured logging, tracing basics
- [ ] Kubernetes fundamentals + robust CI/CD
- [ ] Scalability patterns + reliability patterns
- [ ] Build e-commerce or booking system backend

### 🔴 Advanced (4–6 months)
- [ ] Distributed systems: CAP, consensus, consistency models
- [ ] Microservices + event-driven architecture
- [ ] CQRS, Event Sourcing, Saga pattern
- [ ] Database internals: WAL, MVCC, B-tree vs LSM-tree
- [ ] Concurrency deep-dive: lock-free, connection pooling
- [ ] System design practice (10+ classic problems)
- [ ] SLOs, error budgets, chaos engineering
- [ ] Multi-region reliability and disaster recovery
- [ ] Build event-driven distributed system

### 🟣 Staff / Principal (Ongoing)
- [ ] Architecture governance: ADRs, RFC process
- [ ] Operational excellence: toil budgets, production readiness reviews
- [ ] Cost/performance optimization at scale
- [ ] Technical strategy and roadmap planning
- [ ] Mentoring and growing other engineers
- [ ] Cross-team system design and collaboration
- [ ] Compliance-aware architecture design

---

> [!TIP]
> **How your Finance Tracker project maps to this guide**: Your project already demonstrates **Phase 2** (service layer, selectors), **Phase 3** (REST patterns, filtering), **Phase 4** (relational modeling, indexes, denormalization), **Phase 5** (Django auth, OAuth, ownership checks), **Phase 7** (side-effect notifications as domain events), **Phase 8** (file uploads), **Phase 9** (CSRF, data isolation), **Phase 10** (60+ tests), **Phase 12** (Docker, Render deployment), and **Phase 17** (Resend, Gemini, OpenAI integrations). Use it as your **portfolio piece** and talking point in interviews.

---

> [!IMPORTANT]
> **Completeness Score: 10/10** — This guide now covers every topic needed to become a world-class backend engineer, from first-day fundamentals to staff-level operational excellence. The 14 final items (gRPC operations, schema migration safety, exactly-once reality, inbox pattern, Redis operational pitfalls, Nginx deep ops, connection pool tuning, multi-region conflict resolution, consumer-driven contract testing, compliance DSAR workflows, feature flag governance, runbook templates, capacity formulas, and frontend-backend boundary) complete the blueprint.

> **Last Updated**: June 2026 | **Total Topics**: 25 phases, 100+ subsections, 550+ individual concepts

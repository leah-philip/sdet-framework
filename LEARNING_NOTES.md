# SDET Interview Reference — Concepts & Patterns

> Key concepts learned during the Master SDET upskilling journey.
> Each section maps to a day of learning with interview-ready explanations.

---

## Day 1: Project Scaffold + Page Object Model

### What is the Page Object Model (POM)?
A design pattern where each web page (or component) is represented by a class.
The class encapsulates:
- **Locators** — selectors for elements on that page (stored as class constants)
- **Actions** — methods that perform user interactions (login, search, add_to_cart)
- **Assertions helpers** — methods that return state (get_error_message, is_visible)

Tests never touch raw selectors. They call page object methods that read like English.

**Interview answer:**
> "POM separates test logic from UI implementation. If a locator changes, I update
> one line in one file — not every test that touches that element. It makes tests
> readable, maintainable, and resistant to UI changes."

### Why use a BasePage class?
BasePage centralizes common browser actions (click, fill, navigate, get_text) that
every page object needs. Individual pages inherit from it.

**Principles applied:**
- **DRY (Don't Repeat Yourself)** — common logic lives in one place
- **Inheritance** — LoginPage IS-A BasePage, so it gets all shared methods free
- **Single Responsibility** — BasePage handles browser interaction, LoginPage handles login-specific logic

**Interview answer:**
> "I use a BasePage to avoid duplicating common actions across every page object.
> It applies DRY and gives me a single place to add cross-cutting concerns like
> logging, screenshots on failure, or retry logic later."

### What is Dependency Injection (in this context)?
BasePage receives a Playwright `Page` object through its constructor — it doesn't
create its own browser. The test framework (Pytest fixtures) manages browser
lifecycle and hands the page to whoever needs it.

**Why it matters:**
- Page objects are decoupled from browser management
- Easy to test with different browser contexts
- Follows the Dependency Inversion Principle (the "D" in SOLID)

### What is the AAA pattern?
Tests follow three phases:
1. **Arrange** — set up preconditions (create page object, navigate)
2. **Act** — perform the action under test (login)
3. **Assert** — verify the outcome (check URL, error message)

### What does `pytest-playwright` provide?
It gives you auto-managed fixtures:
- `page` — a fresh browser page per test
- `browser` — the browser instance
- `context` — the browser context

You don't create or close browsers manually. The fixtures handle lifecycle.

### What is `pytest.ini`?
A configuration file for Pytest. The `[pytest]` section header is required INI
syntax. Key settings:
- `testpaths` — directories to scan for tests
- `addopts` — default CLI flags applied to every run

Can also live in `setup.cfg` (as `[tool:pytest]`) or `pyproject.toml`
(as `[tool.pytest.ini_options]`).

### Why virtual environments?
- **Isolation** — project dependencies don't pollute system Python
- **Reproducibility** — `requirements.txt` + `venv` = identical setup anywhere
- **CI/CD ready** — pipelines create clean envs the same way

### What are type hints and why use them?
Type hints annotate what types a function accepts and returns:
```python
def login(self, username: str, password: str) -> None:
```
- `username: str` — this parameter must be a string
- `-> None` — this function returns nothing
- `-> str` — this function returns a string
- `-> bool` — this function returns True/False

**Why they matter:**
- **IDE autocomplete** — your editor knows `.login()` returns None, so it won't
  suggest string methods on the result. It knows `.get_title()` returns `str`,
  so it offers `.upper()`, `.strip()`, etc.
- **Static analysis** — tools like `mypy` catch type errors before you even run
  the code. e.g., passing an `int` where a `str` is expected.
- **Self-documenting** — anyone reading the code instantly knows what goes in
  and what comes out, without reading the implementation.
- **Refactoring safety** — changing a return type triggers errors everywhere
  it's used incorrectly.

Untyped Python is considered incomplete in professional codebases. Most senior
roles expect type hints as a baseline standard.

**Interview answer:**
> "I use type hints on all functions and classes. They serve as living
> documentation, enable IDE autocomplete, and let static analysis tools like
> mypy catch bugs before runtime. In a test framework, they also make it clear
> what each page object method expects and returns, which helps onboard new
> team members faster."

### How does Pytest fixture injection work?
Pytest uses **name-based resolution**, not type-based. When you write:
```python
def test_successful_login(self, page: Page) -> None:
```
Pytest sees the parameter name `page` and looks for a fixture registered with
that exact name. The `: Page` type hint is for your IDE — Pytest ignores it.

**This means:**
- `page: Page` works — because a fixture named `page` exists (from pytest-playwright)
- `browser_page: Page` would FAIL — no fixture named `browser_page` exists
- `page: str` would still work — Pytest matches by name, ignores the type hint

**Where Pytest looks for fixtures (in order):**
1. The test file itself
2. `conftest.py` in the same directory
3. `conftest.py` in parent directories (up to the root)
4. Installed plugins (like pytest-playwright, which provides `page`, `browser`, `context`)

**Fixtures can depend on other fixtures:**
```python
@pytest.fixture
def login_page(page: Page) -> LoginPage:   # "page" fixture is injected here too
    return LoginPage(page)
```
Here, `login_page` depends on `page`. Pytest resolves the chain automatically.

**`conftest.py` is special:**
- Fixtures defined in `conftest.py` are available to all tests in that directory
  and its subdirectories — no import needed.
- This is how shared fixtures (auth, database setup, page objects) work across
  your entire test suite.

**Interview answer:**
> "Pytest resolves fixtures by parameter name, not type. It walks up the
> directory tree looking in conftest.py files, then checks installed plugins.
> Fixtures can depend on other fixtures, forming a dependency chain that Pytest
> resolves automatically. This is how I share setup like authentication state
> across all tests without imports — I define fixtures in conftest.py and Pytest
> injects them wherever a test function uses that parameter name."

---

## Day 2: Global Authentication & Storage State

### What is Playwright's storage_state?
`storage_state` captures everything a browser needs to "remember" a login:
- Cookies
- localStorage

You can **save** it to a JSON file after logging in, then **load** it into any
new browser context. That context behaves as if it already logged in.

**The flow:**
1. Launch browser → create throwaway context → log in → save `storage_state.json`
2. Each test creates a new context with `storage_state` pre-loaded → already logged in

**Interview answer:**
> "I use Playwright's storage_state to authenticate once per test session. The
> login fixture saves cookies and localStorage to a JSON file, then every test
> loads that state into a fresh context. This cuts minutes off pipeline time
> because login only happens once, not per-test."

### What are Pytest fixture scopes?
Scopes control how often a fixture runs:

| Scope | Runs once per... | Use case |
|-------|-----------------|----------|
| `function` (default) | each test | fresh page, isolated state |
| `class` | each test class | shared setup within a class |
| `module` | each test file | shared setup within a file |
| `session` | entire test run | one-time setup like auth, browser launch |

**Key rule:** a higher-scoped fixture (session) cannot depend on a lower-scoped
one (function). But lower can depend on higher.

**Interview answer:**
> "I use session scope for expensive, stateless resources like browser instances
> and authentication. Function scope for cheap, stateful resources like pages —
> so each test gets a clean slate and can't pollute other tests."

### What does yield do in a fixture vs return?
`yield` turns a fixture into a **setup + teardown** pair:

```python
@pytest.fixture()
def page(auth_context: BrowserContext) -> Generator[Page, None, None]:
    page = auth_context.new_page()   # SETUP — runs before the test
    yield page                        # hand value to test, pause here
    page.close()                      # TEARDOWN — runs after test, even on failure
```

- Everything before `yield` = setup
- The yielded value = what the test receives
- Everything after `yield` = teardown (guaranteed to run)

With `return`, there's no teardown phase. Use `return` when the fixture
handles its own cleanup before returning.

**Interview answer:**
> "I use yield in fixtures when I need guaranteed teardown — like closing pages,
> contexts, or database connections. The code after yield runs even if the test
> fails, so resources never leak."

### What is fixture override by proximity?
When multiple fixtures share the same name, Pytest picks the **closest** one:

1. Same test file (closest — wins)
2. conftest.py in same directory
3. conftest.py in parent directories
4. Installed plugins (farthest)

**Practical use:** define a global `page` fixture in conftest.py that provides
authenticated pages. For login tests that need a clean page, define a local
`page` fixture in the test file — it overrides the global one for just that file.

**Interview answer:**
> "I use fixture override by proximity to handle different setup needs. My global
> page fixture provides authenticated sessions by default. Test files that need
> unauthenticated pages — like login tests — define their own local page fixture
> that overrides the global one. No test code changes needed, just a fixture
> definition at the file level."

### How does pytestconfig connect CLI flags to fixtures?
`pytestconfig` is a built-in Pytest fixture that gives access to CLI options:

```python
@pytest.fixture(scope="session")
def browser_instance(pytestconfig) -> Generator[Browser, None, None]:
    headed = pytestconfig.getoption("--headed", default=False)
    browser = playwright.chromium.launch(headless=not headed)
```

This lets your custom fixtures respect CLI flags like `--headed` that are
registered by plugins (pytest-playwright). Without this, hardcoded values
in your fixture ignore what you pass on the command line.

---

## Day 3: Custom Pytest Fixtures & Auto-Injection

### What are custom page object fixtures?
Instead of manually creating page objects in every test:
```python
def test_something(self, page: Page) -> None:
    login_page = LoginPage(page)  # repeated everywhere
```

You define a fixture that does it for you:
```python
@pytest.fixture()
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)
```

Tests just declare the fixture as a parameter:
```python
def test_something(self, login_page: LoginPage) -> None:
    login_page.open()  # already instantiated
```

**Why it matters:**
- **DRY** — instantiation logic lives in one place
- **Consistency** — every test gets page objects set up the same way
- **Scalability** — adding a new page object = one fixture, zero test changes
- **Readability** — test signatures tell you exactly what pages are involved

**Interview answer:**
> "I use custom fixtures to auto-inject page objects into tests. This eliminates
> boilerplate, ensures consistent setup, and makes tests self-documenting — you
> can see from the function signature which pages a test interacts with."

### How do you organize fixtures across files?
Fixtures live in a dedicated `fixtures/` module (e.g., `fixtures/page_fixtures.py`).
They're registered in `conftest.py` via wildcard import:

```python
from fixtures.page_fixtures import *  # noqa: F401, F403
```

**Why this pattern:**
- Keeps `conftest.py` clean — it handles infrastructure (browser, auth), not page objects
- `fixtures/page_fixtures.py` is focused on page object creation
- Wildcard import means adding a new fixture requires zero changes to conftest
- `# noqa` tells linters to allow the wildcard import — this is a valid use case

**Interview answer:**
> "I separate fixtures into modules by concern — page fixtures in one file,
> API fixtures in another. They're imported into conftest.py via wildcard so
> Pytest can discover them. This keeps conftest focused on infrastructure and
> makes fixture files easy to navigate as the suite grows."

### Fixture dependency chains — how do they compose?
Fixtures can depend on other fixtures, forming automatic chains:

```
test asks for inventory_page
  → inventory_page fixture asks for page
  → page fixture (conftest) asks for auth_context
  → auth_context asks for browser_instance + authenticated_state
  → all resolved automatically by Pytest
```

The `inventory_page` fixture doesn't know or care about authentication. It
just receives a `page` and wraps it. The auth layer is handled by a completely
different fixture in a different file.

This is **composition over configuration** — each fixture does one thing, and
they snap together like building blocks.

### When should a fixture auto-navigate vs not?
- **Auto-navigate** (like `inventory_page`) when every test using it starts at
  the same URL. Eliminates repetitive `.open()` calls.
- **Don't auto-navigate** (like `login_page`) when tests need control over the
  starting point — e.g., testing what happens before navigation, or testing
  different entry paths.

### What is `Generator[X, None, None]` in fixture type hints?
The type hint for a `yield`-based fixture:
- 1st value (`X`) — what the fixture yields to the test
- 2nd value (`None`) — nothing is sent back into the generator
- 3rd value (`None`) — nothing is returned when done

When there's no teardown (no code after `yield`), you can use `return` instead
and simplify the type hint to just `-> X`.

### Adding a new page object — the checklist
When you need a new page (e.g., `CartPage`):
1. Create `pages/cart_page.py` extending `BasePage`
2. Add a `cart_page` fixture to `fixtures/page_fixtures.py`
3. Done — conftest's `import *` picks it up automatically

No changes to conftest, no changes to existing tests.

---

## Interview Theory — No Code, Pure Knowledge

> These topics don't have dedicated days in the repo, but they come up
> frequently in senior SDET and Quality Architect interviews.

### The Test Pyramid
A model for balancing test types by speed, cost, and confidence:

```
        /  E2E  \          ← Few: slow, expensive, high confidence
       /  Integ. \         ← Some: moderate speed, test component interaction
      /   Unit    \        ← Many: fast, cheap, test logic in isolation
```

| Level | Speed | Cost | Scope | Example |
|-------|-------|------|-------|---------|
| **Unit** | Milliseconds | Cheapest | Single function/class | Test that `calculate_tax(100)` returns `18` |
| **Integration** | Seconds | Moderate | Multiple components | Test that API endpoint writes to database correctly |
| **E2E** | Seconds-minutes | Most expensive | Full user flow | Test login → add to cart → checkout via browser |

**Anti-pattern:** The "ice cream cone" — mostly E2E tests, few unit tests.
Slow pipelines, flaky results, hard to debug failures.

**Interview answer:**
> "I follow the test pyramid — heavy unit coverage for fast feedback, integration
> tests for component boundaries like API-to-database, and selective E2E tests
> for critical user journeys. This keeps the pipeline fast while maintaining
> confidence. I avoid the ice cream cone anti-pattern where everything is tested
> through the UI."

### Test Strategy — What to Automate vs What Not To
Not everything should be automated. The decision framework:

**Automate when:**
- The test runs frequently (regression, smoke)
- It's repetitive and stable (login, checkout)
- It involves data-intensive validation (1000 records)
- It needs to run across multiple environments/browsers

**Keep manual when:**
- Exploratory testing (finding unknown bugs)
- UX/visual judgment calls ("does this look right?")
- One-time tests or rapidly changing features
- Accessibility nuances that need human judgment

**Risk-based testing:**
Prioritize test coverage based on:
1. **Business impact** — what breaks if this fails? (payment > color change)
2. **Frequency of use** — high-traffic flows first
3. **Likelihood of failure** — recently changed code, complex logic
4. **Regulatory requirements** — compliance features are non-negotiable

**Interview answer:**
> "I use risk-based testing to prioritize automation. High-business-impact,
> high-frequency flows get automated first — like login, payments, and core
> workflows. Exploratory and UX testing stays manual. For each feature, I
> evaluate business risk, change frequency, and complexity to decide the right
> mix of automated vs manual coverage."

### OWASP Top 10 — Security Basics for QA
The 10 most critical web application security risks. You don't need to be a
security expert, but you should know what these are and how to test for them.

1. **Broken Access Control** — users can access pages/data they shouldn't.
   *Test:* Try accessing admin URLs as a regular user.

2. **Cryptographic Failures** — sensitive data (passwords, tokens) stored or
   transmitted without encryption.
   *Test:* Check that passwords aren't in plain text, APIs use HTTPS.

3. **Injection (SQL/XSS)** — user input is executed as code.
   *Test:* Enter `<script>alert('xss')</script>` in form fields.
   Enter `' OR 1=1 --` in login fields.

4. **Insecure Design** — flawed architecture, not just bugs.
   *Test:* Can a user bypass checkout steps? Can they manipulate prices client-side?

5. **Security Misconfiguration** — default credentials, unnecessary features enabled.
   *Test:* Check for exposed debug endpoints, default admin passwords.

6. **Vulnerable Components** — outdated libraries with known CVEs.
   *Test:* Run `pip audit` or `npm audit` on the project.

7. **Authentication Failures** — weak passwords, no rate limiting.
   *Test:* Try brute-forcing login, check if session tokens rotate after login.

8. **Data Integrity Failures** — untrusted data in CI/CD pipelines or updates.
   *Test:* Verify code is signed, dependencies are pinned.

9. **Logging & Monitoring Gaps** — breaches go undetected.
   *Test:* Trigger a failed login — is it logged? Are alerts configured?

10. **Server-Side Request Forgery (SSRF)** — server makes requests to
    unintended internal resources.
    *Test:* Submit internal URLs (localhost, 127.0.0.1) in URL input fields.

**Interview answer:**
> "I'm familiar with the OWASP Top 10. In my test suites, I include basic
> security checks — testing for XSS by injecting script tags, verifying access
> control by trying unauthorized endpoints, and checking that sensitive data
> like tokens aren't exposed in API responses or logs."

### Docker Basics for SDETs
Docker packages your application (or test suite) into a container — a
lightweight, isolated environment that runs the same everywhere.

**Key concepts:**
- **Image** — a blueprint (like a class). Built from a `Dockerfile`.
- **Container** — a running instance of an image (like an object).
- **Dockerfile** — instructions to build an image:
  ```dockerfile
  FROM python:3.10-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  RUN playwright install chromium --with-deps
  COPY . .
  CMD ["pytest", "-v"]
  ```
- **docker-compose** — runs multiple containers together (e.g., test suite + database).

**Why SDETs need Docker:**
- **Consistent CI/CD** — tests run in the same environment locally and in pipelines
- **Dependency isolation** — no "works on my machine" issues
- **Parallel execution** — spin up multiple containers for parallel test runs
- **Clean state** — every container starts fresh, no leftover state

**Interview answer:**
> "I containerize my test suites with Docker to ensure consistent execution
> across local, CI, and staging environments. The Dockerfile installs all
> dependencies including browser binaries, so tests run identically everywhere.
> In CI/CD, each pipeline run spins up a fresh container — no state leaks
> between runs."

### SQL for Testers
Common queries that come up in SDET interviews. You should be comfortable
reading and writing these.

**Basic queries:**
```sql
-- Select with filtering
SELECT * FROM users WHERE status = 'active' AND created_at > '2025-01-01';

-- Aggregate functions
SELECT COUNT(*), AVG(price) FROM orders WHERE status = 'completed';

-- Group by with having
SELECT user_id, COUNT(*) as order_count
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 5;
```

**Joins:**
```sql
-- Inner join — only matching rows
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- Left join — all users, even those with no orders
SELECT u.name, COALESCE(o.total, 0) as total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

**Subqueries:**
```sql
-- Find users who placed orders above average
SELECT name FROM users
WHERE id IN (
    SELECT user_id FROM orders
    WHERE total > (SELECT AVG(total) FROM orders)
);
```

**Why SDETs need SQL:**
- Verify data persistence after API calls
- Set up test data directly in the database
- Assert backend state that's not visible in the UI
- Debug test failures by checking what data actually exists

**Interview answer:**
> "I use SQL to verify backend state in integration tests — confirming that
> API calls actually persist the right data, checking test preconditions, and
> debugging failures by querying the database directly. I'm comfortable with
> joins, aggregations, subqueries, and data manipulation."

---

## Day 4: Network Interception & API Mocking

### What is network interception?
Playwright's `page.route()` lets you intercept HTTP requests at the browser
network level. You sit between the browser and the server and control what
happens to each request.

```python
page.route("**/api/cars", lambda route: route.fulfill(
    status=200,
    content_type="application/json",
    body='{"status": "success", "cars": []}',
))
```

The browser's JavaScript runs for real — it fires a real HTTP request — but
Playwright catches it before it leaves and hands it to your handler.

### The three route actions
Every route handler MUST end with exactly one of:

| Method | What it does | Use case |
|--------|-------------|----------|
| `route.fulfill()` | Return a fake response you control | Mocking data, error states |
| `route.continue_()` | Let the real request go through | Spying/logging requests |
| `route.abort()` | Kill the request entirely | Testing offline/network failure |

If you don't call any of these, the request **hangs forever** and your test
times out.

Note: `continue_()` has an underscore because `continue` is a Python keyword.

### Why register routes BEFORE navigation
`page.route()` is like hiring a security guard. `page.goto()` is opening the
gate. If you open the gate first, requests pass through before the guard is
in position. Always register routes before navigating.

### What is a callback / lambda in this context?
`page.route()` takes a function as its second argument. Playwright calls this
function whenever a matching request is intercepted, passing in a `Route`
object. You define **what to do**; Playwright decides **when to do it**.

```python
# Lambda (one-liner):
page.route(pattern, lambda route: route.fulfill(status=200, body="..."))

# Named function (multi-line):
def handler(route: Route) -> None:
    captured.append(route.request.url)
    route.continue_()
page.route(pattern, handler)
```

Lambda is a shortcut for a one-line anonymous function. Use a named function
when you need multiple lines.

### Mock data must match real API structure
The #1 reason network mocking fails silently: your mock doesn't match the
real response format. Always inspect the actual API response (DevTools →
Network → click the request → Response tab) before writing mocks.

**Real API returns:**
```json
{"status": "success", "cars": [{"id": 1, "name": "...", "price": "€25,000"}]}
```

**Wrong mock:** `[]` — frontend expects an object with `status` and `cars` keys.
**Correct mock:** `{"status": "success", "cars": []}` — matches the structure.

### Network mocking vs unittest.mock
| | `unittest.mock` | `page.route()` |
|---|---|---|
| Where it works | Python code | Browser network layer |
| Browser involved | No | Yes |
| Frontend JS runs | No | Yes |
| Tests UI rendering | No | Yes |

Network mocking is more realistic — the entire frontend runs for real.

### When to use network interception in real projects
- **Error handling** — mock 500/404 to test UI error states
- **Edge cases** — inject zero prices, empty lists, negative values
- **Flaky prevention** — mock unstable third-party APIs
- **Speed** — skip slow API calls with instant mock responses
- **Unreleased features** — test frontend before backend is built
- **Security** — inject XSS payloads in API responses

### Wait strategies: networkidle vs alternatives
`wait_for_load_state("networkidle")` waits for zero network connections for
500ms. Many sites never reach this state (analytics, polling, websockets).

Better alternatives:
- `page.locator(selector).first.wait_for()` — wait for a specific element
- `page.wait_for_load_state("domcontentloaded")` — wait for HTML to parse
- `page.wait_for_timeout(2000)` — fixed wait (last resort for "no content" assertions)

**Interview answer:**
> "I use Playwright's page.route() to intercept browser network requests and
> test UI resilience with mocked data — empty responses, invalid values, server
> errors. This lets me verify error handling and edge cases that the real API
> would never return. I always inspect the actual API response first to ensure
> my mocks match the real structure. I also use route spying with continue_()
> to verify the frontend sends correct requests without modifying them."

---

## Day 5: Structured Logging, Centralized Config & Polish

### Why add logging to a test framework?
When a test fails in CI/CD, you can't open a browser and watch. Logs tell you
exactly what happened — which page was loaded, what was clicked, where it broke.

```
2026-04-07 14:30:15 | INFO     | LoginPage | Logging in as 'standard_user'
2026-04-07 14:30:16 | DEBUG    | LoginPage | Filling '#user-name' with 'standard_user'
2026-04-07 14:30:16 | DEBUG    | LoginPage | Clicking '#login-button'
```

**Interview answer:**
> "I add structured logging to my page objects so every action is traceable.
> When a test fails in CI, I can read the logs to see exactly what happened
> without rerunning locally. I use Python's logging module with lazy %s
> formatting for performance."

### Python logging levels
| Level | Value | Use for |
|-------|-------|---------|
| `DEBUG` | 10 | Detailed diagnostic (clicking, filling fields) |
| `INFO` | 20 | Key business actions (logging in, adding to cart) |
| `WARNING` | 30 | Unexpected but not broken |
| `ERROR` | 40 | Something failed |
| `CRITICAL` | 50 | System unusable |

Setting level to `INFO` means you see INFO + WARNING + ERROR + CRITICAL.
DEBUG messages are hidden. Change to `DEBUG` when troubleshooting.

### Why `%s` formatting instead of f-strings in logging?
```python
self.logger.debug("Clicking '%s'", selector)   # lazy — string built only if printed
self.logger.debug(f"Clicking '{selector}'")     # eager — string ALWAYS built
```

With `%s`, if the log level is above DEBUG, the string is never constructed.
With f-strings, Python builds the string regardless, then throws it away.
Performance difference at scale (thousands of log calls).

### Singleton logger pattern
`logging.getLogger(name)` returns the same object for the same name. The
`if not logger.handlers` check prevents adding duplicate handlers when the
logger is retrieved multiple times. Without it, messages print once per
handler — three calls = three copies of every message.

### `self.__class__.__name__` for automatic logger naming
Written in `BasePage.__init__`, but `self.__class__` refers to the **actual**
child class. So `LoginPage` logs as `"LoginPage"`, `CarPage` logs as `"CarPage"`.
Each child gets its own named logger without extra code.

### What are frozen dataclasses and why use them for config?
`@dataclass` auto-generates `__init__` and `__repr__` from field definitions.
`frozen=True` makes instances immutable — values can't be changed at runtime.

```python
@dataclass(frozen=True)
class SauceDemoConfig:
    base_url: str = "https://www.saucedemo.com"
    username: str = "standard_user"
```

**Why frozen?** Prevents accidental mutation. Without it, a bug in one test
could overwrite `SAUCE_DEMO.username` and silently break every test after it.

**Why dataclass instead of a regular class?** Pure data containers don't need
manual `__init__` and `__repr__`. Dataclass eliminates that boilerplate.

**Why not dataclass on page objects?** Page objects have behavior (methods),
inheritance (BasePage), and custom `__init__`. Dataclass conflicts with these.
Rule: data containers → dataclass. Behavior-driven classes → regular class.

### Why centralize config?
Hardcoded values scattered across files:
- One URL typo → hunt through 10 files to find it
- Change a credential → update every file that uses it
- Different environments (staging/prod) → rewrite everything

Centralized config:
- One source of truth in `utils/config.py`
- Change a URL once → every page object and test picks it up
- Environment switching → swap one config, everything follows

**Interview answer:**
> "I use frozen dataclasses for configuration — URLs, credentials, timeouts —
> in a single config module. They're immutable so tests can't accidentally
> mutate shared state, type-hinted for IDE support, and centralized so
> environment changes are a one-line update."

---

## Day 6: API Test Foundation

### REST API & HTTP Methods
REST (Representational State Transfer) uses HTTP methods to perform actions on
resources (represented by URLs):

| Method | Action | Example |
|--------|--------|---------|
| **POST** | Create | `POST /booking` — create a new booking |
| **GET** | Read | `GET /booking/15` — retrieve booking #15 |
| **PUT** | Replace | `PUT /booking/15` — replace entire booking #15 |
| **PATCH** | Partial update | `PATCH /booking/15` — update one field |
| **DELETE** | Remove | `DELETE /booking/15` — delete booking #15 |

This maps to **CRUD** — Create, Read, Update, Delete.

**Interview answer:**
> "I structure API tests around CRUD operations. Each test targets a specific
> HTTP method and validates status codes, response bodies, and data contracts.
> I use PUT for full replacement and PATCH for partial updates — knowing the
> difference matters for correct test design."

### What is `requests.Session` and why use it?
`requests.Session` maintains state across multiple HTTP requests:

1. **Persistent headers** — set `Content-Type` and `Accept` once, sent with every
   request automatically.
2. **Persistent cookies** — after authentication, the token cookie is sent with
   every subsequent request. Individual methods don't need to know about auth.
3. **TCP connection pooling** — reuses the underlying network connection instead
   of opening a new one per request (skips the 3-step TCP handshake).

Without a session, every API call repeats headers, cookies, and connection setup.

```python
self.session: requests.Session = requests.Session()
self.session.headers.update(dict(BOOKER_API.default_headers))
```

**Interview answer:**
> "I use requests.Session as the foundation for my API client. It persists
> headers and authentication cookies across requests, reuses TCP connections
> for performance, and centralizes HTTP configuration. This mirrors how a
> real client maintains a session with a server."

### What is `raise_for_status()` and why always use it?
`response.raise_for_status()` throws an `HTTPError` if the status code is
4xx (client error) or 5xx (server error). Without it, a 500 response silently
passes — your code moves on to parse the response body, which is either garbage
or an error message, and your test may assert on wrong data.

```python
response = self.session.post(url, json=data)
response.raise_for_status()   # fails immediately on 4xx/5xx
return response.json()        # only reached if status was 2xx
```

**Rule:** Call `raise_for_status()` right after the request, before parsing.

**Interview answer:**
> "I call raise_for_status() after every API request as a fail-fast guard.
> If the server returns an error, the test fails immediately with a clear
> HTTP error — not a confusing JSON parse error downstream."

### `json=` parameter vs `data=` in requests
Two ways to send data:

| Parameter | What it does | Content-Type |
|-----------|-------------|-------------|
| `json=` | Takes a dict, auto-serializes to JSON string, sets Content-Type | `application/json` |
| `data=` | Takes raw string/bytes, sends as-is, you handle serialization | `application/x-www-form-urlencoded` |

Always use `json=` for JSON APIs — it handles serialization and headers in one step.

### Typed models vs raw dicts for test data
Raw dicts have no safety — typos in key names and wrong value types pass silently
until runtime. Typed dataclass models catch these at write-time via IDE warnings.

```python
# Raw dict — typo in "lastnme" goes unnoticed until API returns 400
payload = {"firstname": "James", "lastnme": "Brown", "totalprice": "150"}

# Typed model — IDE immediately flags unknown field and wrong type
payload = BookingPayload(firstname="James", lastnme="Brown", totalprice="150")
```

Models also provide autocomplete — type `payload.` and the IDE shows all fields.

**Interview answer:**
> "I use typed dataclass models for API payloads instead of raw dicts. They
> provide IDE autocomplete, catch field name typos and type mismatches before
> runtime, and serve as living documentation of the API's data contract."

### `asdict()` for recursive dataclass conversion
`dataclasses.asdict()` converts a dataclass to a plain dict **recursively** —
nested dataclasses are also converted. `__dict__` only converts the top level,
leaving nested dataclasses as objects that `json.dumps` can't serialize.

```python
# BookingPayload has a nested BookingDates dataclass
asdict(payload)
# → {"firstname": "James", ..., "bookingdates": {"checkin": "2026-06-01", ...}}

payload.__dict__
# → {"firstname": "James", ..., "bookingdates": BookingDates(checkin="2026-06-01", ...)}
# ← BookingDates is still an object — requests can't serialize this to JSON
```

### Tuple-of-tuples for immutable defaults in frozen dataclasses
Frozen dataclasses require all default values to be immutable. Dicts are mutable,
so they raise `TypeError` as defaults. Use tuple-of-tuples instead:

```python
@dataclass(frozen=True)
class BookerApiConfig:
    default_headers: tuple[tuple[str, str], ...] = (
        ("Content-Type", "application/json"),
        ("Accept", "application/json"),
    )
```

Convert to dict when needed: `dict(BOOKER_API.default_headers)`.

### API client pattern — same principle as POM
The API client class (`BookerClient`) follows the same pattern as Page Object
Model for UI tests:

| | UI Testing (POM) | API Testing (Client) |
|---|---|---|
| **Abstraction** | Page class wraps browser actions | Client class wraps HTTP calls |
| **Tests call** | `login_page.login(user, pass)` | `client.create_booking(payload)` |
| **Tests don't touch** | Raw selectors, Playwright API | Raw URLs, headers, requests |
| **Change URL/selector** | Update one page class | Update one client method |

**Interview answer:**
> "I apply the same abstraction pattern to API testing that I use for UI.
> The API client encapsulates endpoints, headers, auth, and error handling.
> Tests call clean methods like create_booking() — they don't construct URLs
> or manage sessions. If an endpoint changes, I update one method in the
> client, not every test."

### Session-scoped API fixtures
The `booker_client` fixture is session-scoped — authenticates once and reuses
the token for all tests. Same pattern as browser authentication from Day 2.

`sample_booking` is function-scoped — each test gets its own fresh payload.

```python
@pytest.fixture(scope="session")
def booker_client() -> BookerClient:
    client = BookerClient()
    client.authenticate()     # once for entire test run
    return client

@pytest.fixture()
def sample_booking() -> BookingPayload:
    return BookingPayload(...)  # fresh copy per test
```

**Why this split:**
- **Client = infrastructure** — stateless auth, safe to share across all tests
- **Test data = per-test** — isolated so one test can't affect another

### Security: credentials in config vs environment variables
For practice APIs with public credentials (SauceDemo, Restful Booker), inline
config is fine. For real projects, credentials should never be in source code.

**Production approach:**
```python
username: str = field(default_factory=lambda: os.environ["BOOKER_USERNAME"])
```

Credentials live in `.env` files (gitignored locally) or CI/CD secret stores
(GitHub Actions secrets, HashiCorp Vault).

**Interview answer:**
> "In production frameworks, I never hardcode credentials. I use environment
> variables loaded at runtime — locally via .env files (gitignored), and in
> CI/CD via the pipeline's secrets manager. The config dataclass uses
> field(default_factory=...) to pull from os.environ."

---

## Day 7: API Schema Validation & Data-Driven Tests

### What is JSON Schema and why use it for API testing?
JSON Schema is a standard vocabulary for defining the expected structure of
JSON data — field names, types, required fields, nesting, and allowed values.
Instead of manually asserting `"firstname" in response`, you define the entire
contract once and validate against it.

```python
from jsonschema import validate

schema = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": {"type": "object", ...},
    },
    "additionalProperties": False,
}

validate(instance=api_response, schema=schema)
```

If validation passes — nothing happens (test passes silently).
If validation fails — `jsonschema.ValidationError` is raised with a detailed
message like `"'firstname' is a required property"`. No `assert` needed.

**Interview answer:**
> "I use JSON Schema for API contract testing. It validates the entire response
> structure in one call — required fields, types, nesting — instead of manual
> assertions per field. With additionalProperties: false, I catch API drift
> where new fields are silently added. Schema tests complement value assertions
> to provide full API coverage."

### Schema validation vs value assertion — why both?
They catch different categories of bugs:

| | Schema Validation | Value Assertion |
|---|---|---|
| **Checks** | Structure (fields, types, nesting) | Content (actual values) |
| **Catches** | Missing fields, wrong types, extra fields | Wrong data, bad calculations |
| **Example pass** | `{"firstname": "WRONG"}` (string ✓) | Fails — expected "James" |
| **Example fail** | `{"first_name": "James"}` (wrong key) | Never reached |

A response can have the right structure but wrong values, or right values in
the wrong structure. You need both layers.

### What is `additionalProperties: false`?
Rejects any fields not explicitly listed in `"properties"`. Without it, the
schema ignores unexpected fields.

**Without it:** `{"firstname": "James", "ssn": "123-45-6789"}` passes silently.
**With it:** Fails with `Additional properties are not allowed ('ssn' was unexpected)`.

**What it catches:**
- API returning internal/debug fields (security risk)
- API contract changes nobody told you about
- Different API versions returning different shapes

**Tradeoff:** You must update the schema when the API intentionally adds fields.
This is a feature — it forces explicit review of every contract change.

**Interview answer:**
> "I use additionalProperties: false in schemas to enforce strict API contracts.
> If the backend adds a field without updating the contract, my tests catch it
> immediately. This prevents silent drift and catches accidental exposure of
> internal data."

### What is `pytest.mark.parametrize`?
Runs the same test function multiple times with different data sets. Each set
becomes a separate test case — if one fails, others still run.

```python
@pytest.mark.parametrize(
    "firstname, lastname, totalprice",
    [
        ("Alice", "Smith", 100),
        ("Bob", "Jones", 0),
        ("Charlie", "Lee", 999999),
    ],
    ids=["standard", "zero_price", "high_price"],
)
def test_create(self, booker_client, firstname, lastname, totalprice):
    ...
```

**`ids=`** gives human-readable names in output:
- With ids: `test_create[zero_price]`
- Without: `test_create[Bob-Jones-0]`

**Why parametrize instead of separate tests?**
- **DRY** — test logic written once, data varies
- **Maintainability** — change assertion logic in one place, not 5 copies
- **Scalability** — add a new test case = add one tuple to the list

**Stacking decorators for combinations:**
```python
@pytest.mark.parametrize("browser", ["chrome", "firefox"])
@pytest.mark.parametrize("env", ["staging", "prod"])
def test_login(browser, env):  # runs 4 times (2 × 2)
```

**Interview answer:**
> "I use pytest.mark.parametrize for data-driven tests. The test logic is
> written once and executed with multiple data sets — edge cases, boundary
> values, special characters. Each parameterized case runs independently, so
> one failure doesn't block others. I use ids for readable test output."

### What is `pytest.raises` and how to inspect exceptions?
A context manager that asserts code raises a specific exception. If the code
*doesn't* raise, the test *fails*.

```python
# Basic — just verify the error happens
with pytest.raises(requests.HTTPError):
    client.get_booking(999999999)

# Advanced — capture and inspect error details
with pytest.raises(requests.HTTPError) as exc_info:
    client.get_booking(999999999)

assert exc_info.value.response.status_code == 404
```

**The chain explained:**
- `exc_info` — Pytest's ExceptionInfo wrapper
- `.value` — the actual exception object
- `.response` — the HTTP response (attached by requests library)
- `.status_code` — the numeric status code (404, 500, etc.)

**Why inspect the status code?** Without it, any HTTP error passes —
including a 500 (server crash) when you expected a 404 (not found). A 500
for a nonexistent resource is a server bug, not correct behavior.

**Interview answer:**
> "I use pytest.raises for negative testing — verifying that errors happen
> when expected. I capture the exception with `as exc_info` to inspect
> specific details like HTTP status codes, ensuring the API returns the
> correct error type, not just any error."

### What is negative testing and why does it matter?
Testing that the system correctly handles invalid inputs, unauthorized access,
and error conditions. Day 6 tests were all "happy path" — valid data,
authenticated user, existing resources. Negative tests prove the guardrails work.

**What negative tests catch:**
- **Missing error handling** — API returns 200 for nonexistent resource
- **Auth bypass** — unauthenticated users can delete records (security bug)
- **Silent failures** — API accepts garbage data without validation
- **Wrong error codes** — 500 (server bug) instead of 400 (bad input)

**Interview answer:**
> "I include negative tests for every API — nonexistent resources,
> unauthenticated access, invalid payloads. These catch security
> vulnerabilities like auth bypass and incorrect error codes. Most
> production bugs come from unhandled edge cases, not the happy path."

### Unauthenticated client pattern for access control testing
To test that the API enforces authentication, create a separate client that
*doesn't* call `authenticate()`:

```python
def test_unauthenticated_delete_fails(self) -> None:
    unauth_client = BookerClient()          # no authenticate()
    created = unauth_client.create_booking(payload)  # create works without auth
    with pytest.raises(requests.HTTPError):
        unauth_client.delete_booking(created.bookingid)  # delete requires auth
```

The test doesn't use the `booker_client` fixture (which is authenticated).
It creates its own client, proving that the API rejects the operation without
a token. Pytest only injects fixtures that appear in the function signature —
if `booker_client` isn't a parameter, the fixture is never involved.

Same principle as UI login tests overriding the authenticated `page` fixture
to get clean, unauthenticated browser pages.

**Interview answer:**
> "I test access control by creating unauthenticated client instances
> separate from the shared authenticated fixture. This verifies that
> protected operations properly reject requests without tokens. I've
> caught real bugs this way — APIs where GET was protected but DELETE
> wasn't, due to misconfigured auth middleware."

### `create_booking_raw()` — why a separate method?
The existing `create_booking()` returns a typed `BookingResponse` dataclass.
Schema validation needs the raw dict (as returned by the API) to validate
against the JSON schema.

Adding a separate `create_booking_raw()` method follows **Single Responsibility**:
- `create_booking()` → typed object for value assertions
- `create_booking_raw()` → raw dict for schema validation

Existing Day 6 tests don't break. New schema tests use the new method.

---

## Day 8: K6 Performance Testing Setup

### What is K6?
K6 is an open-source load testing tool by Grafana Labs. Scripts are written
in JavaScript, executed by a Go-based runtime (not Node.js). It's lightweight,
CLI-first, and designed for CI/CD integration.

**Why K6 over other tools (JMeter, Gatling, Locust)?**
- Scripts are code (JS), not XML/GUI configs — version-controllable, reviewable
- Go-based engine = low resource usage, high throughput
- Built-in thresholds for pass/fail in CI pipelines
- No JVM dependency (unlike JMeter/Gatling)
- Industry standard — heavily asked in SDET interviews

### K6 script anatomy
Every K6 script has four key parts:

```javascript
// 1. OPTIONS — load profile and thresholds
export const options = {
    stages: [...],
    thresholds: {...},
};

// 2. SETUP — runs once before all VUs (like session-scoped fixture)
export function setup() {
    const token = authenticate();
    return { token };  // passed to every VU iteration
}

// 3. DEFAULT FUNCTION — what each VU executes repeatedly
export default function (data) {
    // data = what setup() returned
    http.get(url, params);
    sleep(1);
}

// 4. TEARDOWN — runs once after all VUs finish (optional)
export function teardown(data) { }
```

### Virtual Users (VUs) vs Requests
A VU is a simulated user running the default function in a loop. One VU
generates multiple requests per iteration.

In the booking test:
- 5 VUs, each running: create → get → list = 3 requests per iteration
- With sleep(1), each VU does ~1 iteration per ~4 seconds
- 45 total iterations × 3 requests = ~135 HTTP requests + 1 auth in setup

VUs are concurrent — they run in parallel, not sequentially.

### Stages — ramp-up, hold, ramp-down
The most common load test pattern:

```javascript
stages: [
    { duration: "10s", target: 5 },   // RAMP UP: gradually add users
    { duration: "20s", target: 5 },   // HOLD: sustain steady load
    { duration: "10s", target: 0 },   // RAMP DOWN: gradually remove users
]
```

- **Ramp up** — finds issues that appear as load increases (connection pooling,
  resource contention)
- **Hold** — measures steady-state performance (the main measurement phase)
- **Ramp down** — verifies the system recovers gracefully (no stuck connections,
  no resource leaks)

### Thresholds — automated pass/fail gates
Thresholds define SLAs as code. If violated, K6 exits with non-zero exit code
— failing the CI pipeline.

```javascript
thresholds: {
    http_req_duration: ["p(95)<2000"],  // 95th percentile under 2 seconds
    http_req_failed: ["rate<0.05"],     // less than 5% error rate
    checks: ["rate>0.95"],             // more than 95% of checks pass
}
```

**Interview answer:**
> "I define performance thresholds as code in K6 — p95 response time, error
> rate, and check pass rate. If any threshold is breached, K6 returns a
> non-zero exit code that fails the CI pipeline. This turns performance
> requirements into automated gates, not manual observations."

### Checks vs Thresholds — the difference
| | Checks | Thresholds |
|---|---|---|
| **What** | Per-request assertions | Aggregate pass/fail gates |
| **On failure** | Records failure, keeps running | Fails the entire test |
| **Purpose** | Verify individual responses | Enforce SLAs across all requests |
| **Example** | "status is 200" | "p(95) < 2000ms" |

Checks are like soft assertions — they record pass/fail rates without stopping.
Thresholds are hard gates — they determine if the overall test passed or failed.

### Percentiles — p90, p95, p99
Average response time is misleading. If 99 requests take 100ms and 1 takes
10 seconds, the average is 199ms — looks fine, but 1% of users had a terrible
experience.

| Metric | Meaning | Use case |
|--------|---------|----------|
| **p(50)** / median | Half of requests are faster | Typical user experience |
| **p(90)** | 90% are faster, 10% are slower | Most users' experience |
| **p(95)** | 95% are faster, 5% are slower | Industry standard SLA metric |
| **p(99)** | 99% are faster, 1% are slower | Worst-case for almost all users |

**Why p95 is the standard:** It represents the experience of the slowest 5%
of users — bad enough to cause complaints, but excludes extreme outliers.

**Interview answer:**
> "I measure performance using p95, not averages. Averages hide slow requests
> — a p95 of 2 seconds means 5% of users wait over 2 seconds. I set
> thresholds on p95 because it represents the tail latency that causes real
> user complaints."

### `setup()` vs `default function` — K6 lifecycle
| | `setup()` | `default function` |
|---|---|---|
| Runs | Once, before all VUs | Per VU, per iteration |
| Purpose | One-time initialization (auth) | Simulate user actions |
| Analogy | Pytest session-scoped fixture | Pytest function-scoped fixture |

`setup()` returns data that's passed to every iteration of `default function`.
The auth token is fetched once and shared — same pattern as your Pytest
`booker_client` session-scoped fixture.

### Think time — `sleep()` in load tests
`sleep(1)` adds a 1-second pause between iterations, simulating a real user
who reads, thinks, and clicks — not a bot firing requests as fast as possible.

Without think time, you're testing machine-gun traffic (stress test / DDoS
simulation). With think time, you're testing realistic user behavior.

### Load testing vs stress testing vs soak testing
All use the same K6 scripts — only the load profile changes:

| | Load Test | Stress Test | Soak Test |
|---|---|---|---|
| **Traffic** | Normal/expected | Beyond limits | Normal/expected |
| **Duration** | Minutes | Minutes | Hours |
| **Question** | "Can it handle normal traffic?" | "Where does it break?" | "Does it hold up over time?" |
| **Finds** | Slow endpoints, missing indexes | Breaking point, crash recovery | Memory leaks, connection leaks, token expiry |
| **When** | Every sprint/PR | Before major launches | Weekly/pre-release |

**Interview answer:**
> "I run three types of performance tests. Load tests verify expected traffic
> stays within SLAs — this runs in CI. Stress tests push beyond limits to
> find the breaking point — before major launches. Soak tests run at normal
> load for hours to catch memory leaks and token expiry — weekly. All three
> use the same K6 scripts with different stage configurations."

### SLA, SLO, SLI — the performance vocabulary
| Term | Meaning | Example |
|------|---------|---------|
| **SLA** (Service Level Agreement) | External promise to customers | "99.9% uptime" |
| **SLO** (Service Level Objective) | Internal target (stricter than SLA) | "99.95% uptime" |
| **SLI** (Service Level Indicator) | Actual measured metric | "Current uptime: 99.97%" |

K6 thresholds codify SLOs. If thresholds pass, you're meeting your objectives.
If the SLO is stricter than the SLA, you have buffer before breaching the
customer-facing promise.

---

*Day 8 complete. More sections will be added as new days are completed.*

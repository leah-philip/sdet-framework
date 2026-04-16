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

*More sections will be added as new days are completed.*

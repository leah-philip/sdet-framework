# QA Level Up — Master SDET Framework

A professional-grade test automation framework built with **Python**, **Playwright**, and **Pytest**, demonstrating advanced SDET patterns and engineering best practices.

## Tech Stack

- **Python 3.10+**
- **Playwright** — browser automation
- **Pytest** — test framework with fixtures and plugins

## Project Structure

```
├── conftest.py           # Global fixtures: auth, browser lifecycle
├── pages/
│   ├── base_page.py      # BasePage with common browser actions
│   └── login_page.py     # LoginPage for SauceDemo
├── tests/
│   ├── test_login.py     # Login flow tests (unauthenticated)
│   └── test_inventory.py # Inventory tests (pre-authenticated)
├── fixtures/             # Custom fixture modules (Day 3+)
├── utils/                # Shared utilities (logging, config)
└── data/                 # Test data and generated state files
```

## Key Patterns Implemented

### Page Object Model (POM)
Every page is a class inheriting from `BasePage`. Locators are class constants, actions are methods. Tests never touch raw selectors.

### Global Authentication via Storage State
Login runs **once per session**. Browser cookies and localStorage are saved to `storage_state.json` and loaded into every test's browser context — no repeated logins.

### Fixture Override by Proximity
The global `page` fixture provides authenticated sessions. Tests that need clean pages (e.g., login tests) override the fixture locally — no code changes needed in the tests themselves.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Running Tests

```bash
# Headless (default)
pytest

# With visible browser
pytest --headed

# Verbose output
pytest -v
```

## Roadmap

- [x] Project scaffold + Base POM
- [x] Global authentication with storage state
- [ ] Custom Pytest fixtures (auto-inject Page Objects)
- [ ] Network interception & API mocking
- [ ] Structured logging & centralized config
- [ ] API testing framework
- [ ] Performance testing with K6
- [ ] Mobile emulation
- [ ] AI/LLM testing with DeepEval
- [ ] CI/CD with GitHub Actions

# QA Level Up — Master SDET Framework

A professional-grade test automation framework built with **Python**, **Playwright**, and **Pytest**, demonstrating advanced SDET patterns and engineering best practices.

## Tech Stack

- **Python 3.10+**
- **Playwright** — browser automation
- **Pytest** — test framework with fixtures and plugins
- **Requests** — HTTP client for API testing

## Project Structure

```
├── conftest.py           # Global fixtures: auth, browser lifecycle
├── api/
│   └── booker_client.py  # REST API client (requests.Session)
├── models/
│   └── booking.py        # Typed request/response dataclass models
├── pages/
│   ├── base_page.py      # BasePage with common browser actions
│   └── login_page.py     # LoginPage for SauceDemo
├── tests/
│   ├── test_login.py     # Login flow tests (unauthenticated)
│   ├── test_inventory.py # Inventory tests (pre-authenticated)
│   └── test_booking_api.py # API CRUD tests (Restful Booker)
├── fixtures/             # Custom fixture modules (page + API)
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

### API Client Pattern
API tests use a dedicated client class (`BookerClient`) built on `requests.Session` — persistent auth, headers, and connection pooling. Typed dataclass models define request/response contracts. Same abstraction principle as POM for UI tests.

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

## Tracking Progress

This repo is built day-by-day as a learning exercise. Two files are maintained alongside the code:

- **`PROMPT.md`** — session context for AI-assisted learning. Updated after each day with what was built, current project structure, and what's next. Paste into a new chat to resume without losing context.
- **`LEARNING_NOTES.md`** — interview-ready reference of concepts and patterns learned. Updated after each day with explanations and interview answers for every topic covered.

**After completing each day:** update both files before ending your session.

## Roadmap

- [x] Project scaffold + Base POM
- [x] Global authentication with storage state
- [x] Custom Pytest fixtures (auto-inject Page Objects)
- [x] Network interception & API mocking
- [x] Structured logging & centralized config
- [x] API testing framework
- [ ] API schema validation & data-driven tests
- [ ] Performance testing with K6
- [ ] Mobile emulation
- [ ] AI/LLM testing with DeepEval
- [ ] CI/CD with GitHub Actions

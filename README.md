![CI](https://github.com/leah-philip/QA_Level_Up/actions/workflows/test.yml/badge.svg)
# QA Level Up — Master SDET Framework

A professional-grade test automation framework built with **Python**, **Playwright**, and **Pytest**, demonstrating advanced SDET patterns and engineering best practices.

## Tech Stack

- **Python 3.10+**
- **Playwright** — browser automation
- **Pytest** — test framework with fixtures and plugins
- **Requests** — HTTP client for API testing
- **jsonschema** — API contract validation
- **K6** — performance/load testing

## Project Structure

```
├── conftest.py              # Global fixtures: auth, browser lifecycle
├── api/
│   └── booker_client.py     # REST API client (requests.Session)
├── models/
│   └── booking.py           # Typed request/response dataclass models
├── schemas/
│   └── booking_schema.py    # JSON schemas for API contract validation
├── pages/
│   ├── base_page.py         # BasePage with common browser actions
│   └── login_page.py        # LoginPage for SauceDemo
├── tests/
│   ├── test_login.py        # Login flow tests (unauthenticated)
│   ├── test_inventory.py    # Inventory tests (pre-authenticated)
│   ├── test_booking_api.py  # API CRUD tests (Restful Booker)
│   ├── test_booking_schema.py     # Schema validation tests
│   ├── test_booking_parametrize.py # Data-driven parameterized tests
│   └── test_booking_negative.py   # Negative & auth bypass tests
├── fixtures/                # Custom fixture modules (page + API)
├── utils/                   # Shared utilities (logging, config)
├── performance/
│   └── scripts/
│       └── booking_load_test.js  # K6 load test with stages & thresholds
└── data/                    # Test data and generated state files
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

### JSON Schema Contract Testing
API responses are validated against strict JSON schemas with `additionalProperties: false`. Catches field additions, removals, and type changes in the API contract — an early warning system for breaking changes.

### Data-Driven & Negative Testing
Parameterized tests cover edge cases (zero price, special characters, empty strings) without duplicating test logic. Negative tests verify error handling, 404 responses, and auth enforcement using `pytest.raises`.

### K6 Performance Testing
Load tests simulate concurrent users against the Restful Booker API with ramp-up/hold/ramp-down stages. Thresholds enforce SLAs as code — p95 response time, error rate, and check pass rate. Threshold breaches return non-zero exit codes for CI/CD integration.

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

# K6 load test
k6 run performance/scripts/booking_load_test.js
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
- [x] API schema validation & data-driven tests
- [x] Performance testing with K6
- [ ] Mobile emulation
- [ ] AI/LLM testing with DeepEval
- [ ] CI/CD with GitHub Actions

## Test Coverage Summary

| Area | File | Tests | What's Covered |
|------|------|-------|----------------|
| UI — Login | `test_login.py` | 3 | Successful, locked out, invalid credentials |
| UI — Inventory | `test_inventory.py` | 5 | Items, sorting, add/remove cart |
| UI — Network | `test_cars_network.py` | 6 | Mocking, spying, error simulation |
| API — CRUD | `test_booking_api.py` | 6 | Create, read, update, delete, structure |
| API — Schema | `test_booking_schema.py` | 3 | Contract validation (create, get, list) |
| API — Data-Driven | `test_booking_parametrize.py` | 8 | Edge cases, boundary values, dates |
| API — Negative | `test_booking_negative.py` | 5 | 404, auth bypass, error handling |
| Perf — Load | `booking_load_test.js` | K6 | Ramp-up/hold/ramp-down, 5 VUs, 3 thresholds |
| **Total** | | **36 + K6** | |

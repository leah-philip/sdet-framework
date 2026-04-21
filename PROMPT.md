# Master SDET Upskilling — Session Context

> Paste this into any new chat so the AI has full context of your progress.

## Who I Am
- 4-year Senior QA Engineer transitioning to Quality Architect/SDET
- Target: ₹25L+ package
- Core stack: Python, Playwright, Pytest

## Repository Purpose
Single professional-grade repo (`QA_Level_Up/`) demonstrating advanced SDET patterns.
Building it day-by-day as a learning exercise — I write the code myself from instructions.

## Current Project Structure
```
QA_Level_Up/
├── conftest.py              # Global fixtures + imports page_fixtures via wildcard import
├── pytest.ini               # testpaths=tests, -v --tb=short
├── requirements.txt         # pytest>=8.0, pytest-playwright>=0.5.0
├── .gitignore               # venv/, __pycache__/, *.pyc, data/storage_state.json
├── PROMPT.md                # This file — session context
├── LEARNING_NOTES.md        # Interview-ready concept notes
├── pages/
│   ├── __init__.py
│   ├── base_page.py         # BasePage: common actions + logging (navigate, click, fill, get_text)
│   ├── login_page.py        # LoginPage: SauceDemo login (inherits BasePage)
│   ├── inventory_page.py    # InventoryPage: inventory actions (add/remove cart, sort, item count)
│   └── car_page.py          # CarPage: cars showroom (expandtesting.com/cars)
├── tests/
│   ├── __init__.py
│   ├── test_login.py        # 3 login tests + local page fixture override (unauthenticated)
│   ├── test_inventory.py    # 5 inventory tests using auto-injected inventory_page fixture
│   └── test_cars_network.py # 6 network interception tests (mock, spy, error handling)
├── fixtures/
│   ├── __init__.py
│   └── page_fixtures.py     # Custom fixtures: login_page, inventory_page, car_page
├── utils/
│   ├── __init__.py
│   ├── logger.py            # get_logger() — structured logging with singleton pattern
│   └── config.py            # Frozen dataclass configs: SAUCE_DEMO, CARS, TIMEOUTS
└── data/
    └── storage_state.json   # Auto-generated: saved browser cookies/localStorage after login
```

## Completed Days

### Day 1 — Project Scaffold + Base POM ✅
- Created folder structure with pages/, tests/, utils/, fixtures/, data/
- Set up virtual environment (venv/) and installed dependencies
- Built BasePage with type-hinted common browser actions
- Built LoginPage extending BasePage for https://www.saucedemo.com
- Wrote 3 login tests (successful, locked_out, invalid_credentials)
- Configured pytest.ini and .gitignore

### Day 2 — Global Authentication ✅
- Built 4 fixtures in conftest.py: browser_instance (session), authenticated_state (session), auth_context (function), page (function)
- Login runs once per session, saves cookies to data/storage_state.json
- All tests get pre-authenticated pages by default via the global page fixture
- test_login.py overrides page fixture locally to get clean unauthenticated pages
- Added test_inventory.py with 3 tests that skip login entirely
- Connected --headed CLI flag to custom browser_instance fixture via pytestconfig

### Day 3 — Custom Pytest Fixtures ✅
- Created InventoryPage (pages/inventory_page.py) with cart, sort, and item count methods
- Created fixtures/page_fixtures.py with login_page and inventory_page fixtures
- Registered fixtures in conftest.py via `from fixtures.page_fixtures import *`
- Refactored test_login.py and test_inventory.py to use auto-injected page objects
- Tests no longer manually instantiate page objects — fixtures handle it
- Added 2 new cart tests (add/remove) in test_inventory.py (now 5 inventory tests)

### Day 4 — Network Interception & Mocking ✅
- Created CarPage (pages/car_page.py) for https://practice.expandtesting.com/cars
- Added car_page fixture to fixtures/page_fixtures.py
- Built 6 network interception tests in test_cars_network.py:
  - Baseline real data load, empty list mock, zero price, negative price, 500 error, request spy
- Used page.route() with fulfill(), continue_(), and abort() patterns
- Mocked API responses matching real structure: {"status": "success", "cars": [...]}
- Discovered UI has no error handling — fails silently on bad data (real finding)
- Local unauthenticated page fixture override for cars tests (not SauceDemo)
- Learned: always inspect actual API response before writing mocks

### Day 5 — Logging, Config & Week 1 Polish ✅
- Created utils/logger.py with get_logger() — singleton pattern, StreamHandler to stdout
- Created utils/config.py with frozen dataclasses: SauceDemoConfig, CarsConfig, TimeoutConfig
- Added logging to BasePage (all actions log automatically via self.__class__.__name__)
- Added business-level logs to LoginPage, InventoryPage (login, add/remove cart, sort)
- Replaced all hardcoded URLs/credentials with config constants (SAUCE_DEMO, CARS)
- Fixed fixture consistency: all page fixtures use return (no teardown needed)
- Wired conftest.py credentials to SAUCE_DEMO config

## Coding Standards Being Followed
- Type hints on all functions and classes
- Page Object Model (POM) with inheritance
- SOLID principles and clean code
- Structured logging via utils/logger.py (DEBUG/INFO levels, %s lazy formatting)
- Centralized config via frozen dataclasses in utils/config.py
- decimal library for financial calculations (when needed)

## Day-by-Day Roadmap

### Week 1: Advanced Framework Architecture
- Day 1: Project Scaffold + Base POM ✅
- Day 2: Global Authentication ✅
- Day 3: Custom Pytest Fixtures ✅
- Day 4: Network Interception & Mocking ✅
- Day 5: Logging + Config + Polish ✅

### Week 2: API Testing
- Day 6: API Test Foundation (Pytest-based API client, request/response models)
- Day 7: API Schema Validation & Data-Driven Tests

### Week 3: Performance Testing
- Day 8: K6 Setup + First Script
- Day 9: K6 Thresholds + CI Integration

### Week 4: Mobile Testing
- Day 10: Playwright Mobile Emulation
- Day 11: Appium Basics (Optional)

### Week 5: AI/LLM Testing
- Day 12: DeepEval Setup
- Day 13: LLM Metrics & Assertions

### Week 6: CI/CD & Portfolio Polish
- Day 14: GitHub Actions Pipeline (Dockerized)
- Day 15: README, Reporting & Final Polish

## What To Do Next
Week 1 complete! Start Day 6: API Test Foundation. Give me step-by-step instructions to:
1. Build a Pytest-based API client for testing REST APIs
2. Create request/response models with type hints
3. Write API tests with proper assertions and data validation

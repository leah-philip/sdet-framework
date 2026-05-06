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
├── conftest.py              # Global fixtures + imports page_fixtures & api_fixtures via wildcard
├── pytest.ini               # testpaths=tests, -v --tb=short
├── requirements.txt         # pytest>=8.0, pytest-playwright>=0.5.0, requests>=2.31, jsonschema>=4.20
├── .gitignore               # venv/, __pycache__/, *.pyc, data/storage_state.json
├── PROMPT.md                # This file — session context
├── LEARNING_NOTES.md        # Interview-ready concept notes
├── api/
│   ├── __init__.py
│   └── booker_client.py     # BookerClient: REST API client using requests.Session (+ create_booking_raw)
├── models/
│   ├── __init__.py
│   └── booking.py           # Typed request/response models: BookingPayload, BookingDates, BookingResponse
├── schemas/
│   ├── __init__.py
│   └── booking_schema.py    # JSON schemas: CREATE_BOOKING, GET_BOOKING, BOOKING_IDS
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
│   ├── test_cars_network.py # 6 network interception tests (mock, spy, error handling)
│   ├── test_booking_api.py  # 6 API tests: full CRUD cycle + response structure validation
│   ├── test_booking_schema.py    # 3 JSON schema validation tests
│   ├── test_booking_parametrize.py # 8 data-driven parameterized tests
│   └── test_booking_negative.py  # 5 negative tests: 404, auth bypass, error handling
├── fixtures/
│   ├── __init__.py
│   ├── page_fixtures.py     # Custom fixtures: login_page, inventory_page, car_page
│   └── api_fixtures.py      # API fixtures: booker_client (session), sample_booking (function)
├── utils/
│   ├── __init__.py
│   ├── logger.py            # get_logger() — structured logging with singleton pattern
│   └── config.py            # Frozen dataclass configs: SAUCE_DEMO, CARS, TIMEOUTS, BOOKER_API
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

### Day 6 — API Test Foundation ✅
- Added `requests>=2.31` to requirements.txt
- Created `BookerApiConfig` frozen dataclass in utils/config.py (base_url, endpoints, credentials, headers)
- Created models/booking.py with typed dataclass models: BookingDates, BookingPayload, BookingResponse
- BookingPayload.to_dict() uses dataclasses.asdict() for recursive nested conversion
- Created api/booker_client.py — REST API client using requests.Session
  - Session persists headers, cookies (auth token), and TCP connections
  - authenticate() stores token via session.cookies.set()
  - Full CRUD: create_booking, get_booking, get_all_booking_ids, update_booking, delete_booking
  - All methods use raise_for_status() for fail-fast error handling
  - Structured logging on all API operations
- Created fixtures/api_fixtures.py with booker_client (session-scoped) and sample_booking (function-scoped)
- Registered api_fixtures in conftest.py via wildcard import
- Wrote 6 API tests in test_booking_api.py:
  - Create booking, get booking, get all IDs, update booking, delete booking, response structure validation
- Used tuple-of-tuples for immutable headers in frozen dataclass config

### Day 7 — API Schema Validation & Data-Driven Tests ✅
- Added `jsonschema>=4.20` to requirements.txt
- Created schemas/booking_schema.py with 3 JSON schemas: CREATE_BOOKING_SCHEMA, GET_BOOKING_SCHEMA, BOOKING_IDS_SCHEMA
- All schemas use `additionalProperties: false` for strict contract validation
- Added `create_booking_raw()` method to BookerClient for raw dict responses
- Wrote 3 schema validation tests in test_booking_schema.py:
  - Create booking schema, get booking schema, get all booking IDs schema
- Wrote 8 parameterized data-driven tests in test_booking_parametrize.py:
  - 5 data variations (standard, zero price, high price, special chars, empty strings)
  - 3 date variations (new year, christmas, one-night stay)
  - Used pytest.mark.parametrize with human-readable `ids=`
- Wrote 5 negative tests in test_booking_negative.py:
  - GET nonexistent booking (404), DELETE nonexistent, UPDATE nonexistent
  - Unauthenticated update fails, unauthenticated delete fails
  - Used pytest.raises with exc_info for status code inspection
  - Unauthenticated tests create separate BookerClient() without calling authenticate()

## Coding Standards Being Followed
- Type hints on all functions and classes
- Page Object Model (POM) with inheritance
- SOLID principles and clean code
- Structured logging via utils/logger.py (DEBUG/INFO levels, %s lazy formatting)
- Centralized config via frozen dataclasses in utils/config.py
- Typed request/response models via frozen dataclasses in models/
- API client pattern with requests.Session (connection pooling, persistent auth)
- JSON schema validation for API contract testing (additionalProperties: false)
- Data-driven tests via pytest.mark.parametrize with ids
- Negative testing with pytest.raises for error path coverage
- decimal library for financial calculations (when needed)

## Day-by-Day Roadmap

### Week 1: Advanced Framework Architecture
- Day 1: Project Scaffold + Base POM ✅
- Day 2: Global Authentication ✅
- Day 3: Custom Pytest Fixtures ✅
- Day 4: Network Interception & Mocking ✅
- Day 5: Logging + Config + Polish ✅

### Week 2: API Testing
- Day 6: API Test Foundation ✅
- Day 7: API Schema Validation & Data-Driven Tests ✅

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
Week 2 complete! Start Day 8: K6 Setup + First Script. Give me step-by-step instructions to:
1. Install K6 and set up performance testing scripts
2. Write first load test against the Restful Booker API
3. Define performance metrics and acceptance thresholds

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
├── conftest.py              # Global fixtures: browser_instance, authenticated_state, auth_context, page
├── pytest.ini               # testpaths=tests, -v --tb=short
├── requirements.txt         # pytest>=8.0, pytest-playwright>=0.5.0
├── .gitignore               # venv/, __pycache__/, *.pyc, data/storage_state.json
├── PROMPT.md                # This file — session context
├── LEARNING_NOTES.md        # Interview-ready concept notes
├── pages/
│   ├── __init__.py
│   ├── base_page.py         # BasePage: common actions (navigate, click, fill, get_text, is_visible)
│   └── login_page.py        # LoginPage: SauceDemo login (inherits BasePage)
├── tests/
│   ├── __init__.py
│   ├── test_login.py        # 3 login tests + local page fixture override (unauthenticated)
│   └── test_inventory.py    # 3 inventory tests using global auth (no login needed)
├── fixtures/
│   └── __init__.py
├── utils/
│   └── __init__.py
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

## Coding Standards Being Followed
- Type hints on all functions and classes
- Page Object Model (POM) with inheritance
- SOLID principles and clean code
- Descriptive logging (adding Day 5)
- decimal library for financial calculations (when needed)

## Day-by-Day Roadmap

### Week 1: Advanced Framework Architecture
- Day 1: Project Scaffold + Base POM ✅
- Day 2: Global Authentication ✅
- Day 3: Custom Pytest Fixtures (auto-inject Page Objects, no manual instantiation)
- Day 4: Network Interception & Mocking (page.route on cars site, mock bad data)
- Day 5: Logging + Config + Polish (structured logging, centralized config, type hints audit)

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
Start Day 3: Custom Pytest Fixtures. Give me step-by-step instructions to:
1. Create custom fixtures that auto-inject Page Objects (LoginPage, InventoryPage, etc.)
2. Remove manual Page Object instantiation from tests
3. Use the fixtures/ directory for organized fixture modules

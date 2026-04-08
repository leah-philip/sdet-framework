from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from pages.login_page import LoginPage

STORAGE_STATE_PATH = Path(__file__).parent / "data" / "storage_state.json"


@pytest.fixture(scope="session")
def browser_instance(pytestconfig) -> Generator[Browser, None, None]:
    headed = pytestconfig.getoption("--headed", default=False)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not headed)
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def authenticated_state(browser_instance: Browser) -> Path:
    context = browser_instance.new_context()
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    page.wait_for_url("**/inventory.html")

    context.storage_state(path=str(STORAGE_STATE_PATH))

    page.close()
    context.close()

    return STORAGE_STATE_PATH


@pytest.fixture()
def auth_context(browser_instance: Browser, authenticated_state: Path) -> Generator[BrowserContext, None, None]:
    context = browser_instance.new_context(storage_state=str(authenticated_state))
    yield context
    context.close()


@pytest.fixture()
def page(auth_context: BrowserContext) -> Generator[Page, None, None]:
    page = auth_context.new_page()
    yield page
    page.close()
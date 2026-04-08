import pytest
from playwright.sync_api import Page, BrowserContext
from typing import Generator
from pages.login_page import LoginPage

@pytest.fixture()
def unauthenticated_context(browser_instance) -> Generator[BrowserContext, None, None]:
    context = browser_instance.new_context()
    yield context
    context.close()

@pytest.fixture()
def page(unauthenticated_context: BrowserContext) -> Generator[Page, None, None]:
    new_page = unauthenticated_context.new_page()
    yield new_page
    new_page.close()

class TestLogin:
    """Tests for the SauceDemo login functionality."""

    def test_successful_login(self, page: Page) -> None:
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        assert "inventory" in page.url

    def test_locked_out_user(self, page: Page) -> None:
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("locked_out_user", "secret_sauce")

        assert "locked out" in login_page.get_error_message().lower()

    def test_invalid_credentials(self, page: Page) -> None:
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("wrong_user", "wrong_pass")

        assert login_page.is_visible(LoginPage.ERROR_MESSAGE)
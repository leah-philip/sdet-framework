from pages.base_page import BasePage
from utils.config import SAUCE_DEMO


class LoginPage(BasePage):
    """Page Object for the SauceDemo login page."""

    URL = SAUCE_DEMO.base_url

    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def open(self) -> None:
        self.navigate(self.URL)

    def login(self, username: str, password: str) -> None:
        self.logger.info("Logging in as '%s'", username)
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
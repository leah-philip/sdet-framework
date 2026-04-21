from playwright.sync_api import Page

from utils.logger import get_logger


class BasePage:
    """Base class for all Page Objects. Centralizes common browser actions."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def navigate(self, url: str) -> None:
        self.logger.info("Navigating to %s", url)
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url

    def click(self, selector: str) -> None:
        self.logger.debug("Clicking '%s'", selector)
        self.page.click(selector)

    def fill(self, selector: str, value: str) -> None:
        self.logger.debug("Filling '%s' with '%s'", selector, value)
        self.page.fill(selector, value)

    def get_text(self, selector: str) -> str:
        return self.page.inner_text(selector)

    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)
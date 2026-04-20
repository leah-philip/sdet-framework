from pages.base_page import BasePage


class CarPage(BasePage):
    """Page Object for the Cars Showroom page."""

    URL = "https://practice.expandtesting.com/cars"

    CAR_CARD = '[data-testid^="car-"]'
    CAR_NAME = '[data-testid="car-name"]'
    CAR_PRICE = '[data-testid="car-price"]'

    def open(self) -> None:
        self.navigate(self.URL)

    def get_car_count(self) -> int:
        return self.page.locator(self.CAR_CARD).count()

    def get_car_names(self) -> list[str]:
        return self.page.locator(self.CAR_NAME).all_text_contents()

    def get_car_prices(self) -> list[str]:
        return self.page.locator(self.CAR_PRICE).all_text_contents()

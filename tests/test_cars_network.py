import json
from utils.config import CARS
from playwright.sync_api import Page, Route, BrowserContext
from typing import Generator
import pytest

from pages.car_page import CarPage

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


class TestCarsNetworkMocking:
    """Tests using network interception to mock API responses."""

    CARS_API_PATTERN = CARS.api_url_pattern

    def _mock_cars_response(self, route: Route, cars: list[dict], status: str = "success") -> None:
        """Helper to fulfill a route with custom car data."""
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"status": status, "cars": cars}),
        )

    def test_page_loads_with_real_data(self, page: Page) -> None:
        """Baseline: verify the page loads cars from the real API."""
        page.goto(CarPage.URL)
        page.locator(CarPage.CAR_CARD).first.wait_for(timeout=5000)

        cards = page.locator(CarPage.CAR_CARD)
        assert cards.count() >0

    def test_mock_empty_car_list(self, page: Page) -> None:
        """Mock an empty API response — UI should handle gracefully."""
        page.route(self.CARS_API_PATTERN, lambda route: self._mock_cars_response(route, []))

        page.goto(CarPage.URL)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        cards = page.locator(CarPage.CAR_CARD)
        assert cards.count() == 0

    def test_mock_zero_price(self, page: Page) -> None:
        """Mock a car with price 0 — test UI display of edge case."""
        fake_cars = [
            {"id": 1, "name": "Ghost Car", "price": "€0", "image": "/img/cars/golf.png"},
        ]
        page.route(self.CARS_API_PATTERN, lambda route: self._mock_cars_response(route, fake_cars))

        page.goto(CarPage.URL)
        page.locator(CarPage.CAR_CARD).first.wait_for(timeout=5000)

        prices = page.locator(CarPage.CAR_PRICE).all_text_contents()
        assert any("0" in price for price in prices)

    def test_mock_negative_price(self, page: Page) -> None:
        """Mock a car with negative price — test UI resilience."""
        fake_cars = [
            {"id": 1, "name": "Broken Car", "price": "-€5,000", "image": "/img/cars/golf.png"},
        ]
        page.route(self.CARS_API_PATTERN, lambda route: self._mock_cars_response(route, fake_cars))

        page.goto(CarPage.URL)
        page.locator(CarPage.CAR_CARD).first.wait_for(timeout=5000)

        prices = page.locator(CarPage.CAR_PRICE).all_text_contents()
        assert any("-" in price for price in prices)

    def test_mock_api_server_error(self, page: Page) -> None:
        """Mock a 500 server error — UI fails silently with no error message."""
        page.route(
            self.CARS_API_PATTERN,
            lambda route: route.fulfill(status=500, body="Internal Server Error"),
        )

        page.goto(CarPage.URL)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        cards = page.locator(CarPage.CAR_CARD)
        assert cards.count() == 0

    def test_spy_on_api_request(self, page: Page) -> None:
        """Intercept and inspect the actual API request without modifying it."""
        captured_requests: list[str] = []

        def spy_handler(route: Route) -> None:
            captured_requests.append(route.request.url)
            route.continue_()

        page.route(self.CARS_API_PATTERN, spy_handler)

        page.goto(CarPage.URL)
        page.locator(CarPage.CAR_CARD).first.wait_for(timeout=5000)

        assert len(captured_requests) > 0
        assert "cars" in captured_requests[0].lower()
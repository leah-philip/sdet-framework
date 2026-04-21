from dataclasses import dataclass


@dataclass(frozen=True)
class SauceDemoConfig:
    base_url: str = "https://www.saucedemo.com"
    inventory_url: str = "https://www.saucedemo.com/inventory.html"
    username: str = "standard_user"
    password: str = "secret_sauce"


@dataclass(frozen=True)
class CarsConfig:
    base_url: str = "https://practice.expandtesting.com/cars"
    api_url_pattern: str = "**/api/cars"


@dataclass(frozen=True)
class TimeoutConfig:
    default: int = 5000
    long: int = 15000
    short: int = 2000


SAUCE_DEMO = SauceDemoConfig()
CARS = CarsConfig()
TIMEOUTS = TimeoutConfig()
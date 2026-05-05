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

@dataclass(frozen=True)
class BookerApiConfig:
    base_url: str = "https://restful-booker.herokuapp.com"
    auth_endpoint: str = "/auth"
    booking_endpoint: str = "/booking"
    username: str = "admin"
    password: str = "password123"
    default_headers: tuple[tuple[str, str], ...] = (
        ("Content-Type", "application/json"),
        ("Accept", "application/json"),
    )
    
BOOKER_API = BookerApiConfig()
SAUCE_DEMO = SauceDemoConfig()
CARS = CarsConfig()
TIMEOUTS = TimeoutConfig()
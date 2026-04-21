from typing import Generator

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.car_page import CarPage


@pytest.fixture()
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture()
def inventory_page(page: Page) -> InventoryPage:
    inventory = InventoryPage(page)
    inventory.open()
    return inventory


@pytest.fixture()
def car_page(page: Page) -> CarPage:
    car = CarPage(page)
    car.open()
    return car
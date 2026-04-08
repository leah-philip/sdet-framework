from playwright.sync_api import Page


class TestInventory:
    """Tests that rely on being already logged in via global auth."""

    def test_inventory_page_loads(self, page: Page) -> None:
        page.goto("https://www.saucedemo.com/inventory.html")
        assert page.is_visible("[data-test='inventory-list']")

    def test_inventory_has_items(self, page: Page) -> None:
        page.goto("https://www.saucedemo.com/inventory.html")
        items = page.locator("[data-test='inventory-item']")
        assert items.count() > 0

    def test_page_title(self, page: Page) -> None:
        page.goto("https://www.saucedemo.com/inventory.html")
        assert "Swag Labs" in page.title()
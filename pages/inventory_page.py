from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page Object for the SauceDemo inventory page."""

    URL = "https://www.saucedemo.com/inventory.html"

    INVENTORY_LIST = "[data-test='inventory-list']"
    INVENTORY_ITEM = "[data-test='inventory-item']"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    CART_BADGE = "[data-test='shopping-cart-badge']"
    ADD_TO_CART_BACKPACK = "[data-test='add-to-cart-sauce-labs-backpack']"
    REMOVE_BACKPACK = "[data-test='remove-sauce-labs-backpack']"

    def open(self) -> None:
        self.navigate(self.URL)

    def get_item_count(self) -> int:
        return self.page.locator(self.INVENTORY_ITEM).count()

    def add_backpack_to_cart(self) -> None:
        self.click(self.ADD_TO_CART_BACKPACK)

    def remove_backpack_from_cart(self) -> None:
        self.click(self.REMOVE_BACKPACK)

    def get_cart_count(self) -> str:
        return self.get_text(self.CART_BADGE)

    def sort_by(self, value: str) -> None:
        self.page.select_option(self.SORT_DROPDOWN, value)

    def get_item_names(self) -> list[str]:
        return self.page.locator(self.INVENTORY_ITEM).all_inner_texts()
from pages.inventory_page import InventoryPage


class TestInventory:
    """Tests that rely on being already logged in via global auth."""

    def test_inventory_page_loads(self, inventory_page: InventoryPage) -> None:
        assert inventory_page.is_visible(InventoryPage.INVENTORY_LIST)

    def test_inventory_has_items(self, inventory_page: InventoryPage) -> None:
        assert inventory_page.get_item_count() > 0

    def test_page_title(self, inventory_page: InventoryPage) -> None:
        assert "Swag Labs" in inventory_page.get_title()

    def test_add_item_to_cart(self, inventory_page: InventoryPage) -> None:
        inventory_page.add_backpack_to_cart()
        assert inventory_page.get_cart_count() == "1"

    def test_remove_item_from_cart(self, inventory_page: InventoryPage) -> None:
        inventory_page.add_backpack_to_cart()
        inventory_page.remove_backpack_from_cart()
        assert not inventory_page.is_visible(InventoryPage.CART_BADGE)
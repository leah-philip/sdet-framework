import pytest
import requests

from api.booker_client import BookerClient
from models.booking import BookingPayload, BookingDates


class TestBookingNegative:

    def test_get_nonexistent_booking_returns_404(
        self, booker_client: BookerClient
    ) -> None:
        with pytest.raises(requests.HTTPError) as exc_info:
            booker_client.get_booking(999999999)

        assert exc_info.value.response.status_code == 404

    def test_delete_nonexistent_booking_returns_error(
        self, booker_client: BookerClient
    ) -> None:
        with pytest.raises(requests.HTTPError):
            booker_client.delete_booking(999999999)

    def test_update_nonexistent_booking_returns_error(
        self, booker_client: BookerClient
    ) -> None:
        payload = BookingPayload(
            firstname="Ghost",
            lastname="User",
            totalprice=100,
            depositpaid=True,
            bookingdates=BookingDates(
                checkin="2026-09-01",
                checkout="2026-09-05",
            ),
        )

        with pytest.raises(requests.HTTPError):
            booker_client.update_booking(999999999, payload)

    def test_unauthenticated_update_fails(self) -> None:
        unauth_client = BookerClient()

        payload = BookingPayload(
            firstname="Unauth",
            lastname="User",
            totalprice=100,
            depositpaid=True,
            bookingdates=BookingDates(
                checkin="2026-09-01",
                checkout="2026-09-05",
            ),
        )

        created = unauth_client.create_booking(payload)

        with pytest.raises(requests.HTTPError):
            unauth_client.update_booking(created.bookingid, payload)

    def test_unauthenticated_delete_fails(self) -> None:
        unauth_client = BookerClient()

        payload = BookingPayload(
            firstname="Unauth",
            lastname="Delete",
            totalprice=100,
            depositpaid=True,
            bookingdates=BookingDates(
                checkin="2026-09-01",
                checkout="2026-09-05",
            ),
        )

        created = unauth_client.create_booking(payload)

        with pytest.raises(requests.HTTPError):
            unauth_client.delete_booking(created.bookingid)
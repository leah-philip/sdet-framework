import pytest
from api.booker_client import BookerClient
from models.booking import BookingPayload, BookingDates


@pytest.fixture(scope="session")
def booker_client() -> BookerClient:
    client = BookerClient()
    client.authenticate()
    return client


@pytest.fixture()
def sample_booking() -> BookingPayload:
    return BookingPayload(
        firstname="James",
        lastname="Brown",
        totalprice=150,
        depositpaid=True,
        bookingdates=BookingDates(
            checkin="2026-06-01",
            checkout="2026-06-10",
        ),
        additionalneeds="Breakfast",
    )
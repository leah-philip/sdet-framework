import pytest

from api.booker_client import BookerClient
from models.booking import BookingPayload, BookingDates


class TestBookingParametrized:

    @pytest.mark.parametrize(
        "firstname, lastname, totalprice, depositpaid, additional",
        [
            ("Alice", "Smith", 100, True, "Breakfast"),
            ("Bob", "Jones", 0, False, "None"),
            ("Charlie", "Lee", 999999, True, "Late checkout"),
            ("Diana", "O'Connor", 50, True, "Extra pillows"),
            ("", "", 1, False, ""),
        ],
        ids=[
            "standard_booking",
            "zero_price",
            "high_price",
            "special_characters",
            "empty_strings",
        ],
    )
    def test_create_booking_with_various_data(
        self,
        booker_client: BookerClient,
        firstname: str,
        lastname: str,
        totalprice: int,
        depositpaid: bool,
        additional: str,
    ) -> None:
        payload = BookingPayload(
            firstname=firstname,
            lastname=lastname,
            totalprice=totalprice,
            depositpaid=depositpaid,
            bookingdates=BookingDates(
                checkin="2026-08-01",
                checkout="2026-08-10",
            ),
            additionalneeds=additional,
        )

        result = booker_client.create_booking(payload)

        assert result.bookingid > 0
        assert result.booking["firstname"] == firstname
        assert result.booking["lastname"] == lastname
        assert result.booking["totalprice"] == totalprice

    @pytest.mark.parametrize(
        "checkin, checkout",
        [
            ("2026-01-01", "2026-01-10"),
            ("2026-12-25", "2026-12-31"),
            ("2027-06-15", "2027-06-16"),
        ],
        ids=["new_year", "christmas", "one_night_stay"],
    )
    def test_create_booking_with_various_dates(
        self,
        booker_client: BookerClient,
        checkin: str,
        checkout: str,
    ) -> None:
        payload = BookingPayload(
            firstname="DateTest",
            lastname="User",
            totalprice=100,
            depositpaid=True,
            bookingdates=BookingDates(checkin=checkin, checkout=checkout),
        )

        result = booker_client.create_booking(payload)

        assert result.bookingid > 0
        assert result.booking["bookingdates"]["checkin"] == checkin
        assert result.booking["bookingdates"]["checkout"] == checkout
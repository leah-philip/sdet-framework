from api.booker_client import BookerClient
from models.booking import BookingPayload, BookingDates


class TestBookingAPI:

    def test_create_booking(
        self, booker_client: BookerClient, sample_booking: BookingPayload
    ) -> None:
        result = booker_client.create_booking(sample_booking)

        assert result.bookingid > 0
        assert result.booking["firstname"] == sample_booking.firstname
        assert result.booking["lastname"] == sample_booking.lastname
        assert result.booking["totalprice"] == sample_booking.totalprice

    def test_get_booking(
        self, booker_client: BookerClient, sample_booking: BookingPayload
    ) -> None:
        created = booker_client.create_booking(sample_booking)
        fetched = booker_client.get_booking(created.bookingid)

        assert fetched["firstname"] == sample_booking.firstname
        assert fetched["lastname"] == sample_booking.lastname
        assert fetched["totalprice"] == sample_booking.totalprice
        assert fetched["depositpaid"] == sample_booking.depositpaid

    def test_get_all_booking_ids(self, booker_client: BookerClient) -> None:
        booking_ids = booker_client.get_all_booking_ids()

        assert isinstance(booking_ids, list)
        assert len(booking_ids) > 0
        assert "bookingid" in booking_ids[0]

    def test_update_booking(
        self, booker_client: BookerClient, sample_booking: BookingPayload
    ) -> None:
        created = booker_client.create_booking(sample_booking)

        updated_payload = BookingPayload(
            firstname="Jane",
            lastname="Doe",
            totalprice=250,
            depositpaid=False,
            bookingdates=BookingDates(
                checkin="2026-07-01",
                checkout="2026-07-15",
            ),
            additionalneeds="Lunch",
        )

        updated = booker_client.update_booking(created.bookingid, updated_payload)

        assert updated["firstname"] == "Jane"
        assert updated["lastname"] == "Doe"
        assert updated["totalprice"] == 250

    def test_delete_booking(
        self, booker_client: BookerClient, sample_booking: BookingPayload
    ) -> None:
        created = booker_client.create_booking(sample_booking)
        status_code = booker_client.delete_booking(created.bookingid)

        assert status_code == 201  # Restful Booker returns 201 on delete (quirk)

    def test_create_booking_validates_response_structure(
        self, booker_client: BookerClient, sample_booking: BookingPayload
    ) -> None:
        result = booker_client.create_booking(sample_booking)

        assert hasattr(result, "bookingid")
        assert hasattr(result, "booking")
        assert isinstance(result.bookingid, int)
        assert isinstance(result.booking, dict)
        assert "firstname" in result.booking
        assert "lastname" in result.booking
        assert "totalprice" in result.booking
        assert "depositpaid" in result.booking
        assert "bookingdates" in result.booking
from jsonschema import validate

from api.booker_client import BookerClient
from models.booking import BookingPayload
from schemas.booking_schema import (
    CREATE_BOOKING_SCHEMA,
    GET_BOOKING_SCHEMA,
    BOOKING_IDS_SCHEMA,
)


class TestBookingSchema:

    def test_create_booking_matches_schema(
        self, booker_client: BookerClient, sample_booking: BookingPayload
    ) -> None:
        raw_response = booker_client.create_booking_raw(sample_booking)

        validate(instance=raw_response, schema=CREATE_BOOKING_SCHEMA)

    def test_get_booking_matches_schema(
        self, booker_client: BookerClient, sample_booking: BookingPayload
    ) -> None:
        created = booker_client.create_booking(sample_booking)
        fetched = booker_client.get_booking(created.bookingid)

        validate(instance=fetched, schema=GET_BOOKING_SCHEMA)

    def test_get_all_booking_ids_matches_schema(
        self, booker_client: BookerClient
    ) -> None:
        booking_ids = booker_client.get_all_booking_ids()

        validate(instance=booking_ids, schema=BOOKING_IDS_SCHEMA)
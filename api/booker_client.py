import requests
from utils.logger import get_logger
from utils.config import BOOKER_API
from models.booking import BookingPayload, BookingResponse


class BookerClient:

    def __init__(self) -> None:
        self.base_url: str = BOOKER_API.base_url
        self.session: requests.Session = requests.Session()
        self.session.headers.update(dict(BOOKER_API.default_headers))
        self.logger = get_logger(self.__class__.__name__)

    def authenticate(self) -> str:
        self.logger.info("Authenticating with Booker API")
        response = self.session.post(
            f"{self.base_url}{BOOKER_API.auth_endpoint}",
            json={"username": BOOKER_API.username, "password": BOOKER_API.password},
        )
        response.raise_for_status()
        token: str = response.json()["token"]
        self.session.cookies.set("token", token)
        self.logger.info("Authentication successful, token stored")
        return token

    def create_booking(self, payload: BookingPayload) -> BookingResponse:
        self.logger.info(
            "Creating booking for %s %s", payload.firstname, payload.lastname
        )
        response = self.session.post(
            f"{self.base_url}{BOOKER_API.booking_endpoint}",
            json=payload.to_dict(),
        )
        response.raise_for_status()
        data: dict = response.json()
        self.logger.info("Booking created with ID: %s", data["bookingid"])
        return BookingResponse(bookingid=data["bookingid"], booking=data["booking"])

    def get_booking(self, booking_id: int) -> dict:
        self.logger.info("Getting booking %s", booking_id)
        response = self.session.get(
            f"{self.base_url}{BOOKER_API.booking_endpoint}/{booking_id}",
        )
        response.raise_for_status()
        return response.json()

    def get_all_booking_ids(self) -> list[dict]:
        self.logger.info("Getting all booking IDs")
        response = self.session.get(
            f"{self.base_url}{BOOKER_API.booking_endpoint}",
        )
        response.raise_for_status()
        return response.json()

    def update_booking(self, booking_id: int, payload: BookingPayload) -> dict:
        self.logger.info("Updating booking %s", booking_id)
        response = self.session.put(
            f"{self.base_url}{BOOKER_API.booking_endpoint}/{booking_id}",
            json=payload.to_dict(),
        )
        response.raise_for_status()
        return response.json()

    def delete_booking(self, booking_id: int) -> int:
        self.logger.info("Deleting booking %s", booking_id)
        response = self.session.delete(
            f"{self.base_url}{BOOKER_API.booking_endpoint}/{booking_id}",
        )
        response.raise_for_status()
        return response.status_code
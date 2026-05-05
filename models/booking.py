from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class BookingDates:
    checkin: str
    checkout: str


@dataclass(frozen=True)
class BookingPayload:
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str = "Breakfast"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class BookingResponse:
    bookingid: int
    booking: dict
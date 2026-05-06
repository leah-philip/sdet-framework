CREATE_BOOKING_SCHEMA: dict = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": {
            "type": "object",
            "required": [
                "firstname",
                "lastname",
                "totalprice",
                "depositpaid",
                "bookingdates",
            ],
            "properties": {
                "firstname": {"type": "string"},
                "lastname": {"type": "string"},
                "totalprice": {"type": "integer"},
                "depositpaid": {"type": "boolean"},
                "bookingdates": {
                    "type": "object",
                    "required": ["checkin", "checkout"],
                    "properties": {
                        "checkin": {"type": "string"},
                        "checkout": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
                "additionalneeds": {"type": "string"},
            },
            "additionalProperties": False,
        },
    },
    "additionalProperties": False,
}

GET_BOOKING_SCHEMA: dict = {
    "type": "object",
    "required": [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates",
    ],
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "totalprice": {"type": "integer"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "required": ["checkin", "checkout"],
            "properties": {
                "checkin": {"type": "string"},
                "checkout": {"type": "string"},
            },
            "additionalProperties": False,
        },
        "additionalneeds": {"type": "string"},
    },
    "additionalProperties": False,
}

BOOKING_IDS_SCHEMA: dict = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["bookingid"],
        "properties": {
            "bookingid": {"type": "integer"},
        },
        "additionalProperties": False,
    },
}
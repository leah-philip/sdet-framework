import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = "https://restful-booker.herokuapp.com";

export const options = {
  stages: [
    { duration: "10s", target: 5 },
    { duration: "20s", target: 5 },
    { duration: "10s", target: 0 },
  ],
  thresholds: {
    http_req_duration: ["p(95)<2000"],
    http_req_failed: ["rate<0.05"],
    checks: ["rate>0.95"],
  },
};

function getAuthToken() {
  const payload = JSON.stringify({
    username: "admin",
    password: "password123",
  });

  const params = {
    headers: { "Content-Type": "application/json" },
  };

  const res = http.post(`${BASE_URL}/auth`, payload, params);

  check(res, {
    "auth status is 200": (r) => r.status === 200,
    "auth returns token": (r) => r.json("token") !== undefined,
  });

  return res.json("token");
}

export function setup() {
  const token = getAuthToken();
  return { token: token };
}

export default function (data) {
  const params = {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Cookie: `token=${data.token}`,
    },
  };

  const bookingPayload = JSON.stringify({
    firstname: "Perf",
    lastname: "Test",
    totalprice: 100,
    depositpaid: true,
    bookingdates: {
      checkin: "2026-08-01",
      checkout: "2026-08-10",
    },
    additionalneeds: "Breakfast",
  });

  // Create a booking
  const createRes = http.post(
    `${BASE_URL}/booking`,
    bookingPayload,
    params
  );

  check(createRes, {
    "create status is 200": (r) => r.status === 200,
    "create returns bookingid": (r) => r.json("bookingid") !== undefined,
  });

  const bookingId = createRes.json("bookingid");

  // Get the booking
  if (bookingId) {
    const getRes = http.get(
      `${BASE_URL}/booking/${bookingId}`,
      params
    );

    check(getRes, {
      "get status is 200": (r) => r.status === 200,
      "get returns firstname": (r) => r.json("firstname") === "Perf",
    });
  }

  // List all booking IDs
  const listRes = http.get(`${BASE_URL}/booking`, params);

  check(listRes, {
    "list status is 200": (r) => r.status === 200,
    "list returns array": (r) => Array.isArray(r.json()),
  });

  sleep(1);
}
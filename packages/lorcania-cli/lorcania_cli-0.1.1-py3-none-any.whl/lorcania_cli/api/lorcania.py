from typing import Any, Literal, Dict
from urllib.parse import unquote, urljoin
import requests


ExpectedResponse = Literal["json"] | Literal["plain"]
SupportedMethod = Literal["get"] | Literal["post"]


class AuthenticationError(Exception):
    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)


class LorcaniaAPI:
    def __init__(
        self, email: str, password: str, base_url="https://lorcania.com/"
    ) -> None:
        self._base_url = base_url
        self._session = requests.Session()

        self._get("/login", "plain")
        try:
            self._post(
                "/login", json={"email": email, "password": password, "remember": ""}
            )
        except requests.HTTPError as err:
            if err.response.status_code == 422:
                raise AuthenticationError()
            else:
                raise err

    def collection(self):
        return self._get("/api/collection")

    def cards(self):
        return self._post(
            "/api/cardsSearch",
            json={
                "colors": [],
                "sets": [],
                "traits": [],
                "keywords": [],
                "costs": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "inkwell": [],
                "rarity": [],
                "language": "English",
                "options": [],
                "sorting": "default",
            },
        )

    def _get(self, path: str, expected_response: ExpectedResponse = "json"):
        return self._request("get", path, expected_response=expected_response)

    def _post(self, path: str, json: Dict[str, Any] | None = None):
        return self._request("post", path, json=json, expected_response="json")

    def _request(
        self,
        method: SupportedMethod,
        path: str,
        json: Dict[str, Any] | None = None,
        expected_response: ExpectedResponse = "json",
    ):
        r = self._session.request(
            method, urljoin(self._base_url, path), headers=self._headers(), json=json
        )
        r.raise_for_status()
        if expected_response == "json":
            return r.json()
        else:
            return r.text

    def _headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-XSRF-TOKEN": self._xsrf_token(),
        }

    def _xsrf_token(self):
        if "XSRF-TOKEN" in self._session.cookies:
            return unquote(self._session.cookies["XSRF-TOKEN"])
        else:
            return None

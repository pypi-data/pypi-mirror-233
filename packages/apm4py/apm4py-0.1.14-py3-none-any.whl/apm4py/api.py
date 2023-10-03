"""
generic api requests including authorization
"""

from typing import Optional

import requests

from apm4py.decorators import handle_response, expect_json
from apm4py.structures import User


def _create_authorization_header(method: str, token: str) -> dict:
    return {"Authorization": f"{method} {token}"}


def get_token(scheme: str, host: str, instance: int, **kwargs) -> str:
    headers = {**kwargs.pop("headers", dict())}

    port = "" if host != "localhost" else ":4424"

    r = requests.get(
        f"{scheme}://{host}{port}/instance/{instance}/user/analyst/token",
        headers=headers,
        **kwargs,
    )
    r.raise_for_status()
    token = r.content.decode()
    return token


# TODO consider certificate passing for TLS
# TODO consider letting kwargs replace authentication header
class API:
    """An api for a specific user at a Lana deployment.

    All required information to make authenticated requests to the api are
    passed during construction and stored. Named request methods are
    provided as wrappers around requests library methods, that add required
    header fields. Additional headers to the requests library methods can be
    passed as keyword arguments.

    When constructed a request to the lana api is made in order to
    retrieve user information.

    Attributes:
        url (str):
            A string denoting the URL of the lana api, including the
            application root.
        user:
            A User dataclass encapsulating the user of the api information.
        headers:
            A dictionary representing the authorization header used for every
            request by default.
    """

    # TODO document
    def __init__(
        self,
        scheme: str,
        host: str,
        instance: int = 1,
        token: Optional[str] = None,
        port: Optional[int] = None,
        application_root: Optional[str] = None,
        **kwargs,
    ):
        """Construct a configured Appian API.

        Args:
            scheme:
                A string denoting the scheme of the api URL.
            host:
                A string denoting the APM API host.
            token:
                A string denoting the user authentication token without the
                preceding "API-Key".
            port:
                (optional) A string or integer denoting the port of the
                lana api.
            application_root:
                (optional) A string denoting the application root. Only required
                if your lana api is placed outside the URL root, e.g. "/lana-api"
                instead of "/". Has to start with a slash.
            **kwargs:
                Keyword arguments to pass to requests for the initial
                request retrieving user information.
        """

        self.url = (
            f"{scheme}://{host}"
            + (f":{port}" if port else "")
            + (f":{application_root}" if application_root else "").replace("//", "/")
        ).strip("/")
        self.token = token if token else get_token(scheme, host, instance)
        auth_method = "Bearer" if not "lanalabs.com" in self.url else "API-Key"
        self.headers = _create_authorization_header(auth_method, self.token)
        self.user = self.get_user(**kwargs)

    @expect_json
    @handle_response
    def get_user_information(self, **kwargs) -> dict:
        r = requests.get(
            self.url + "/api/users/by-token", headers=self.headers, **kwargs
        )
        r.raise_for_status()
        return r

    def get_user(self, **kwargs) -> User:
        user_info = self.get_user_information(**kwargs)
        return User(
            user_id=user_info.get("id"),
            organization_id=user_info.get("organizationId"),
            api_key=user_info.get("apiKey"),
            role=user_info.get("role"),
        )

    def _request(self, method, route, headers=None, additional_headers=None, **kwargs):
        headers = {
            **self.headers,
            **(additional_headers or dict()),
            **(headers or dict()),
        }
        return requests.request(method, self.url + route, headers=headers, **kwargs)

    @handle_response
    def get(self, route, additional_headers=None, **kwargs):
        return self._request("GET", route, additional_headers, **kwargs)

    @handle_response
    def post(self, route, additional_headers=None, **kwargs):
        return self._request("POST", route, additional_headers, **kwargs)

    @handle_response
    def patch(self, route, additional_headers=None, **kwargs):
        return self._request("PATCH", route, additional_headers, **kwargs)

    @handle_response
    def delete(self, route, additional_headers=None, **kwargs):
        return self._request("DELETE", route, additional_headers, **kwargs)

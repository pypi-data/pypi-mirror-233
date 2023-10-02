import logging
import os
import re
from json import JSONDecodeError
from typing import Any, Dict, Iterator, Mapping, Optional, Union

import requests
from requests.adapters import HTTPAdapter, Retry
from requests.cookies import RequestsCookieJar

from servehub.__about__ import __version__
from servehub.exceptions import (
    ServeHubError,
    ApiError,
    ApiNotDeployedError,
    ApiNotFoundError,
)

_LOGGER = logging.getLogger(__name__)

class Client:
    def __init__(self, api_token: Optional[str] = None) -> None:
        super().__init__()
        # Client is instantiated at import time, so do as little as possible.
        # This includes resolving environment variables -- they might be set programmatically.
        self.api_token = api_token
        self.base_url = os.environ.get(
            "SERVEHUB_API_URL", "https://servehub.co/api"
        )

        # TODO: make thread safe
        self.read_session = _create_session()
        read_retries = Retry(
            total=5,
            backoff_factor=2,
            # Only retry 500s on GET so we don't unintionally mutute data
            allowed_methods=["GET"],
            # https://support.cloudflare.com/hc/en-us/articles/115003011431-Troubleshooting-Cloudflare-5XX-errors
            status_forcelist=[
                429,
                500,
                503,
                504,
                520,
                521,
                522,
                523,
                524,
                526,
                527,
            ],
        )
        self.read_session.mount("http://", HTTPAdapter(max_retries=read_retries))
        self.read_session.mount("https://", HTTPAdapter(max_retries=read_retries))

        self.write_session = _create_session()
        write_retries = Retry(
            total=5,
            backoff_factor=2,
            allowed_methods=["POST", "PUT"],
            # Only retry POST/PUT requests on rate limits, so we don't unintionally mutute data
            status_forcelist=[429],
        )
        self.write_session.mount("http://", HTTPAdapter(max_retries=write_retries))
        self.write_session.mount("https://", HTTPAdapter(max_retries=write_retries))

        self.api_session = _create_session()
        api_retries = Retry(
            total=5,
            backoff_factor=2,
            allowed_methods=["POST", "PUT"],
            # Only retry POST/PUT requests on rate limits, so we don't unintionally mutute data
            status_forcelist=[429],
        )
        self.api_session.mount("http://", HTTPAdapter(max_retries=api_retries))
        self.api_session.mount("https://", HTTPAdapter(max_retries=api_retries))

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        # from requests.Session
        if method in ["GET", "OPTIONS"]:
            kwargs.setdefault("allow_redirects", True)
        if method in ["HEAD"]:
            kwargs.setdefault("allow_redirects", False)
        kwargs.setdefault("headers", {})
        kwargs["headers"].update(self._headers())
        session = self.read_session
        if method in ["POST", "PUT", "DELETE", "PATCH"]:
            session = self.write_session
        resp = session.request(method, self.base_url + path, **kwargs)
        if 400 <= resp.status_code < 600:
            try:
                # Error from the serve hub API
                raise ServeHubError(resp.json()["detail"])
            except (JSONDecodeError, KeyError):
                pass
            raise ServeHubError(f"HTTP error: {resp.status_code, resp.reason}")
        return resp

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Token {self._api_token()}",
            "User-Agent": f"servehub-python/{__version__}",
        }

    def _api_token(self) -> str:
        token = self.api_token
        # Evaluate lazily in case environment variable is set with dotenv, or something
        if token is None:
            token = os.environ.get("SERVEHUB_API_TOKEN")
        if not token:
            raise ServeHubError(
                """No API token provided. You need to set the SERVEHUB_API_TOKEN environment variable or create a client with `servehub.Client(api_token=...)`.

You can find your API key on https://servehub.co/settings"""
            )
        return token

    def run(
        self, api: str, input: Dict[str, Any], suffix: Optional[str], **kwargs
    ) -> Union[Any, Iterator[Any]]:
        """
        Run a ML API and wait for its output.

        Args:
            api: The ML API to run, in the format `owner/api_name:deployment_name`
            input: The input to the model, as a dictionary
            suffix: The suffix to add to the API url
        Returns:
            The output of the model
        """
        # Split model_version into owner, name, version in format owner/name:version
        m = re.match("^(?P<owner>[^/]+)/(?P<api_name>[^:]+):(?P<deployment_name>.+)$", api)
        if not m:
            raise ApiNotFoundError(
                f"Invalid api: {api}. Expected format: owner/api_name:deployment_name"
            )
        # owner, api_name, deployment_name = m.group("owner"), m.group("api_name"), m.group("deployment_name")

        # get the deployment url
        resp = self._request("GET", f"/v2/deployment_url?api={api}")
        # check if error
        if resp.status_code == 404:
            raise ApiNotFoundError(resp.json()["error"])
        elif resp.status_code == 502:
            # Reason: 502 usually indicates that one server on the internet received an invalid response from
            # another server. In the context of a platform that helps users deploy an ML API on their own
            # infrastructure, if there's a deployment error on the user's end, it could be seen as the platform
            # receiving an invalid response from the user's infrastructure (acting as another server). Using this
            # status would suggest that while the platform is functioning correctly, there's an issue with the
            # "downstream" ML API service on the user's end.
            raise ServeHubError(resp.json()["error"])
        elif resp.status_code == 409:
            # Reason: 409 suggest that the current state of the ML API (not deployed) is in conflict with the desired
            # action (running the API).
            raise ApiNotDeployedError(resp.json()["error"])

        # Some other error
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ServeHubError(str(e))

        deployment_url = resp.json()["deployment_url"]

        # Run the API
        session = self.api_session
        if suffix:
            deployment_url += f"/{suffix}"


        if "as_json" in kwargs and kwargs["as_json"]:
            kwargs.pop("as_json")
            resp = session.request("POST", deployment_url, json=input, **kwargs)
        else:
            resp = session.request(
                "POST", deployment_url, json=input, **kwargs
            )
        if 400 <= resp.status_code < 600:
            try:
                raise ApiError(resp.json()["detail"])
            except (JSONDecodeError, KeyError):
                pass
            raise ApiError(f"HTTP error: {resp.status_code, resp.reason}")

        try:
            return resp.json()
        except (JSONDecodeError, KeyError):
            return resp


class _NonpersistentCookieJar(RequestsCookieJar):
    """
    A cookie jar that doesn't persist cookies between requests.
    """

    def set(self, name, value, **kwargs) -> None:
        return

    def set_cookie(self, cookie, *args, **kwargs) -> None:
        return


def _create_session() -> requests.Session:
    s = requests.Session()
    s.cookies = _NonpersistentCookieJar()
    return s

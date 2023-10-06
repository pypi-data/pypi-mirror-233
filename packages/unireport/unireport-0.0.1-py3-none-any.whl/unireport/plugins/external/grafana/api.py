import warnings
from typing import Tuple, Union
from urllib.parse import parse_qs, urlparse

import requests
from urllib3.exceptions import InsecureRequestWarning

from unireport.plugins.external.grafana.client import GrafanaClient
from unireport.utils import as_bool

DEFAULT_TIMEOUT = 10.0


class GrafanaAPI:
    def __init__(
        self,
        auth=None,
        host="localhost",
        port=None,
        url_path_prefix="",
        protocol="http",
        verify=True,
        timeout=DEFAULT_TIMEOUT,
    ):
        self.client = GrafanaClient(
            auth,
            host=host,
            port=port,
            url_path_prefix=url_path_prefix,
            protocol=protocol,
            verify=verify,
            timeout=timeout,
        )
        self.url = None

    @classmethod
    def from_url(
        cls,
        url: str = None,
        credential: Union[str, Tuple[str, str], requests.auth.AuthBase] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        """
        Factory method to create a `GrafanaApi` instance from a URL.

        Accepts an optional credential, which is either an authentication
        token, or a tuple of (username, password).
        """

        # Sanity checks and defaults.
        if url is None:
            url = "http://admin:admin@localhost:3000"

        if credential is not None and not isinstance(
            credential, (str, Tuple, requests.auth.AuthBase)
        ):
            raise TypeError(f"Argument 'credential' has wrong type: {type(credential)}")

        original_url = url
        url = urlparse(url)

        # Use username and password from URL.
        if credential is None and url.username:
            credential = (url.username, url.password)

        # Optionally turn off SSL verification.
        verify = as_bool(parse_qs(url.query).get("verify", [True])[0])
        if verify is False:
            warnings.filterwarnings("ignore", category=InsecureRequestWarning)

        grafana = cls(
            credential,
            protocol=url.scheme,
            host=url.hostname,
            port=url.port,
            url_path_prefix=url.path.lstrip("/"),
            verify=verify,
            timeout=timeout,
        )
        grafana.url = original_url

        return grafana

    def query_raw(self, url, params=None):
        response = self.client.get(url, params=params)
        return response

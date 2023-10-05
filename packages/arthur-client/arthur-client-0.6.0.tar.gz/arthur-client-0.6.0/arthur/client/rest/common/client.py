from typing import Optional, Any, Union, Dict, List, Tuple
from http import HTTPStatus
from requests.cookies import RequestsCookieJar
from requests import Response

# import http client
from arthur.client.http.requests import HTTPClient


PATH_PREFIX = "/"


class ArthurClientCommon:
    """
    A Python client to interact with the Arthur API Common
    """

    def __init__(self, http_client: HTTPClient):
        """
        Create a new ArthurClientCommon from an HTTPClient

        :param http_client: the :class:`~arthurai.client.http.requests.HTTPClient` to use for underlying requests
        """
        self.http_client = http_client
        self.http_client.set_path_prefix(PATH_PREFIX)

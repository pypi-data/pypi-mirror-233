import logging
import os
from distutils.util import strtobool
from getpass import getpass
from platform import system
from typing import Optional

from arthur.client.auth.helpers import get_current_org, user_login
from arthur.client.auth.refresh import AuthRefresher
from arthur.client.http.requests import HTTPClient
from arthur.common.exceptions import MissingParameterError, UserValueError
from arthur.client.version import __version__

# import sub-clients
from arthur.client.rest.admin.client import ArthurAdminClient
from arthur.client.rest.alerts.client import ArthurAlertsClient
from arthur.client.rest.bench.client import ArthurBenchClient
from arthur.client.rest.common.client import ArthurClientCommon
from arthur.client.rest.enrichments.client import ArthurEnrichmentsClient
from arthur.client.rest.inferences.client import ArthurInferencesClient
from arthur.client.rest.insights.client import ArthurInsightsClient
from arthur.client.rest.metrics.client import ArthurMetricsClient
from arthur.client.rest.model_groups.client import ArthurModelGroupsClient
from arthur.client.rest.models.client import ArthurModelsClient
from arthur.client.rest.query.client import ArthurQueryClient
# end import sub-clients

UNKNOWN_ORG_ID = "unknown-org"
ORG_ID_HEADER = "Arthur-Organization-ID"


logger = logging.getLogger(__name__)


class ArthurClient:
    def __init__(
        self,
        url: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
        organization_id: Optional[str] = None,
        verify_ssl: Optional[bool] = None,
        allow_insecure: bool = False,
        offline: bool = False,
    ):
        """
        TODO!
        """
        # basic values
        if url is None:
            url = os.getenv("ARTHUR_API_URL")
        if url is None:
            raise MissingParameterError(
                "You must provide a URL through the 'url' parameter or the ARTHUR_API_URL "
                "environment variable"
            )
        if verify_ssl is None:  # if not provided
            # read from env var, or default to True if not present
            try:
                verify_ssl = bool(strtobool(os.getenv("ARTHUR_VERIFY_SSL", "true")))
            except ValueError:
                raise UserValueError(
                    f"ARTHUR_VERIFY_SSL environment variable must be a boolean value, got "
                    f"{os.getenv('ARTHUR_VERIFY_SSL')}"
                )

        # authorization
        # TODO: allow specified login/pass to override an env var api key
        if login is None:
            login = os.getenv("ARTHUR_LOGIN")
        if password is None:
            password = os.getenv("ARTHUR_PASSWORD")
        if api_key is None and login is None:
            api_key = os.getenv("ARTHUR_API_KEY")
        # validate only login or api key
        if login is not None and api_key is not None:
            raise UserValueError(
                "You may not provide both a login and api key, please ensure you are are supplying only "
                "one through the login/api_key parameters and ARTHUR_LOGIN/ARTHUR_API_KEY environment "
                "variables"
            )
        if login is not None:  # login if provided
            # if password not supplied, get it from input
            if password is None:
                password = getpass(f"Please enter password for {login}: ")

            # Get session token from login and password
            auth_token = user_login(
                api_http_host=url, login=login, password=password, verify_ssl=verify_ssl
            )
            # create an auth refresher
            auth_refresher = AuthRefresher(
                url=url, login=login, password=password, verify_ssl=verify_ssl
            )
            header_refresh_func = auth_refresher.refresh
        elif api_key is not None:  # if api key provided, set that
            auth_token = api_key
            header_refresh_func = None
        else:
            raise MissingParameterError(
                "No authentication provided. Please supply a login (username or email) through "
                "the 'login' parameter or ARTHUR_LOGIN environment variable.\n\nIf this is a "
                "production environment, alternatively consider providing an API key through "
                "the 'api_key' parameter or ARTHUR_API_KEY environment variable."
            )

        # org id
        if offline:
            if organization_id is not None:
                raise UserValueError(
                    "You cannot specify an organization ID if you are offline."
                )
            else:
                organization_id = UNKNOWN_ORG_ID
        else:  # if online
            # fill org ID with environment variable if not provided
            if organization_id is None:
                organization_id = os.getenv("ARTHUR_ORGANIZATION_ID")
            # if still no org ID, fetch it from the API
            if organization_id is None:
                organization_id = get_current_org(
                    url, auth_token, verify_ssl=verify_ssl
                )

        # TODO: consider having the SDK override this?
        user_agent = f"arthur-client/{__version__} (system={system()})"
        headers = {
            "Accept": "application/json",
            "Authorization": auth_token,
            "User-Agent": user_agent,
            ORG_ID_HEADER: organization_id,
        }

        # setup http client construction arguments
        client_kwargs = {
            "base_url": url,
            "default_headers": headers,
            "verify_ssl": verify_ssl,
            "allow_insecure": allow_insecure,
            "header_refresh_func": header_refresh_func,
        }

        # create client object for each client subcomponent
        self.admin = ArthurAdminClient(HTTPClient(**client_kwargs))  # type: ignore
        self.alerts = ArthurAlertsClient(HTTPClient(**client_kwargs))  # type: ignore
        self.bench = ArthurBenchClient(HTTPClient(**client_kwargs))  # type: ignore
        self.common = ArthurClientCommon(HTTPClient(**client_kwargs))  # type: ignore
        self.enrichments = ArthurEnrichmentsClient(HTTPClient(**client_kwargs))  # type: ignore
        self.inferences = ArthurInferencesClient(HTTPClient(**client_kwargs))  # type: ignore
        self.insights = ArthurInsightsClient(HTTPClient(**client_kwargs))  # type: ignore
        self.metrics = ArthurMetricsClient(HTTPClient(**client_kwargs))  # type: ignore
        self.model_groups = ArthurModelGroupsClient(HTTPClient(**client_kwargs))  # type: ignore
        self.models = ArthurModelsClient(HTTPClient(**client_kwargs))  # type: ignore
        self.query = ArthurQueryClient(HTTPClient(**client_kwargs))  # type: ignore
        # end client object creation

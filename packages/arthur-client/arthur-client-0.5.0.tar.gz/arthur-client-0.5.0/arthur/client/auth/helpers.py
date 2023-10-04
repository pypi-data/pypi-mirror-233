from typing import Optional

import requests

from arthur.client.http.requests import HTTPClient
from arthur.client.rest.admin.client import ArthurAdminClient
from arthur.client.rest.admin.models import LoginRequest, AuthenticationInfo
from arthur.common.exceptions import (
    UserValueError,
    ForbiddenError,
    UnauthorizedError,
    NotFoundError,
    ArthurUnexpectedError,
)


# TODO: ask BE if this ever returns empty
def get_current_org(
    api_http_host: str, auth_token: str, verify_ssl: bool = True
) -> Optional[str]:
    """Get the current organization for the provided access key

    :param api_http_host: base url of the host to connect to, including protocol (e.g. "https://app.arthur.ai")
    :param auth_token: API Key to pass to the API
    :param verify_ssl: Boolean for whether requests should verify that the SSL certificate is valid and not self-signed
    :return: the organization ID associated with the provided access key, None if no such organization exists
    """
    auth_info = get_auth_info(api_http_host, auth_token, verify_ssl)
    if auth_info is None:
        raise ArthurUnexpectedError("Invalid / non-existent auth_info")
    elif len(auth_info.organization_ids) == 1:
        # If the user is authenticated into a single org, automatically select it as the user's current org
        return auth_info.organization_ids[0]
    elif len(auth_info.organization_ids) > 1:
        # Raise exception and give the user options of available current organizations
        authenticated_org_id_str = "".join(
            f"{org_id}\n" for org_id in auth_info.organization_ids
        )[:-1]
        raise UserValueError(
            f"Your access_key provides access to multiple organizations - please specify one of the following: "
            + authenticated_org_id_str
        )
    else:  # len(auth_info.organization_ids) == 0
        return None


def get_auth_info(
    api_http_host: str, auth_token: str, verify_ssl: bool = True
) -> AuthenticationInfo:
    """Get the AuthInfo struct associated with the provided access key

    :param api_http_host: base url of the host to connect to, including protocol (e.g. "https://app.arthur.ai")
    :param auth_token: Token to fetch authentication info for
    :param verify_ssl: Boolean for whether requests should verify that the SSL certificate is valid and not self-signed
    :return: the AuthInfo associated with the provided access key
    :permissions: N/A
    """
    admin_client = ArthurAdminClient(
        HTTPClient(
            base_url=api_http_host,
            verify_ssl=verify_ssl,
            default_headers={"Authorization": auth_token},
        )
    )
    try:
        auth_info = admin_client.authenticate()
    except requests.exceptions.SSLError as e:
        raise UserValueError(
            f"""SSL Error connecting to {api_http_host}, please connect to a secure server or use 
                             verify_ssl=False to override security checks"""
        ) from e
    except requests.RequestException as e:
        raise UserValueError(
            f"Failed to connect to {api_http_host}, please ensure the URL is correct"
        ) from e
    except NotFoundError as e:
        raise ArthurUnexpectedError(
            "Auth Info endpoint not implemented by api-host"
        ) from e

    return auth_info


def user_login(
    api_http_host: str, login: str, password: str, verify_ssl: bool = True
) -> str:
    """Static convenience function to get a new auth token for the provided username and password

    :param api_http_host: base url of the host to connect to, including protocol (e.g. "https://app.arthur.ai")
    :param login: the username or password to use to log in
    :param password: password for the user
    :param verify_ssl: Boolean for whether requests should verify that the SSL certificate is valid and not self-signed
    :return: an access_key
    """

    admin_client = ArthurAdminClient(
        HTTPClient(base_url=api_http_host, verify_ssl=verify_ssl)
    )
    try:
        _, login_cookies = admin_client.login(
            LoginRequest(login=login, password=password)
        )
    # TODO: move all these checkings into the HTTPClient
    except requests.exceptions.SSLError as e:
        raise UserValueError(
            f"""SSL Error connecting to {api_http_host}, please connect to a secure server or use 
                             verify_ssl=False to override security checks"""
        ) from e
    except requests.RequestException as e:
        raise UserValueError(
            f"Failed to connect to {api_http_host}, please ensure the URL is correct"
        ) from e
    except ForbiddenError as e:
        raise UserValueError(
            f"Unauthorized, please ensure your username and password are correct"
        ) from e

    auth_token = login_cookies.get("Authorization")

    return auth_token

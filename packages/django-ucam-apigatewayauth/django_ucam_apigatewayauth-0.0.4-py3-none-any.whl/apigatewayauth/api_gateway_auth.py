from dataclasses import dataclass
from typing import Optional, Set

from identitylib.identifiers import Identifier
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request


@dataclass(eq=True)
class APIGatewayAuthenticationDetails:
    """
    A dataclass representing the authentication information passed from the API Gateway.

    """

    principal_identifier: Identifier
    scopes: Set[str]
    app_id: Optional[str] = None
    client_id: Optional[str] = None


class APIGatewayAuthentication(authentication.BaseAuthentication):
    """
    An Authentication provider which interprets the headers provided by the API Gateway.

    This library expects to only be used within an application that is deployed behind and can
    only be invoked by the API Gateway, and therefore relies on the fact that the headers
    provided are authoritative.

    """

    def authenticate(self, request: Request):
        if not request.META.get("HTTP_X_API_ORG_NAME", None):
            # bail early if we look like we're not being called by the API Gateway
            return None
        if not request.META.get("HTTP_X_API_OAUTH2_USER", None):
            raise AuthenticationFailed("Could not authenticate using x-api-* headers")

        try:
            principal_identifier = Identifier.from_string(
                request.META["HTTP_X_API_OAUTH2_USER"], find_by_alias=True
            )
        except Exception:
            raise AuthenticationFailed("Invalid principal identifier")

        auth = APIGatewayAuthenticationDetails(
            principal_identifier=principal_identifier,
            scopes=set(filter(bool, request.META.get("HTTP_X_API_OAUTH2_SCOPE", "").split(" "))),
            # the following will only be populated for confidential clients
            app_id=request.META.get("HTTP_X_API_DEVELOPER_APP_ID", None),
            client_id=request.META.get("HTTP_X_API_OAUTH2_CLIENT_ID", None),
        )
        # the first item in the tuple represents the 'user' which we don't have when we've
        # used the API Gateway for authentication.
        return None, auth

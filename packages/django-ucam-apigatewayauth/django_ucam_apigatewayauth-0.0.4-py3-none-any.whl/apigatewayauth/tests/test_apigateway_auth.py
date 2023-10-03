from django.test import TestCase
from identitylib.identifiers import Identifier, IdentifierSchemes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory

from apigatewayauth.api_gateway_auth import (
    APIGatewayAuthentication,
    APIGatewayAuthenticationDetails,
)


class APIGatewayAuthTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.request_factory = APIRequestFactory()
        self.auth = APIGatewayAuthentication()

    def request_with_headers(self, headers={}):
        parsed_headers = {
            f'HTTP_{key.upper().replace("-", "_")}': value for key, value in headers.items()
        }
        return self.request_factory.get("/", **parsed_headers)

    def test_bails_early_without_api_org(self):
        self.assertIsNone(
            self.auth.authenticate(self.request_with_headers({"Accept": "application/json"}))
        )

    def test_throws_without_auth_details(self):
        with self.assertRaisesMessage(
            AuthenticationFailed, "Could not authenticate using x-api-* headers"
        ):
            self.auth.authenticate(self.request_with_headers({"x-api-org-name": "test"}))

    def test_throws_without_principal_identifier(self):
        with self.assertRaisesMessage(
            AuthenticationFailed, "Could not authenticate using x-api-* headers"
        ):
            self.auth.authenticate(
                self.request_with_headers(
                    {"x-api-org-name": "test", "x-api-developer-app-class": "public"}
                )
            )

    def test_throws_with_bad_principal_identifier(self):
        with self.assertRaisesMessage(AuthenticationFailed, "Invalid principal identifier"):
            self.auth.authenticate(
                self.request_with_headers(
                    {
                        "x-api-org-name": "test",
                        "x-api-developer-app-class": "public",
                        "x-api-oauth2-user": "Monty Dawson",
                    }
                )
            )

    def test_can_use_any_identifier_scheme_in_principal_identifier(self):
        for scheme in IdentifierSchemes.get_registered_schemes():
            _, auth = self.auth.authenticate(
                self.request_with_headers(
                    {
                        "x-api-org-name": "test",
                        "x-api-developer-app-class": "public",
                        "x-api-oauth2-user": str(Identifier("1000", scheme)),
                    }
                )
            )
            self.assertEqual(auth.principal_identifier, Identifier("1000", scheme))

    def test_throws_with_unknown_identifier_type(self):
        with self.assertRaisesMessage(AuthenticationFailed, "Invalid principal identifier"):
            self.auth.authenticate(
                self.request_with_headers(
                    {
                        "x-api-org-name": "test",
                        "x-api-developer-app-class": "public",
                        "x-api-oauth2-user": "wgd23@gmail.com",
                    }
                )
            )

    def test_returns_client_details_for_valid_auth(self):
        user, auth = self.auth.authenticate(
            self.request_with_headers(
                {
                    "x-api-org-name": "test",
                    "x-api-developer-app-class": "public",
                    "x-api-oauth2-user": str(Identifier("a123", IdentifierSchemes.CRSID)),
                }
            )
        )
        self.assertIsNone(user)

        self.assertEqual(
            auth,
            APIGatewayAuthenticationDetails(
                Identifier("a123", IdentifierSchemes.CRSID),
                set(),
                None,
                None,
            ),
        )

    def test_will_pass_through_scopes(self):
        _, auth = self.auth.authenticate(
            self.request_with_headers(
                {
                    "x-api-org-name": "test",
                    "x-api-developer-app-class": "public",
                    "x-api-oauth2-user": str(Identifier("a123", IdentifierSchemes.CRSID)),
                    "x-api-oauth2-scope": (
                        "https://api.apps.cam.ac.uk/a.readonly https://api.apps.cam.ac.uk/b"
                    ),
                }
            )
        )

        self.assertEqual(
            auth,
            APIGatewayAuthenticationDetails(
                Identifier("a123", IdentifierSchemes.CRSID),
                set(
                    [
                        "https://api.apps.cam.ac.uk/a.readonly",
                        "https://api.apps.cam.ac.uk/b",
                    ]
                ),
                None,
                None,
            ),
        )

    def test_will_pass_through_app_and_client_ids(self):
        _, auth = self.auth.authenticate(
            self.request_with_headers(
                {
                    "x-api-org-name": "test",
                    "x-api-developer-app-class": "confidential",
                    "x-api-oauth2-user": str(Identifier("a123", IdentifierSchemes.CRSID)),
                    "x-api-oauth2-scope": (
                        "https://api.apps.cam.ac.uk/a.readonly https://api.apps.cam.ac.uk/b"
                    ),
                    "x-api-developer-app-id": "app-uuid-mock",
                    "x-api-oauth2-client-id": "client-id-uuid-mock",
                }
            )
        )

        self.assertEqual(
            auth,
            APIGatewayAuthenticationDetails(
                Identifier("a123", IdentifierSchemes.CRSID),
                set(
                    [
                        "https://api.apps.cam.ac.uk/a.readonly",
                        "https://api.apps.cam.ac.uk/b",
                    ]
                ),
                "app-uuid-mock",
                "client-id-uuid-mock",
            ),
        )

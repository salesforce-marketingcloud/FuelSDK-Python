from unittest import TestCase
from FuelSDK import ET_Client


class TestET_Client(TestCase):
    """ These tests are specific for OAuth2 Public/Web Apps,
    so config should be modified accordingly."""

    def setUp(self):
        self.client = ET_Client(False, False)

    def test_authToken_and_refreshKey_should_differ_if_refresh_token_is_enforced(self):
        self.authToken1 = self.client.authToken
        self.refreshKey1 = self.client.refreshKey

        self.client.refresh_token_with_oAuth2(True)

        self.authToken2 = self.client.authToken
        self.refreshKey2 = self.client.refreshKey

        self.assertNotEqual(self.authToken1, self.authToken2)
        self.assertNotEqual(self.refreshKey1, self.refreshKey2)

    def test_auth_payload_should_have_public_app_attributes(self):
        self.client.application_type = 'public'

        payload = self.client.create_payload()

        self.assertEqual(self.client.client_id, payload['client_id'])
        self.assertEqual(self.client.redirect_URI, payload['redirect_uri'])
        self.assertEqual(self.client.authorization_code, payload['code'])
        self.assertEqual('authorization_code', payload['grant_type'])

    def test_auth_payload_for_public_app_should_not_have_client_secret(self):
        self.client.application_type = 'public'

        payload = self.client.create_payload()

        self.assertRaises(KeyError, lambda: payload['client_secret'])

    def test_auth_payload_should_have_web_app_attributes(self):
        self.client.application_type = 'web'

        payload = self.client.create_payload()

        self.assertEqual('authorization_code', payload['grant_type'])
        self.assertEqual(self.client.client_id, payload['client_id'])
        self.assertEqual(self.client.client_secret, payload['client_secret'])
        self.assertEqual(self.client.redirect_URI, payload['redirect_uri'])
        self.assertEqual(self.client.authorization_code, payload['code'])

    def test_auth_payload_should_have_server_app_attributes(self):
        self.client.application_type = 'server'

        payload = self.client.create_payload()

        self.assertEqual('client_credentials', payload['grant_type'])
        self.assertEqual(self.client.client_id, payload['client_id'])
        self.assertEqual(self.client.client_secret, payload['client_secret'])

    def test_auth_payload_for_server_app_should_not_have_code_and_redirect_uri(self):
        self.client.application_type = 'server'

        payload = self.client.create_payload()

        self.assertRaises(KeyError, lambda: payload['code'])
        self.assertRaises(KeyError, lambda: payload['redirect_uri'])

    def test_auth_payload_with_refresh_token_should_have_refresh_token_attribute(self):
        self.client.refreshKey = 'RefreshKey'

        payload = self.client.create_payload()

        self.assertEqual('refresh_token', payload['grant_type'])
        self.assertEqual(self.client.refreshKey, payload['refresh_token'])

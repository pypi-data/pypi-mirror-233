import os
from unittest import TestCase

from connectify.configuration_services import load_env_variables_from_file
from connectify.facebook_services import FacebookConnection


class TestFacebookConnection(TestCase):
    def setUp(self) -> None:
        load_env_variables_from_file(".env.dev")
        self.connection = FacebookConnection(access_token=os.getenv("FB_ACCESS_TOKEN"))

    def test_get_ad_accounts(self):
        ad_accounts = self.connection.get_ad_accounts()
        assert ad_accounts, "failed to fetch ad accounts"

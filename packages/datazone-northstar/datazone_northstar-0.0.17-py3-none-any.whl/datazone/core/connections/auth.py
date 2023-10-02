import json
import os

import keyring
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from datazone.core.connections.config import ConnectionConfig
from datazone.constants import Constants


class AuthService:
    def __init__(self):
        self.config = ConnectionConfig()
        # TODO consider remove it. It provide use insecure http urls.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    def set_token(self, token):
        raw_token = json.dumps(token)
        keyring.set_password(Constants.DEFAULT_KEYRING_APP_NAME, "token", raw_token)

    def get_token(self):
        token = keyring.get_password(Constants.DEFAULT_KEYRING_APP_NAME, "token")
        if token:
            return json.loads(token)

    def login(self):
        client = LegacyApplicationClient(client_id=Constants.DEFAULT_OAUTH2_CLIENT_ID)
        session = OAuth2Session(client=client)
        token = session.fetch_token(
            token_url=self.config.token_url,
            username=self.config.username,
            password=self.config.password,
        )

        self.set_token(token)
        return token

    def get_session(self):
        token = self.get_token()
        if token is None:
            token = self.login()

        return OAuth2Session(
            client_id=Constants.DEFAULT_OAUTH2_CLIENT_ID,
            token=token,
            auto_refresh_url=self.config.token_url,
            token_updater=self.set_token,
            auto_refresh_kwargs={"client_id": Constants.DEFAULT_OAUTH2_CLIENT_ID},
        )

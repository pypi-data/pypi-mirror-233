"""Base

- TOKEN_URL: URL for authentication based on default or env.
- BASE_URL: URL for API requests.
"""
import os
from abc import ABC, abstractmethod
import json
import logging
from pathlib import Path
from time import time
from typing import TypedDict

from requests_oauthlib import OAuth2Session
from requests import Session, Response
from requests.exceptions import HTTPError
from oauthlib.oauth2 import BackendApplicationClient

logger = logging.getLogger(__name__)

TOKEN_URL = os.getenv(
    'UBICQUIA_AUTH_URL',
    'https://auth.ubihub.ubicquia.com'
    '/auth/realms/ubivu-prd/protocol/openid-connect/token'
)

BASE_URL = os.getenv('UBICQUIA_BASE_URL', 'https://api.ubicquia.com/api')


class TokenCache(ABC):
    """Define implementation for caching the token.

    Define a cache to save and obtains token from external storage systems.
    """
    @abstractmethod
    def save(self, token: dict) -> None:
        """Save token in external storage.

        Args:
            token: data to save

        Returns:
            None

        Raises:
        """

    @abstractmethod
    def retrieve(self) -> dict:
        """Obtains token from storage.

        Write your own method to obtain or retrieve token from external source.
        """


class FileTokenCache(TokenCache):
    """Implementation for single JSON file to store the token in filesystem.

    This will be the default Session Token to be serialized as Token.
    """
    tmp_dir: Path = Path('./.tmp').resolve()
    filename: str = 'token.json'

    def save(self, token: dict) -> None:
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        with open(self.tmp_dir / self.filename, 'w') as j:
            json.dump(token, j)
        logger.debug('Save token in JSON file')

    def retrieve(self) -> dict:
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.tmp_dir / self.filename, 'r') as j:
                _token = json.load(j)
        except FileNotFoundError:
            _token = {}
        return _token


class UbicquiaSession:
    """Generate a requests.Session handling the Oauth2 flow.

    Ubicquia login require: Oauth2 - Client Credentials.

    oauthlib for BackendApplicationClient doesn't use 'refresh_token' in token
    response but Auth server gives that.

    Refresh Token isn't interactive, so always requests an Access Token
    https://stackoverflow.com/a/58698729/4112006

    Attributes:
        token_url: URL used for token and authentication.

    Args:
        client_id: client id from platform
        client_secret: secret from platform
        token_url: authentication url
        token_cache: TokenCache implementation
    """

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 token_url: str = TOKEN_URL,
                 token_cache: TokenCache = FileTokenCache()
                 ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.token_cache = token_cache
        self.__token = {}

    @property
    def token(self) -> dict:
        return self.__token

    @token.setter
    def token(self, value: dict) -> None:
        """Token setter.

        Args:
            value: token data

        Returns:
            None.

        Raises:
            ValueError: if token is not a dict
        """
        if not isinstance(value, dict):
            raise ValueError('Value must be dict')
        self.__token = value

    def is_expired(self, expires_at: float) -> bool:
        """Check if token is expired.

        Args:
            expires_at: token expiration time

        Returns:
            True if expired, False otherwise
        """
        current_time = time()
        safe_expires_at = expires_at - 60
        return current_time > safe_expires_at

    def obtain_token_session(self) -> None:
        """Obtain a Token from:

        1. Obtain a Token from Cache
        2. Check if token is expired
        3. Request new token if necessary
        4. Generate a `requests.Session` for consecutive requests. Additionally,
            some extra http headers included.
        """
        request_new_token = False
        if self.token_cache:
            self.token = self.token_cache.retrieve()
        if not self.token:
            request_new_token = True
        if self.token and self.is_expired(self.token['expires_at']):
            request_new_token = True
        oauth2_client = BackendApplicationClient(client_id=self.client_id)
        oauth2_client.prepare_request_body(scope=['openid'])
        if request_new_token:
            logger.info('Request new token: Oauth fetch_token')
            self.oauth = OAuth2Session(client=oauth2_client)
            self.token = self.oauth.fetch_token(
                token_url=self.token_url,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            if self.token_cache:
                logger.debug('Save the token')
                self.token_cache.save(self.token)
            else:
                logger.debug('Token not cached')
        else:
            self.oauth: Session = OAuth2Session(
                client=oauth2_client,
                token=self.token
            )
        # The Oauth2 session will set the corret headers for http request calls
        self.client: Session = self.oauth
        #
        # Configure headers for requests. Standard:
        # self.client.headers.update({'Accept': 'application/json'})
        # Ubicquia API Docs show:
        self.client.headers.update({'accept': 'application/json'})
        # breakpoint ()
        # print (f'self.client.headers {self.client.headers}')

    def raw_req(self, *args, **kwargs) -> Response:
        """Returns a Respose object from requests.

        Args:
            `*args`, `**kwargs`: parameters passed to requests.request

        Return:
            Response object from requests module.

        Raises:
            HTTP Errors from requests.
        """
        self.obtain_token_session()
        return self.client.request(*args, **kwargs)

    def req(self, *args, **kwargs) -> dict:
        """Make a HTTP request to server.

        Wrapper for requests. Use this method as it were

        .. code:: python

            requests.request(*args, **kwargs)

        Args:
            args, kwargs: same as requests.request(...)

        Returns:
            dict: response data

        Raises:
            HTTPError:
        """
        self.obtain_token_session()
        r = self.client.request(*args, **kwargs)
        # from  pprint import pprint
        # print (self.client.access_token)
        # print( f'request.headers = {r.request.headers}')
        # print( f'request.body = {r.request.body}')
        # pprint( r.json())
        # breakpoint ()
        try:
            data = r.json()
        except json.decoder.JSONDecodeError:
            data = {}
        try:
            r.raise_for_status()
        except HTTPError:
            logger.exception(f'HTTPError handled. Error json={data}')
            raise
        return data

    def __str__(self):
        return f'UbicquiaSession {self.client_id}'


class PaginationDict(TypedDict):
    page: str
    per_page: str


class Endpoint:
    """Define common endpoint class for SDK.

    Attributes:
        base_url: URL obtained from Session
    """

    def __init__(self, session: UbicquiaSession):
        """
        Args:
            session: generated by Oauthlib
        """
        self.base_url = BASE_URL
        self.base_url_v2 = BASE_URL + '/v2'
        self.session = session

    def pagination(self,
                   page: int = 1,
                   per_page: int = 15) -> PaginationDict:
        """Handle pagination.

        Filter by pagination parameters. Example unpack to combine pagination
        ** self.pagination(** pagination)

        Args:
            page: (default to 1) page number
            per_page: (default to 15) number of items per page

        Returns:
            PaginationDict: example {'page': 1, 'per_page': 15}

        Raises:
            TypeError: if invalid arguments provided,
                method got an unexpected keyword argument
        """
        return PaginationDict(page=page, per_page=per_page)

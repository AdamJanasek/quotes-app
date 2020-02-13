import os
from json import JSONDecodeError
import requests
from requests import Response

from app.common.extensions import cache


def parse_data(func):
    """Decorator to unpack http response code and request body
    """
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        try:
            data = response.json()
            return response.status_code, data
        except JSONDecodeError:
            return 500, {'message': 'Response parse error.'}

    return wrapper


class FavQsApi:
    """Class for communication with FavQs API v2.
    Includes methods to downloading quotes, filtering, logging in, voting and managing favorites.
    """

    def __init__(self):
        """Initializes the API url and requests headers.
        """
        self.__api_url: str = os.environ.get("API_URL")  #:
        self.__headers: dict = {
            'Content-Type': 'application/json',
            'Authorization': 'Token token="{}"'.format(os.environ.get("API_KEY"))
        }

        self.__user_headers: dict = {
            'Content-Type': 'application/json',
            'Authorization': 'Token token="{}"'.format(os.environ.get("API_KEY")),
            'User-Token': ''
        }

        self.__login_payload: dict = {
            "user": {
                "login": '',
                "password": ''
            }
        }
        # variable storing login information
        self.__logged: bool = False

    def __post_api(self, url: str, payload: dict) -> Response:
        return requests.post(self.__api_url + url, json=payload, headers=self.__headers)

    def __get_api(self, url: str) -> Response:
        return requests.get(self.__api_url + url, headers=self.__headers)

    def __put_api_logged_user(self, url: str) -> Response:
        return requests.put(self.__api_url + url, headers=self.__user_headers)

    def __get_api_logged_user(self, url: str) -> Response:
        return requests.get(self.__api_url + url, headers=self.__user_headers)

    def login(self, login: str, password: str) -> (int, dict):
        self.__login_payload.get('user')['login'] = login
        self.__login_payload.get('user')['password'] = password
        response: Response = self.__post_api('session', self.__login_payload)

        try:
            data: dict = response.json()
        except JSONDecodeError:
            return 500, {'message': 'Response parse error.'}

        if not data.get('message'):
            self.__user_headers['User-Token'] = data.get('User-Token', '')
            self.__logged = True
            return response.status_code, {}

        return response.status_code, data

    @parse_data
    @cache.cached(300)
    def get_quotes(self) -> (int, dict):
        return self.__get_api('quotes')

    @parse_data
    def get_filtered_quotes(self, keyword) -> (int, dict):
        if keyword:
            return self.__get_api('quotes/?filter={}'.format(keyword))
        return self.__get_api('quotes')

    @parse_data
    def up_vote(self, quote_id: int) -> Response:
        return self.__put_api_logged_user('quotes/' + str(quote_id) + '/upvote')

    @parse_data
    def down_vote(self, quote_id: int) -> Response:
        return self.__put_api_logged_user('quotes/' + str(quote_id) + '/downvote')

    @parse_data
    def add_to_favorites(self, quote_id: int) -> Response:
        return self.__put_api_logged_user('quotes/' + str(quote_id) + '/fav')

    @parse_data
    def remove_from_favorites(self, quote_id: int) -> Response:
        return self.__put_api_logged_user('quotes/' + str(quote_id) + '/unfav')

    @parse_data
    def get_favorites(self) -> (int, dict):
        return self.__get_api_logged_user('activities')

    def logout(self) -> None:
        self.__user_headers['User-Token'] = ''
        self.__logged = False

    @property
    def logged(self) -> bool:
        return self.__logged

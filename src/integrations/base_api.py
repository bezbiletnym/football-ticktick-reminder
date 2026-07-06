from abc import ABC, abstractmethod
import requests


class BaseAPI(ABC):

    _TOKEN: str

    def __init__(self, token: str):
        self._TOKEN = token


    @abstractmethod
    def _get_headers(self) -> dict:
        pass


    def _send_request(self, method: str, url: str, data: dict) -> dict:
        try:
            response = requests.request(method=method, url=url, json=data,
                                        headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Something went wrong: {repr(e)}")
            return {}
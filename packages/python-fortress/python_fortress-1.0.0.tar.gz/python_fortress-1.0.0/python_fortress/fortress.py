import logging
from io import StringIO
from typing import Optional

import requests
from dotenv import load_dotenv

# logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://www.passfortress.com/api/"


class Fortress:
    api_key: str
    access_token: str
    master_key: str
    envfile_name: str

    """
    A class that represents a secret fortress and allows you to interact with the API to retrieve an .env file.
    """

    def __init__(self, base_url: str = BASE_URL, **credentials):
        """
        Initializes a Fortress instance.

        :param base_url: URL base para la API.
        """
        self.base_url: str = base_url
        self.configure(**credentials)

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def configure(self, **credentials):
        self.api_key: str = credentials.get("api_key", None)
        self.access_token: str = credentials.get("access_token", None)
        self.master_key: str = credentials.get("master_key", None)

    def _build_url(self, endpoint: str) -> str:
        """
        Constructs the full URL for a specific endpoint.

        :param endpoint: desired endpoint.
        :return: full url.
        """
        return f"{self.base_url}{endpoint}"

    def get_envfile(self, envfile_id) -> Optional[str]:
        """
        Gets the content of the .env file from the API.

        :return: Content of the .env file or None if there is an error.
        """
        url = self._build_url(endpoint=f"get-secret/{envfile_id}/")
        data = {
            "api_key": self.api_key,
            "master_key": self.master_key,
            "secret_type": "envfile",
        }
        response = requests.post(url=url, data=data, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("secret_data", {}).get("value")

        logger.error(f"Error getting envfile. Code: {response.status_code}. message: {response.text}")
        return None

    def load_env(self, envfile_id):
        envfile = self.get_envfile(envfile_id)
        if envfile:
            load_dotenv(stream=StringIO(envfile))
            return True
        return False

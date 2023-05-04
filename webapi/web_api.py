import urllib.request
import json


class WebAPI:
    """
    General class for interacting with web APIs
    """

    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url

    def _download_url(self, query: str) -> dict:
        """
        Downloads the URL and returns the result as a string
        param:
            query: str - the query to be appended to the base URL
        """
        if self.api_key is None:
            raise Exception("API key not set")
        opener = urllib.request.build_opener()
        opener.addheaders = [('X-APIKEY', self.api_key)]
        urllib.request.install_opener(opener)
        response = urllib.request.urlopen(self.base_url + query)
        json_results = response.read()
        r_obj = json.loads(json_results)
        response.close()
        return r_obj

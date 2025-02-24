import requests

from bs4 import BeautifulSoup

class CinemaScraper:
    result = []

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self._html = None
        

    def make_request(self) -> str:
        return requests.get(self.base_url).text

    def html_parser(self) -> str:
        if self._html is None:
            self._html = BeautifulSoup(self.make_request(),
                                       'html.parser')
            
        return self._html

    def find_elements_by_tag(self, tag: str) -> str:
        if self._html is None:
            self._html = BeautifulSoup(self.make_request(),
                                       'html.parser')
            
        return self._html.find_all(tag)

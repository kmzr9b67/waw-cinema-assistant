import requests

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from cinema_scraper import CinemaScraper
from movie import Movie

class Iluzjon():
    list_shows = []
    number = 0

    def __init__(self):
        self.base_url = 'https://www.iluzjon.fn.org.pl/repertuar.html'
        Iluzjon.number += 1
        self.cinema = 'Iluzjion'
        self.number = Iluzjon.number
        self.request = requests.get(self.base_url).text
        self.html = BeautifulSoup(self.request, 'html.parser')
        

    def __get_result(self, schedule:str, movie_title:str, realise_year:str) -> dict:
        movie = Movie(title=movie_title, time=schedule, cinema='Iluzjon',
                     year=realise_year, base_url=self.base_url)
        movie.set_rating()

        return movie.to_dictionary()
    
    @staticmethod
    def __get_year(info:list) -> str:
        try:
            # It removes the last element from the list, which represents the year, 
            # but the year is not always provided. The list also contains the countries 
            # of production.
            int(info[-1])
            return info[-1].strip()
        except ValueError:
            return '0000'

    def get_shows_list(self, list:list) -> list:
        if Iluzjon.number > self.number:
            return 0 
        with ThreadPoolExecutor(len(list)) as executor:
            for result in executor.map(Iluzjon.__get_year, list):
                Iluzjon.list_shows.append(result)

        return Iluzjon.list_shows

    def get_result_map(self, time:str, title:str, year:str) -> list:
        if Iluzjon.number > self.number:
            return 0 
        with ThreadPoolExecutor(len(time)) as executor:
            for result in executor.map(self.__get_result, time, title, year):
                CinemaScraper.result.append(result)

        return CinemaScraper.result

from concurrent.futures import ThreadPoolExecutor

from CinemaScraper import CinemaScraper
from Movie import Movie

class Iluzjon(CinemaScraper):
    lista_shows = []
    numer = 0

    def __init__(self):
        self.base_url = 'https://www.iluzjon.fn.org.pl/repertuar.html'
        super().__init__(self.base_url)
        Iluzjon.numer += 1
        self.cinema = 'iluzjion'
        self.id = Iluzjon.numer

    def __get_result(self, schedule, movie_title, realise_year):
        movie = Movie(title=movie_title, time=schedule, cinema='Iluzjon',
                     year=realise_year, base_url=self.base_url)
        movie.set_rating()

        return movie.to_dictionary()


    def get_shows_list(self, lista):
        def __get_year(info):
            try:
                int(info[-1])
                return info[-1].strip()
            except ValueError:
                return "0000"

        with ThreadPoolExecutor(len(lista)) as executor:
            for result in executor.map(__get_year, lista):
                Iluzjon.lista_shows.append(result)

        return Iluzjon.lista_shows

    def get_result_map(self, time, title, year):
        with ThreadPoolExecutor(len(time)) as executor:
            for result in executor.map(self.__get_result, time, title, year):
                CinemaScraper.result.append(result)

        return CinemaScraper.result

from concurrent.futures.thread import ThreadPoolExecutor

from movie import Movie
from cinema_scraper import CinemaScraper

class Amondo(CinemaScraper):
    number = 0
    url = []

    def __init__(self):
        self.base_url = 'https://kinoamondo.pl/repertuar'
        super().__init__(self.base_url)
        Amondo.number += 1
        self.cinema = 'Amondo'
        self.number = Amondo.number


    def retrive_movie_info(self, number: int) ->list:
        def __fetch_movie_info(url, time):
            movie = Movie(base_url=url, time=time, cinema='Amondo')
            movie.set_title()
            movie.set_year()
            movie.set_rating()
            return movie.to_dictionary()

        box = self.html_parser().find(id=f'schedule-{number}')
        try:
            urls_list = [i.find('a')['href'] for i in
                        box.find_all('div', class_='col-md-2 col-sm-3')]
        except AttributeError:
            return []

        times_list = [i.text[-5:] for i in box.find_all(class_='time')]
        # Handles multiple clicks when the user presses the button repeatedly

        if Amondo.number > self.number:
            return 0
        
        with ThreadPoolExecutor(len(urls_list)) as executor:
            for mapa in executor.map(__fetch_movie_info,
                                     urls_list, times_list):
                CinemaScraper.result.append(mapa)
        return 0






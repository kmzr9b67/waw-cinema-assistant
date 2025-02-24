import imdb

from cinema_scraper import CinemaScraper

class Movie:
    IA = imdb.IMDb()

    def __init__(
            self, time, base_url, cinema, title=None, year=None,
            rating=None, director = None):
        self.base_url = base_url
        self.time = time
        self.title = title
        self.cinema = cinema
        self.year = year
        self.rating = rating
        self.director = director
        

    def set_title(self) -> str:
        self.title = CinemaScraper(self.base_url).find_elements_by_tag(
            'h1'
        )[0].text
        return self.title

    def set_rating(self) -> None:
        try:
            info = Movie.IA.get_movie(
                Movie.IA.search_movie(f'{self.title} ({self.year})')[0].getID())
            if self.cinema == 'Iluzjon':
                self.director = (info.data['director'][0]['name'])
            self.rating = info.data['rating']
        except (KeyError, IndexError):
            self.rating = ''
    

    def set_year(self) -> None:
        try:
            info = [i.find_all_next('li') for i in
                            CinemaScraper(self.base_url).html_parser().find_all(
                                'ul', class_='movie-info')][0]
            director_str = str(info[0])
            self.director = director_str[21:len(director_str)-5]
            year_str = str(info[1])
            self.year = year_str[len(year_str) - 12:len(year_str) - 8]
        except (IndexError, AttributeError):
            self.year = '0000'

    def to_dictionary(self) -> dict:
        return {
            'rating': self.rating,
            'time': self.time,
            'cinema': self.cinema,
            'title': self.title,
            'link': self.base_url,
            'director': self.director,
            'year': self.year
        }

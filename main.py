from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timedelta

from flask import Flask, render_template, request

from amondo import Amondo
from cinema_scraper import CinemaScraper
from iluzjon import Iluzjon

DAY_AFTER_TOMORROW = (datetime.now().date() + timedelta(2)).strftime('%a, %d.%m')
DAYS = {
    'Today': datetime.now().date(),
    'Tomorrow': datetime.now().date() + timedelta(1),
    (datetime.now().date() + timedelta(2)).strftime('%a,'): 
                                                    datetime.now().date() + timedelta(2)
}


app = Flask(__name__)

def get_amondo_data(number: str) -> None:
    cinema = Amondo()
    cinema.retrive_movie_info(number) 

def get_iluzjon_data(day_number: int) -> None:
    cinema = Iluzjon()
    headings = cinema.html_parser().find_all('h3')
    try:
        counter = [int(i.text[0:2]) for i in headings].index(day_number)
    except ValueError:
        return []

    show_table = cinema.find_elements_by_tag('table')[counter]
    show_table_hour = show_table.find_all(class_='hour')
    time_and_title = [i.text.split(' - ', 1) for i in show_table_hour]
    list_times = [i[0] for i in time_and_title]
    list_titles = [i[1] for i in time_and_title]
    list_years_html = [i.text.split(',') for i in show_table.find_all('i')]
    list_years = cinema.get_shows_list(list_years_html)
    cinema.get_result_map(list_times, list_titles, list_years)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('help.html', day_after_tomorrow = DAY_AFTER_TOMORROW)

@app.route('/result', methods=['GET', 'POST'])
def get_info():
    day_get = request.args.get('day')
    date = DAYS[day_get] 
    CinemaScraper.result = []

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(get_amondo_data, date)
        executor.submit(get_iluzjon_data, int(date.day))

    repertuar = CinemaScraper.result
    repertuar.sort(key = lambda x: str(x['rating']), reverse = True)
    
    if day_get not in ['Today', 'Tomorrow']:
        day_get = DAY_AFTER_TOMORROW
    return render_template('index.html', post=repertuar, 
                        what_day = day_get, what_date = date)

if __name__ == '__main__':
    app.run()

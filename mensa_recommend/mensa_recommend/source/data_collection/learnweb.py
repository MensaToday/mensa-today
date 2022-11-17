"""
  Collect course data
"""
from __future__ import absolute_import, unicode_literals
from typing import List, Tuple
from urllib.parse import urlparse, parse_qs
import re
from .utils import Collector, NoAuthCollector, url_to_soup
from bs4 import BeautifulSoup
import requests
from courses.models import Room, Course, Timeslot
from users.models import User
from celery import shared_task


@shared_task
def run(ziv_id: str, ziv_password: str, current_user: int):
    lw_collector = LearnWebCollector(ziv_id, ziv_password, current_user)
    lw_collector.run()


class LearnWebCollector(Collector):

    def __init__(self, ziv_id: str, ziv_password: str, current_user: int):
        self.ziv_id = ziv_id
        self.ziv_password = ziv_password
        self.current_user = current_user

        self.base_url = 'https://sso.uni-muenster.de/LearnWeb/learnweb2'
        self.search_url_pattern = 'https://sso.uni-muenster.de/LearnWeb/learnweb2/course/search.php?search={search_string}'

    def run(self) -> None:
        session_id = self.__get_session_id()

        headers = {'Cookie': session_id}

        courses = self.__get_current_courses(headers)

        # TODO parallel
        for course in courses:
            self.__save_course_details(course, headers)

    def __get_session_id(self) -> str:

        payload = {'httpd_username': self.ziv_id,
                   'httpd_password': self.ziv_password}

        try:
            session = requests.Session()
            session_response = session.post(self.base_url, data=payload)

            if session_response.status_code == 401:
                raise SystemError("401 unauthorized")

        except requests.exceptions.RequestException as error:
            raise SystemError(error) from error

        session_header = session_response.headers

        return session_header['set-Cookie']

    def __get_current_courses(self, headers: dict) -> List[str]:

        soup = url_to_soup(self.base_url, headers)

        current_semester = soup.find('ul', attrs={'class': 'sub-sub-menu'})

        if current_semester is None:
            raise SystemError("could not find element")

        courses = []
        course_list_elements = current_semester.find_all(
            'li', attrs={'class': 'sub-sub-menu-item'})

        if course_list_elements is not None:
            for i in current_semester.find_all('li', attrs={'class': 'sub-sub-menu-item'}):
                courses.append(i.find('span').getText())
        else:
            raise SystemError("could not find element")

        return courses

    def __save_course_details(self, course: str, headers: dict):
        search_url = self.search_url_pattern.format(
            search_string=requests.utils.quote(course))

        course_name, qis_url = self.__get_quis_url_name(search_url, headers)

        if qis_url is not None:
            qis_url = qis_url['href']+'&language=en'

            parsed_qis_url = urlparse(qis_url)
            course_id = parse_qs(parsed_qis_url.query)['publishid'][0]

            table_data = self.__get_qis_table_data(qis_url)

            course = Course(course_id, course_name, course)
            course.save()
            course.users.add(self.current_user)

    def __get_quis_url_name(self, search_url: str, headers: dict) -> Tuple[str, str]:
        soup = url_to_soup(search_url, headers)

        number_search_results_string = soup.find('h2').getText()

        if number_search_results_string is not None:
            number_search_results = int(
                re.sub(r'[^0-9,.]', ' ', number_search_results_string))
        else:
            raise SystemError("could not find element")

        if number_search_results > 1:
            raise Warning("Learnweb Search results in more than 1 courses")
        elif number_search_results == 0:
            raise SystemError("Learnweb Search results in 0 courses")

        course_name = soup.find('a', attrs={'class': 'aalink'}).text

        qis_url = soup.find('div', attrs={'class': 'content'}).find(
            'div', attrs={'class': 'summary'}).find('a')

        return course_name, qis_url

    def __get_qis_table_data(self, qis_url: str) -> List:
        soup = url_to_soup(qis_url)

        # Quispos table crawling
        table_data = []
        table = soup.find(
            'table', attrs={'summary': 'Übersicht über alle Veranstaltungstermine'})
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            filtered_cols = []
            for ele in cols:
                room = ele.find('a', attrs={'class': 'regular'})

                if room is not None:
                    room_link = room['href']

                    parsed_room_link = urlparse(room_link)
                    link_params = parse_qs(parsed_room_link.query)

                    if 'raum.rgid' in link_params:
                        room_id = link_params['raum.rgid'][0]
                        filtered_cols.append(room_id)
                    else:
                        filtered_cols.append(ele.text.strip())
                else:
                    filtered_cols.append(ele.text.strip())

            table_data.append(filtered_cols)

        formatted_qis_table_data = self.__format_qis_table_data(table_data)

        return formatted_qis_table_data

    def __format_qis_table_data(self, table_data: List) -> List[dict]:

        formatted_qis_table_data = []
        for entry in table_data[1:]:
            weekday = entry[1]

            start_end_time = entry[2].replace(u'\xa0', u' ')
            start_time, end_time = start_end_time.split(' to ')

            rythm = entry[3]

            start_end_date = entry[4].replace(u'\xa0', u' ')
            start_date, end_date = start_end_date.split(' to ')

            room_id = entry[5]

            qis_table_data_dict = {'weekday': weekday, 'start_time': start_time,
                                   'end_time': end_time, 'rythm': rythm, 'start_date': start_date,
                                   'end_date': end_date, 'room_id': room_id}

            formatted_qis_table_data.append(qis_table_data_dict)

        return formatted_qis_table_data


class RoomCollector(NoAuthCollector):

    def __init__(self):
        self.room_url_pattern = 'https://studium.uni-muenster.de/qisserver/rds?state=wsearchv&search=3&alias_einrichtung.eid=einrichtung.dtxt&alias_k_raumart.raumartid=k_raumart.dtxt&raum.rgid={room_id}&P_start=0&P_anzahl=10&_form=display&language=en'

    def build_urls(self) -> List[str]:
        return ['https://studium.uni-muenster.de/qisserver/rds?state=change&type=6&moduleParameter=raumSelect&nextdir=change&next=SearchSelect.vm&target=raumSearch&subdir=raum&source=state%3Dchange%26type%3D5%26moduleParameter%3DraumSearch%26nextdir%3Dchange%26next%3Dsearch.vm%26subdir%3Draum%26_form%3Ddisplay%26topitem%3Dfacilities%26subitem%3DsearchFacilities%26function%3Dnologgedin%26field%3Ddtxt&targetfield=dtxt&_form=display&noDBAction=y&init=y']

    def scrape(self, document: BeautifulSoup) -> None:
        room_ids = self.__get_room_ids(document)

        for room_id in room_ids:
            room_name, room_address, room_seats = self.__get_room_info(room_id)

            if room_name is not None:
                Room(room_id, room_name, room_address, room_seats).save()

    def __get_room_ids(self, document: BeautifulSoup) -> List[int]:

        fieldset = document.find_all('fieldset')[1]
        room_ids = []
        for room in fieldset.find_all('a', href=True):
            room_link = room['href']

            parsed_room_link = urlparse(room_link)
            link_params = parse_qs(parsed_room_link.query)
            if 'raum.rgid' in link_params:
                room_id = link_params['raum.rgid'][0]
                room_ids.append(room_id)

        return room_ids

    def __get_room_info(self, room_id: int) -> Tuple[str, str, int]:

        url_pattern_formatted = self.room_url_pattern.format(room_id=room_id)

        document = url_to_soup(url_pattern_formatted)

        info_row = document.find('div', attrs={'class': 'InfoLeiste'}).text
        hits = int(re.findall(r'(.*)(?=hits)', info_row)[0])

        room_name: str = None
        room_address: str = None
        room_seats: int = None

        if hits != 0:
            rows = document.find_all('div', attrs={'class': 'erg_list_entry'})

            for row in rows:
                row_label = row.find(
                    'div', attrs={'class': 'erg_list_label'}).text
                if 'Room:' in row_label:
                    room_name = row.find(
                        'strong').text.strip().replace(',', '')
                elif 'Building Address:' in row_label:
                    room_address = row.find(
                        'div', attrs={'class': 'erg_list_label'}).next_sibling.strip().replace(',', '')
                elif 'Equipment:' in row_label:
                    room_seats = re.findall(
                        r'(?<=Plätze:)(.\s*[0-9]*)(?=[a-zA-Z]*)', row.text)

                    if len(room_seats) != 0:
                        room_seats = room_seats[0].strip()

                        if room_seats != '':
                            room_seats = int(room_seats)
                        else:
                            room_seats = None
                    else:
                        room_seats = None

        return room_name, room_address, room_seats

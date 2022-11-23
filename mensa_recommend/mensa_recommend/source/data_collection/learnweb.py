"""
    Define classes to crawl course data (including Date/Time and location) 
    from the learnweb and quispos system of the university Münster
"""
from __future__ import absolute_import, unicode_literals

import datetime
import re
from typing import List, Tuple, Union
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup
from celery import shared_task

from courses.models import Room, Course, Timeslot, Reservation
from .utils import Collector, NoAuthURLCollector, url_to_soup


@shared_task
def run(ziv_id: str, ziv_password: str, current_user: int):
    lw_collector = LearnWebCollector(ziv_id, ziv_password, current_user)
    result = lw_collector.run()

    return result


class LearnWebCollector(Collector):
    """
        Methods to authenticate to the learnweb and to get all user courses. 
        After getting the courses detailed course data will be requested from
        the quispos system. All crawled data will be stored in the database
    """

    def __init__(self, ziv_id: str, ziv_password: str, current_user: int):
        self.ziv_id = ziv_id
        self.ziv_password = ziv_password
        self.current_user = current_user

        # set base urls
        self.base_url = 'https://sso.uni-muenster.de/LearnWeb/learnweb2'
        self.search_url_pattern = 'https://sso.uni-muenster.de/LearnWeb/learnweb2/course/search.php?search={search_string}'

    def run(self) -> None:
        """
            main method which can be run to execute whole data collection process
        """

        # authenticate the user
        session_id = self.get_session_id()

        headers = {'Cookie': session_id}

        # get current courses from the learnweb. Headers with the session_id are required
        courses = self.__get_current_courses(headers)

        # TODO parallel
        # Get and save course details for each course
        for course in courses:
            self.__save_course_details(course, headers)

    def get_session_id(self) -> Union[str, False]:
        """Authenticate the user to the sso of the learnweb. If the credentials
        are incorrect a False will be returned to indicate the wrong credentials
        to the user. This method can also be execuded first to initial check the
        correctness.

        Return
        ------
        session_id : str
            The session id can be used for further authentication
        """

        # Create payload with the required naming
        payload = {'httpd_username': self.ziv_id,
                   'httpd_password': self.ziv_password}

        try:
            # Send payload to authentication server via a post request
            session = requests.Session()
            session_response = session.post(self.base_url, data=payload)

            # Check if credentials are correct. If not a 401 (unauthorized) will be
            # the status code and a False will be returned
            if session_response.status_code == 401:
                return False

        except requests.exceptions.RequestException as error:
            raise SystemError(error) from error

        # Get the headers and return the 'set-Cookie' header
        session_header = session_response.headers

        return session_header['set-Cookie']

    def __get_current_courses(self, headers: dict) -> List[str]:
        """Private method to get all courses of the current semester out of the learnweb

            Parameters
            ----------
            headers : dict
                Authentication header of the form {'Cookie': session_id}

            Return
            ------
            courses : List[str]
                A list of all courses consisting of course abbreviations
        """

        # Get soup object from the base learnweb url
        soup = url_to_soup(self.base_url, headers)

        # Navigate to the current semester menu
        current_semester = soup.find('ul', attrs={'class': 'sub-sub-menu'})

        # Check if object can be found
        if current_semester is None:
            raise SystemError("could not find element")

        courses = []

        # Get all course list elements
        course_list_elements = current_semester.find_all(
            'li', attrs={'class': 'sub-sub-menu-item'})

        # Check if list elements can be found
        if course_list_elements is not None:

            # Iterate over each element of the list and get the list text (course abbreviation)
            for i in current_semester.find_all('li', attrs={'class': 'sub-sub-menu-item'}):

                # append the abbreviation the courses list
                courses.append(i.find('span').getText())
        else:
            raise SystemError("could not find element")

        return courses

    def __save_course_details(self, course: str, headers: dict):
        """Private method to get and save the course details. Here the quispos sever will be accessed

            Parameters
            ----------
            course: str
                Course abbreviation
            headers : dict
                Authentication header of the form {'Cookie': session_id}

        """

        # format the learnweb search url with the course name
        search_url = self.search_url_pattern.format(
            search_string=requests.utils.quote(course))

        # Get the quipos url of the course by searching for the course in the learnweb
        course_name, qis_url = self.__get_quis_url_name(search_url, headers)

        # Check if the quis_url is None. There are some courses that do not have a quipos entry.
        # This courses will be ignored
        if qis_url is not None:

            # Change language of the quispos site to get only english namings
            qis_url = qis_url['href']+'&language=en'

            # Get the publish id (unique id of the course) from the qis url
            parsed_qis_url = urlparse(qis_url)
            course_id = parse_qs(parsed_qis_url.query)['publishid'][0]

            # Get detailed course data from the quispos table of the course site
            table_data = self.__get_qis_table_data(qis_url)

            # Save the data into the database
            course = Course(course_id, course_name, course)
            course.save()
            course.users.add(self.current_user)

            for data in table_data:
                room = Room.objects.get(pk=data['room_id'])

                # Check if room exists otherwise do not save the timeslot
                if room is not None:

                    # Get or create timeslot
                    try:
                        timeslot = Timeslot.objects.get(weekDay=data['weekday'], startTime=data['start_time'],
                                                        endTime=data['end_time'], startDate=data['start_date'],
                                                        endDate=data['end_date'],  rythm=data['rythm'])
                    except Timeslot.DoesNotExist:
                        timeslot = Timeslot(weekDay=data['weekday'], startTime=data['start_time'],
                                            endTime=data['end_time'], startDate=data['start_date'],
                                            endDate=data['end_date'],  rythm=data['rythm'])

                        timeslot.save()

                    Reservation(course=course, timeslot=timeslot,
                                room=room).save()

    def __get_quis_url_name(self, search_url: str, headers: dict) -> Union[Tuple[str, str], Tuple[None, None]]:
        """Private method to get the quispos url from the learnweb search result

            Parameters
            ----------
            search_url : str
                The learnweb search url including the current searched course name
            headers : dict
                Authentication header of the form {'Cookie': session_id}

            Return
            ------
            course_name : str
                The detailed course name
            qis_url : str
                The quispos url for further crawling

        """

        # Get soup object from the learnweb search url
        soup = url_to_soup(search_url, headers)

        # Get the number of search results
        number_search_results_string = soup.find('h2').getText()

        # check if the number of search results of the form (Suchergebnisse: x) is not None.
        # Otherwise there will be a search error
        if number_search_results_string is not None:
            # Get the number of (Suchergebnisse: x)
            number_search_results = int(
                re.sub(r'[^0-9,.]', ' ', number_search_results_string))
        else:
            raise SystemError("could not find element")

        # Check if number is 0 or greater than 1. if it is greater than 1 raise a warning
        # if it is 0 than return None for course_name and qis_url.
        if number_search_results > 1:
            raise Warning("Learnweb Search results in more than 1 courses")
        elif number_search_results == 0:
            return None, None

        course_name = soup.find('a', attrs={'class': 'aalink'}).text

        # get the qis a tag but do not get the href out of. It will be checked
        # at a later point.
        qis_url = soup.find('div', attrs={'class': 'content'}).find(
            'div', attrs={'class': 'summary'}).find('a')

        return course_name, qis_url

    def __get_qis_table_data(self, qis_url: str) -> List[dict]:
        """private method to get the quipos table of the course detail page

            Parameters
            ----------
            qis_url : str
                The quipos url
            Return
            ------
            formatted_qis_table_data : List[dict]
                A list of dicts with detailed course data for each time_slot of the following form:
                [{'weekday': weekday, 'start_time': start_time,
                'end_time': end_time, 'rythm': rythm, 'start_date': start_date,
                'end_date': end_date, 'room_id': room_id}]

        """

        # Get soup object from the qis_url
        soup = url_to_soup(qis_url)

        # Quispos table crawling
        table_data = []

        # Find the correct table with timeslot details
        table = soup.find(
            'table', attrs={'summary': 'Übersicht über alle Veranstaltungstermine'})

        # Get all rows of the table
        rows = table.find_all('tr')

        # Iterate over each row
        for row in rows:

            # Get the colums
            cols = row.find_all('td')

            # Iterate over each column
            filtered_cols = []
            for ele in cols:

                # Try to get the room because the room link is required
                room = ele.find('a', attrs={'class': 'regular'})

                # check if column has a link
                if room is not None:

                    # If yes, then get the link
                    room_link = room['href']

                    # Parse the link parameters
                    parsed_room_link = urlparse(room_link)
                    link_params = parse_qs(parsed_room_link.query)

                    # Check if 'raum.rgid' is in the parameters
                    if 'raum.rgid' in link_params:

                        # If yes, then append to room id to the filter_cols list
                        room_id = link_params['raum.rgid'][0]
                        filtered_cols.append(room_id)
                    else:

                        # Else, just append the text
                        filtered_cols.append(ele.text.strip())
                else:

                    # Else, just append the text
                    filtered_cols.append(ele.text.strip())

            # Append the whole row to the table_data list
            table_data.append(filtered_cols)

        # Format the table_data list to make it clearly structured
        formatted_qis_table_data = self.__format_qis_table_data(table_data)

        return formatted_qis_table_data

    def __format_qis_table_data(self, table_data: List[List]) -> List[dict]:
        """private method to format the qis table data

            Parameters
            ----------
            table_data : List[List]
                List of Lists of the course details

            Return
            ------
            formatted_qis_table_data : List[dict]
                A list of dicts with detailed course data for each time_slot of the following form:
                [{'weekday': weekday, 'start_time': start_time,
                'end_time': end_time, 'rythm': rythm, 'start_date': start_date,
                'end_date': end_date, 'room_id': room_id}]

        """

        formatted_qis_table_data = []

        # Iterate over each row. The first row will be excluded because it is always empty
        for entry in table_data[1:]:

            # Extract specific information
            weekday = entry[1]

            start_end_time = entry[2].replace(u'\xa0', u' ')
            start_time, end_time = start_end_time.split(' to ')

            rythm = entry[3]

            start_end_date = entry[4].replace(u'\xa0', u' ')
            start_date, end_date = start_end_date.split(' to ')

            # Reformat time
            start_date = datetime.datetime.strptime(
                start_date, '%d.%m.%Y').strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(
                end_date, '%d.%m.%Y').strftime('%Y-%m-%d')

            room_id = entry[5]

            # Create a dict with all information combined
            qis_table_data_dict = {'weekday': weekday, 'start_time': start_time,
                                   'end_time': end_time, 'rythm': rythm, 'start_date': start_date,
                                   'end_date': end_date, 'room_id': room_id}

            formatted_qis_table_data.append(qis_table_data_dict)

        return formatted_qis_table_data


class RoomCollector(NoAuthURLCollector):
    """
        Methods to get the all Rooms of the university including address and number of seats
    """

    def __init__(self):
        self.room_url_pattern = 'https://studium.uni-muenster.de/qisserver/rds?state=wsearchv&search=3&alias_einrichtung.eid=einrichtung.dtxt&alias_k_raumart.raumartid=k_raumart.dtxt&raum.rgid={room_id}&P_start=0&P_anzahl=10&_form=display&language=en'

    def _build_urls(self) -> List[str]:
        return ['https://studium.uni-muenster.de/qisserver/rds?state=change&type=6&moduleParameter=raumSelect&nextdir=change&next=SearchSelect.vm&target=raumSearch&subdir=raum&source=state%3Dchange%26type%3D5%26moduleParameter%3DraumSearch%26nextdir%3Dchange%26next%3Dsearch.vm%26subdir%3Draum%26_form%3Ddisplay%26topitem%3Dfacilities%26subitem%3DsearchFacilities%26function%3Dnologgedin%26field%3Ddtxt&targetfield=dtxt&_form=display&noDBAction=y&init=y']

    def scrape(self, document: BeautifulSoup) -> None:
        """method to format the qis table data

            Parameters
            ----------
            document : BeautifulSoup
                BeautifulSoup object that can be used for crawling

        """

        # Get the ids of the room
        room_ids = self.__get_room_ids(document)

        # Iterate over each room to get more details
        for room_id in room_ids:

            # Get more room details
            room_name, room_address, room_seats = self.__get_room_info(room_id)

            # If the room is not None, save it to the database
            if room_name is not None:
                Room(room_id, room_name, room_address, room_seats).save()

    def __get_room_ids(self, document: BeautifulSoup) -> List[int]:
        """private method to get all the room ids

            Parameters
            ----------
            document : BeautifulSoup
                BeautifulSoup object that can be used for crawling

            Return
            ------
            room_ids : List[int]
                List of integers of all room ids

        """

        fieldset = document.find_all('fieldset')[1]

        room_ids = []

        # get all the links of the room listing
        for room in fieldset.find_all('a', href=True):
            room_link = room['href']

            # Get the url parameters
            parsed_room_link = urlparse(room_link)
            link_params = parse_qs(parsed_room_link.query)

            # if the room is in the parameters get and append it to the rooms_ids list
            if 'raum.rgid' in link_params:
                room_id = link_params['raum.rgid'][0]
                room_ids.append(room_id)

        return room_ids

    def __get_room_info(self, room_id: int) -> Tuple[str, str, Union[int, None]]:
        """private method to get all the room ids

            Parameters
            ----------
            room_id : int
                Id of the current observerd room

            Return
            ------
            room_name : str
                Name of the room
            room_address : str
                Address of the room
            room_seats : str
                Number of seats in the room

        """

        # Format the room search url with the room_id
        url_pattern_formatted = self.room_url_pattern.format(room_id=room_id)

        # Get soup object from the room search url
        document = url_to_soup(url_pattern_formatted)

        # Check how many search results are available
        info_row = document.find('div', attrs={'class': 'InfoLeiste'}).text
        hits = int(re.findall(r'(.*)(?=hits)', info_row)[0])

        room_name: str = None
        room_address: str = None
        room_seats: int = None

        # If number of hits is not 0 than information of the room can be extracted
        if hits != 0:
            rows = document.find_all('div', attrs={'class': 'erg_list_entry'})

            # Iterate over each row of the room information table
            for row in rows:

                # Get the row label
                row_label = row.find(
                    'div', attrs={'class': 'erg_list_label'}).text

                # Check if the label of the current row is one of the relevant infos
                # (room_name, room_address, room_seats)
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

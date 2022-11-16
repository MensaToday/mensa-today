from utils import Collector, url_to_soup
import requests

class LearnWebCollector(Collector):
    
    def __init__(self, ziv_id:str, ziv_password:str):
        self.ziv_id = ziv_id
        self.ziv_password = ziv_password
        self.base_url = 'https://sso.uni-muenster.de/LearnWeb/learnweb2'
            
    def run(self) -> None:
        session_id = self.__get_session_id()
        
        self.headers = {'Cookie': session_id}
        
        self.__get_current_courses()
    
    def __get_session_id(self):
        
        payload = {'httpd_username': self.ziv_id, 'httpd_password': self.ziv_password}
        
        try:
            session = requests.Session()
            session_response = session.post(self.base_url, data=payload)
            
            if session_response.status_code == 401:
                SystemExit("401 unauthorized")
            
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        
        session_header = session_response.headers
        
        return session_header['set-Cookie']
    
    def __get_current_courses(self):
        
        soup = url_to_soup(self.base_url, self.headers)
        
        current_semester = soup.find('ul', attrs={'class':'sub-sub-menu'})
    
        for i in current_semester.find_all('li', attrs={'class':'sub-sub-menu-item' }):
            print(i.find('span').getText())
import unittest
import requests

from bs4 import BeautifulSoup
from config import cookies, headers



class TestParserWork(unittest.TestCase):
    def setUp(self) -> None:
        self.url_by = 'https://rabota.by/vacancies/programmist?page=0&customDomain=1'
        self.url_ru = 'https://hh.ru/vacancies/programmist'
        self.url_kz = 'https://hh.kz/vacancies/programmist'
        
        self.response_by = requests.get(self.url_by, cookies=cookies, headers=headers)
        self.response_ru = requests.get(self.url_ru, cookies=cookies, headers=headers)
        self.response_kz = requests.get(self.url_kz, cookies=cookies, headers=headers)


    def test_status_code_url_by(self):
        self.assertEqual(self.response_by.status_code, 200)
    
    def test_status_code_url_ru(self):
        self.assertEqual(self.response_ru.status_code, 200)

    def test_status_code_url_kz(self):
        self.assertEqual(self.response_kz.status_code, 200)
        






if __name__ == '__main__':
    unittest.main()
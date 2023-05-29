import requests
import re
import logging

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

class Parser:
    '''A website parser which looking for programmer vacancies on rabota.by'''

    __page_vacancy_urls = []

    def __init__(self, url, cookies=None, headers=None, params={'page': '0',
                                                                'customDomain': '1',}) -> None:
        self.url_website = url
        self.cookies = cookies
        self.headers = headers
        self.params = params
#------------------------------------
    def get_page_html_text(self, url, params=None):
        try:
            self.response = requests.get(url=url, cookies=self.cookies, headers=self.headers, params=params)   
            logging.info(f"Response status code: [{self.response.status_code}], URL: {url}")
            self.soup = BeautifulSoup(self.response.text, 'lxml')
        except Exception as ex:
            logging.error(f"Error fetching URL: {url}\n{ex}")

    def find_total_sum_vacancies(self):
        self.get_page_html_text(self.url_website, self.params)
        total_string = self.soup.find('span', {'data-qa':"vacancies-total-found", 'class':"bloko-header-section-3"}).find('span')
        list_figures = re.findall(r'[\d]', str(total_string))
        self.total_sum = int(''.join(list_figures))
   
    def count_pages(self):
        return self.total_sum // 50 + 1
#---------------------------------------------------------------
    def find_all_page_urls_vacancies(self):    
        for url in self.page_vacancies:
            info = url.find('div', class_="vacancy-serp-item-body__main-info")
            link_container = info.find('a', class_='serp-item__title').get('href')
            self.__page_vacancy_urls.append(link_container)    

    def find_all_page_vacancies(self):
        self.page_vacancies = []
        self.page_vacancies = self.soup.find_all('div', {'data-qa':"vacancy-serp__vacancy vacancy-serp__vacancy_premium", 'class':"serp-item"})
        self.page_vacancies += self.soup.find_all('div', {'data-qa':"vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus", 'class':"serp-item"})
        self.page_vacancies += self.soup.find_all('div', {'data-qa':"vacancy-serp__vacancy vacancy-serp__vacancy_standard", 'class':"serp-item"})
        self.page_vacancies += self.soup.find_all('div', {'data-qa':"vacancy-serp__vacancy vacancy-serp__vacancy_free", 'class':"serp-item"})
    
    def find_all_pages_urls(self):
        for page in range(self.count_pages()):
           self.params['page'] = str(page)
           logging.info(f"Page: {page+1}")
           self.get_page_html_text(self.url_website, self.params)
           self.find_all_page_vacancies()
           self.find_all_page_urls_vacancies()

    def find_data_vacancy(self):
        for index, url in enumerate(self.__page_vacancy_urls, start=1):
            try:
                logging.info(f"Vacancy: {index}")
                self.get_page_html_text(url)    
                job_name = self.soup.find('h1', {'data-qa':"vacancy-title", 'class':'bloko-header-section-1'})
                salary = self.soup.find('div', {'data-qa':"vacancy-salary"})
                work_exp = self.soup.find('span', {'data-qa':"vacancy-experience"})
                company = self.soup.find('span', {'data-qa':"bloko-header-2", 'class':'bloko-header-section-2 bloko-header-section-2_lite'})
                company_url = self.soup.find('a', {'data-qa':"vacancy-company-name"})
                description = self.soup.find('div', {'data-qa':"vacancy-description"})
                address = self.soup.find('span', {'data-qa':"vacancy-view-raw-address"})
                data_list = [job_name, salary, work_exp, company, description, address, company_url]
                names_list = ['name_vacancy', 'salary', 'work_exp', 'company', 'description', 'address', 'company_url']
                data_vacancy = {key: value.text.replace('\xa0', '').replace('\u202f', '') if value else 'Developer' for key, value in zip(names_list, data_list)}
                if company_url:
                    data_vacancy['company_url'] = 'https://rabota.by' + company_url.get('href')
                data_vacancy['url'] = url
                yield data_vacancy
                
            except Exception as ex:
                logging.error(f"Error getting data vacancy: {index}, {url}\n{ex}")
                continue


















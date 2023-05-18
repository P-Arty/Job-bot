import psycopg2

from datetime import date
from string import punctuation
from config import host, database, user, password

class PostgresDataVacancy:
    '''A class creates database and inserts data vacancies from class Parser into PostgreSQL'''
    def __init__(self) -> None:
        self.connection = psycopg2.connect(host=host,
                                           database=database,
                                           user=user,
                                           password=password)
        self.connection.autocommit = True         

    def __execute_cursor(self, request):
        self.curs = self.connection.cursor()
        self.curs.execute(request)

    def delete_tables_if_exist(self):
        self.__execute_cursor('''DROP TABLE IF EXISTS vacancies CASCADE;''')
        print('Deleted')

    def create_tables_if_not_exist(self):
        self.__execute_cursor('''CREATE TABLE IF NOT EXISTS vacancies(
                       vacancy_id serial PRIMARY KEY,
                       title VARCHAR(250),
                       experience VARCHAR(30),
                       company VARCHAR(250),
                       salary VARCHAR(50),
                       description TEXT,
                       addres VARCHAR(500),
                       url_vacancy VARCHAR(500),
                       parse_date DATE
                       );''')
        print('DataBase Created')
    
    def insert_data_into_db(self, info):
        self.__execute_cursor(f'''BEGIN;
                  INSERT INTO vacancies (title, experience, company, salary, description, addres, url_vacancy, parse_date)
                    VALUES ('{info['name_vacancy'].replace("'", "")}', '{info['work_exp'].replace("'", "")}', '{info['company'].replace("'", "")}', '{info['salary'].replace("'", "")}', 
                    '{info['description'].replace("'", "")}','{info['address'].replace("'", "")}', '{info['url']}', '{str(date.today())}');
                  COMMIT;''')
        print(f'{info["name_vacancy"]} -- Inserted')
    
    def select_data_from_db(self, search_data='python'):
        self.__execute_cursor(f'''SELECT title, company, url_vacancy, parse_date
                          FROM vacancies
                          WHERE description  ILIKE '{search_data}'
                        ''')
        return self.curs.fetchall()

    def select_count_vacancies(self):
        self.__execute_cursor('''SELECT COUNT(*)
              FROM vacancies''')
        return self.curs.fetchone()
       
    def get_today_date(self):
        self.__execute_cursor(f'''SELECT parse_date
                          FROM vacancies
                          LIMIT 1;
                        ''')
        return self.curs.fetchone()

    def close_connection(self):
        if self.connection:
            self.connection.close()


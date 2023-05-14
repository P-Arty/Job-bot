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
        with self.connection.cursor() as cursor:
            cursor.execute(request)
            
    def delete_tables_if_exist(self):
        self.__execute_cursor('''DROP TABLE IF EXISTS vacancies CASCADE;''')

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
    
    def insert_data_into_db(self, info):
        self.__execute_cursor(f'''BEGIN;
                  INSERT INTO vacancies (title, experience, company, salary, description, addres, url_vacancy, parse_date)
                    VALUES ('{info['name_vacancy'].replace("'", "")}', '{info['work_exp'].replace("'", "")}', '{info['company'].replace("'", "")}', '{info['salary'].replace("'", "")}', 
                    '{info['description'].replace("'", "")}','{info['address'].replace("'", "")}', '{info['url']}', '{str(date.today())}');
                  COMMIT;''')
        print(f'{info["name_vacancy"]} -- Inserted')
    
    def select_data_from_db(self, search_data='python'):
        with self.connection.cursor() as cursor:
            cursor.execute(f'''SELECT title, company, url_vacancy, parse_date
                          FROM vacancies
                          WHERE description  ~* '{search_data.strip(punctuation)}'
                        ''')
            return cursor.fetchall()

    def select_count_vacancies(self):
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT COUNT(*)
              FROM vacancies''')
            for cur in cursor.fetchall():
                print(*cur, sep='\n', end='\n--------------------------------------\n')

    def close_connection(self):
        if self.connection:
            self.connection.close()



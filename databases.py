import psycopg2
import logging

from datetime import date
from config import host, database, user, password

logging.basicConfig(level=logging.INFO)


class PostgresDataVacancy:
    '''A class creates database and inserts data vacancies from class Parser into PostgreSQL'''
    def __init__(self, table_name='vacancies') -> None:
        self.connection = psycopg2.connect(host=host,
                                           database=database,
                                           user=user,
                                           password=password)
        self.table_name = table_name
        self.connection.autocommit = True 
        logging.info(f"Database connection established")        

    def __execute_cursor(self, request):
        try:
            self.curs = self.connection.cursor()
            self.curs.execute(request)
        except Exception as ex:
            logging.error(f"Error executing operation: {request}\n{ex}")

    def delete_tables_if_exist(self):
        self.__execute_cursor(f'''DROP TABLE IF EXISTS {self.table_name} CASCADE;''')
        logging.info(f'Deleted Table: {self.table_name}')

    def create_tables_if_not_exist(self):
        self.__execute_cursor(f'''CREATE TABLE IF NOT EXISTS {self.table_name}(
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
        logging.info(f'Created Table: {self.table_name}')
    
    def insert_data_into_db(self, info):
        self.__execute_cursor(f'''BEGIN;
                  INSERT INTO {self.table_name} (title, experience, company, salary, description, addres, url_vacancy, parse_date)
                    VALUES ('{info['name_vacancy'].replace("'", "")}', '{info['work_exp'].replace("'", "")}', '{info['company'].replace("'", "")}', '{info['salary'].replace("'", "")}', 
                    '{info['description'].replace("'", "")}','{info['address'].replace("'", "")}', '{info['url']}', '{str(date.today())}');
                  COMMIT;''')
        logging.info(f"Inserted vacancy: {info['name_vacancy']} into Table: {self.table_name}")
    
    def select_data_from_db(self, search_data='python'):
        self.__execute_cursor(f'''SELECT title, company, url_vacancy, parse_date
                          FROM {self.table_name}
                          WHERE description  ILIKE '{search_data}'
                        ''')
        logging.info(f"Selected [{search_data}] from Table description: {self.table_name}")
        return self.curs.fetchall()

    def select_count_vacancies(self):
        self.__execute_cursor('''SELECT COUNT(*)
              FROM vacancies''')
        logging.info(f"Selected total count vacancies from Table: {self.table_name}")
        return self.curs.fetchone()
       
    def get_today_date(self):
        self.__execute_cursor(f'''SELECT parse_date
                          FROM vacancies
                          LIMIT 1;
                        ''')
        logging.info(f"Selected total count vacancies from Table: {self.table_name}")
        return self.curs.fetchone()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            logging.info(f"DB connection closed")


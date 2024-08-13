import psycopg2
from colorama import init, Fore, Style
from psycopg2 import sql
from typing import Any

from src.table_output import table_output


class DBManager:
    """ Обеспечивает взаимодействие с базой данных PostgreSQL"""

    def __init__(self, params: dict, db_name=None):
        self.params = params
        self.db_name = db_name
        self.conn = psycopg2.connect(dbname=self.db_name, **self.params)
        self.cur = self.conn.cursor()

    def database_exists(self, db_name: str) -> bool:
        """
        Проверка существования базы данных с заданным именем.
        :return: True если база данных существует и False если нет.
        """
        self.conn.autocommit = True  # Включаем автокоммит

        self.cur.execute(sql.SQL('SELECT 1 FROM pg_database WHERE datname = %s'), [db_name])
        return self.cur.fetchone() is not None

    def create_database(self, db_name: str) -> None:
        """
        Создание базы данных с заданным именем.
        """
        try:
            self.conn.autocommit = True  # Включаем автокоммит
            # Создаем базу данных
            self.cur.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(db_name)))
            print(f'База данных {db_name} успешно создана.')
        except Exception as e:
            print(f'Ошибка при создании базы данных: {e}')
        finally:
            # Закрываем соединение
            if self.conn:
                self.cur.close()
                self.conn.close()
                print('Соединение с PostgreSQL закрыто.')

    def create_tables(self, db_name: str, employers: list[dict[str, Any]], vacancies: list[dict[str, Any]]) -> None:
        """
        Создание таблиц companies и vacancies.
        """
        try:
            self.conn = psycopg2.connect(dbname=db_name, **self.params)
            self.cur = self.conn.cursor()
            self.conn.autocommit = True  # Включаем автокоммит

            # SQL-запрос для удаления таблиц
            self.cur.execute(f'DROP TABLE IF EXISTS vacancies')
            self.cur.execute(f'DROP TABLE IF EXISTS companies CASCADE')

            # SQL-запрос для создания таблицы companies
            self.cur.execute(f'''
                        CREATE TABLE companies 
                        (
                            company_id INTEGER PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            url TEXT
                        )
                    ''')

            # SQL-запрос для заполнения таблицы companies
            for employer in employers:
                self.cur.execute(
                    '''
                    INSERT INTO companies (company_id, name, url)
                    VALUES (%s, %s, %s)
                    ''',
                    (employer['id'], employer['name'], employer['url'])
                )
            print(f'Таблица companies успешно создана.')

            # SQL-запрос для создания таблицы vacancies
            self.cur.execute(f'''
                        CREATE TABLE vacancies 
                        (
                            vacancy_id INTEGER PRIMARY KEY,
                            company_id INTEGER,
                            name VARCHAR(255) NOT NULL,
                            salary_from INTEGER,
                            salary_to INTEGER,
                            currency VARCHAR(5),
                            url TEXT,
                            CONSTRAINT vacancy_companies_fk FOREIGN KEY (company_id)  REFERENCES companies (company_id)
                        )
                    ''')

            # SQL-запрос для заполнения таблицы vacancies
            for vacancy in vacancies:
                self.cur.execute(
                    '''
                    INSERT INTO vacancies (vacancy_id, company_id, name, salary_from, salary_to, currency, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''',
                    (vacancy['id'], vacancy['employer']['id'], vacancy['name'], vacancy['salary']['from'],
                     vacancy['salary']['to'], vacancy['salary']['currency'], vacancy['alternate_url'])
                )
            print(f'Таблица vacancies успешно создана.')

        except Exception as e:
            print(f'Ошибка при создании таблицы: {e}')

        finally:
            # Закрываем соединение
            if self.conn:
                self.cur.close()
                self.conn.close()
                print('Соединение с PostgreSQL после создания таблицы закрыто.')

    def get_companies_and_vacancies_count(self, db_name: str) -> None:
        """ Получает список всех компаний и количество вакансий у каждой компании"""
        try:
            self.conn = psycopg2.connect(dbname=db_name, **self.params)
            self.cur = self.conn.cursor()
            self.conn.autocommit = True  # Включаем автокоммит

            self.cur.execute(f'SELECT companies.name, COUNT(vacancies.vacancy_id) AS vacancies_count, companies.url '
                             f'FROM companies '
                             f'LEFT JOIN vacancies ON companies.company_id = vacancies.company_id '
                             f'GROUP BY companies.company_id, companies.name ORDER BY vacancies_count DESC;')
            rows = self.cur.fetchall()

            columns = ["Компания", "Количество вакансий", "Ссылка"]
            table_output(rows, columns)

        except Exception as e:
            print(f'Ошибка при создании таблицы: {e}')

        finally:
            # Закрываем соединение
            if self.conn:
                self.cur.close()
                self.conn.close()
                print('Соединение с PostgreSQL после создания таблицы закрыто.')

    def get_vacancies(self, db_name: str):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        (с сортировкой зарплаты по убыванию)
        """
        try:
            self.conn = psycopg2.connect(dbname=db_name, **self.params)
            self.cur = self.conn.cursor()
            self.conn.autocommit = True  # Включаем автокоммит

            self.cur.execute('''
            SELECT vacancies.vacancy_id, companies.name AS company_name, vacancies.name AS vacancy_name, 
            COALESCE (vacancies.salary_from, vacancies.salary_to) AS salary_from, vacancies.currency, vacancies.url 
            FROM vacancies JOIN companies ON vacancies.company_id = companies.company_id ORDER BY salary_from DESC;
            ''')
            rows = self.cur.fetchall()

            columns = ["id вакансии", "Компания", "Вакансия", "Зарплата", "Валюта", "Ссылка"]
            table_output(rows, columns)

        except Exception as e:
            print(f'Ошибка при создании таблицы: {e}')

        finally:
            # Закрываем соединение
            if self.conn:
                self.cur.close()
                self.conn.close()
                print('Соединение с PostgreSQL после создания таблицы закрыто.')

    def get_avg_salary(self, db_name: str) -> None:
        """ Получает среднюю зарплату по вакансиям"""
        try:
            self.conn = psycopg2.connect(dbname=db_name, **self.params)
            self.cur = self.conn.cursor()
            self.conn.autocommit = True  # Включаем автокоммит

            self.cur.execute(f'SELECT companies.name, COUNT(vacancies.vacancy_id) AS vacancies_count, '
                             f'AVG(COALESCE(vacancies.salary_from, vacancies.salary_to)) AS average_salary '
                             f'FROM companies LEFT JOIN vacancies ON companies.company_id = vacancies.company_id '
                             f'GROUP BY companies.company_id, companies.name ORDER BY average_salary DESC;')
            rows = self.cur.fetchall()

            columns = ["Компания", "Количество вакансий", "Средняя зарплата по вакансиям"]
            table_output(rows, columns)

        except Exception as e:
            print(f'Ошибка при создании таблицы: {e}')

        finally:
            # Закрываем соединение
            if self.conn:
                self.cur.close()
                self.conn.close()
                print('Соединение с PostgreSQL после создания таблицы закрыто.')

    def get_vacancies_with_higher_salary(self, db_name: str) -> None:
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        try:
            self.conn = psycopg2.connect(dbname=db_name, **self.params)
            self.cur = self.conn.cursor()
            self.conn.autocommit = True  # Включаем автокоммит

            self.cur.execute('''
            SELECT companies.name AS company_name, vacancies.name, 
            COALESCE(vacancies.salary_from, vacancies.salary_to) AS salary, 
            (SELECT AVG(COALESCE(salary_from, salary_to)) FROM vacancies) AS average_salary, 
            vacancies.currency, vacancies.url 
            FROM vacancies JOIN companies ON vacancies.company_id = companies.company_id 
            WHERE COALESCE(vacancies.salary_from, vacancies.salary_to) > (SELECT AVG(COALESCE(salary_from, salary_to)) 
            FROM vacancies) ORDER BY salary DESC;''')
            rows = self.cur.fetchall()

            columns = ["Компания", "Вакансия", "Зарплата", "Средняя зарплата", "Валюта", "Ссылка"]
            table_output(rows, columns)

        except Exception as e:
            print(f'Ошибка при создании таблицы: {e}')

        finally:
            # Закрываем соединение
            if self.conn:
                self.cur.close()
                self.conn.close()
                print('Соединение с PostgreSQL после создания таблицы закрыто.')

    def get_vacancies_with_keyword(self, db_name: str, keyword: str) -> None:
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        try:
            self.conn = psycopg2.connect(dbname=db_name, **self.params)
            self.cur = self.conn.cursor()
            self.conn.autocommit = True  # Включаем автокоммит

            self.cur.execute(f"SELECT  vacancies.name AS vacancy_name, companies.name AS company_name, "
                             f"COALESCE (vacancies.salary_from, vacancies.salary_to) AS salary_from, "
                             f"vacancies.currency, vacancies.url "
                             f"FROM vacancies JOIN companies ON vacancies.company_id = companies.company_id "
                             f"WHERE vacancies.name ILIKE '%{keyword}%' ORDER BY salary_from DESC;")
            rows = self.cur.fetchall()

            if not rows:
                init()
                mistake = f'\nСлово {keyword} в названиях вакансий не найдено\n'
                print(mistake.replace(keyword, f"{Fore.YELLOW}{keyword}{Style.RESET_ALL}"))
            else:
                columns = ["Вакансия", "Компания", "Зарплата", "Валюта", "Ссылка"]
                table_output(rows, columns)

        except Exception as e:
            print(f'Ошибка при создании таблицы: {e}')

        finally:
            # Закрываем соединение
            if self.conn:
                self.cur.close()
                self.conn.close()
                print('Соединение с PostgreSQL после создания таблицы закрыто.')

import psycopg2
from config import config
from typing import Optional, Dict, List


params = config()


class DBManager:

    def __init__(self, db_params):

        self.conn = psycopg2.connect(dbname='manager', **db_params)

    def get_companies_and_vacancies_count(self) -> List[tuple]:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT employers.name,
                COUNT(vacancies.vacancy_id) as vacancies_count
                FROM employers
                LEFT JOIN vacancies ON employers.employer_id =
                vacancies.employer_id
                GROUP BY employers.name
                """
            )
            result = cursor.fetchall()
            return result

    def get_all_vacancies(self) -> List[tuple]:
        """Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT name, title, salary, vacancies.url
                FROM employers
                LEFT JOIN vacancies ON employers.employer_id =
                vacancies.employer_id
                """
            )
            result = cursor.fetchall()
            return result

    def get_avg_salary(self) -> Optional[round]:
        """Получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT AVG(salary) FROM vacancies
                """
            )
            result = cursor.fetchall()
            return result

    def get_vacancies_with_higher_salary(self) -> List[tuple]:
        """Получает список всех вакансий, у которых зарплата выше средней
         по всем вакансиям"""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT title, salary
                FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies)
                """
            )
            result = cursor.fetchall()
            return result

    def get_vacancies_with_keyword(self, keyword: str) -> List[tuple]:
        """Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например python"""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT title
                FROM vacancies 
                WHERE title LIKE %s
                """,
                (f'%{keyword}%',)
            )
            result = cursor.fetchall()
            return result

    def close_connection(self) -> None:
        """Закрывает таблицу"""
        self.conn.close()

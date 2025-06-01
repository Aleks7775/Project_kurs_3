import psycopg2
from connect_api import HH
from config import config


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о вакансиях и работодателях"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                   employer_id VARCHAR(20) PRIMARY KEY,
                   name VARCHAR (255) NOT NULL,
                   url VARCHAR(255)
                   )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                    vacancy_id VARCHAR(20) PRIMARY KEY,
                    employer_id VARCHAR(20) REFERENCES employers(employer_id),
                    title VARCHAR(255) NOT NULL,
                    salary INTEGER,
                    url VARCHAR NOT NULL
                    )
        """)

    conn.commit()
    conn.close()


def save_data_to_db(company_data, vacancy_data, database_name, params):

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for company in company_data:
            emp_id = company['employer']['id']
            name = company['employer']['name']
            url = company['employer']['alternate_url']
            cur.execute(
                """
                INSERT INTO employers (employer_id, name, url)
                VALUES (%s, %s, %s)
                RETURNING employer_id
                """,
                (emp_id, name, url)
            )

        for vacancy in vacancy_data:
            vacancy_id = vacancy['id']
            employer_id = vacancy['employer']['id']
            title = vacancy['name']
            salary_get = vacancy.get('salary')
            salary = salary_get.get('from') if salary_get else None
            url = vacancy['alternate_url']
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, employer_id, title, salary, url)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (vacancy_id, employer_id, title, salary, url)
            )

    conn.commit()
    conn.close()

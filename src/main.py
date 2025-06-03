from psycopg2 import connect
from config import config
from utils import create_database, save_data_to_db
from connect_api import HH
from db_manager import DBManager

company = {4233, 1373, 39305, 7944, 1740, 15478, 3529, 78638, 2180, 1057}  # 10 выбранных мной компаний

params = config()
hh = HH()

"""Собирает данные о 10_ти выбранных работодателях и их вакансиях
(ограничил до 10 вакансий каждой компании) с HH.ру и сохраняем в базу данных"""
company_data = hh.get_vacancies(company, 1)
vacancy_data = hh.get_vacancies(company)

create_database('manager', params)   #Создание базы данных с названием "manager"

save_data_to_db(company_data, vacancy_data, 'manager', params)  #Сохранение данных о работодателе в базу данных


def main() -> None:
    """Меню действий с пользователем"""
    db_manager = DBManager(params)

    while True:
        print(
         """
------------------------------
      Меню действий
------------------------------
1. Список компаний и вакансий
2. Список всех вакансий
3. Средняя зарплата
4. Вакансии с зарплатой выше средней
5. Поиск по ключевому слову
0. Выход
         """)

        value = input()
        if value == "1":
            companies_vacancies = db_manager.get_companies_and_vacancies_count()
            for key, value in companies_vacancies:
                print(f"Компания: {key}, Количество вакансий: {value}")
        elif value == "2":
            all_vacancies = db_manager.get_all_vacancies()
            for i in all_vacancies:
                print(f"Компания: {i[0]}, Вакансия: {i[1]}, Зарплата: {i[2]}, Сcылка: {i[3]}")
        elif value == "3":
            avg_vacancies = db_manager.get_avg_salary()
            print(f'Средняя зарплата по вакансиям: {round(avg_vacancies[0][0])}')
        elif value == "4":
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            for key, value in vacancies_with_higher_salary:
                print(f"Вакансия: {key}, Зарплата: {value}")
        elif value == "5":
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(input("Введите ключевое слово для поиска:"))
            for i in vacancies_with_keyword:
                print(f"Вакансия: {i[0]}")
        elif value == "0":
            db_manager.close_connection()
            break
        else:
            print("Неверны ввод. Попробуйте снова.")


main()

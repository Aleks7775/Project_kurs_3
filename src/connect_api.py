import requests


class HH:
    def __init__(self):
        self.base_url = 'https://api.hh.ru/'
        self.headers = {'User-Agent': 'HH-User-Agent'}

    def connect_to_appi(self, employer_id):
        """Получение данных о работодателя по его id"""
        try:
            url = f'{self.base_url}employers/{employer_id}'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка подключения: {e}")

    def get_vacancies(self, employer_ids, per_page=10):
        """Получение всех вакансий для множества employer_ids"""
        all_vacancies = []  # Список для хранения всех вакансий

        for employer_id in employer_ids:
            try:
                vacancies = []
                params = {'employer_id': employer_id, 'per_page': per_page}
                response = requests.get(f'{self.base_url}vacancies', headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                vacancies.extend(data['items'])
                all_vacancies.extend(vacancies)
            except requests.exceptions.RequestException as e:
                print(f"Ошибка получения вакансий для {employer_id}: {e}")

        return all_vacancies

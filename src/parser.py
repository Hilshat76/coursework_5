from typing import Any

import requests
from abc import ABC, abstractmethod
from tqdm import tqdm


class Parser(ABC):
    @abstractmethod
    def load_vacancies(self, **kwargs):
        pass

    @abstractmethod
    def load_employers(self, **kwargs):
        pass


class HH(Parser):
    """ Класс для работы с API HeadHunter"""

    def __init__(self, employer_ids: list):
        self.employer_ids = employer_ids
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'page': 0, 'per_page': 100, "employer_id": employer_ids, 'only_with_salary': True}
        self.vacancies = []
        self.employers = []

    def load_employers(self, **kwargs) -> list[dict[str, Any]]:
        for employer in tqdm(self.employer_ids, ncols=100, desc='Загрузка работодателей', leave=False):
            url = f"https://api.hh.ru/employers/{employer}"
            get_response = requests.get(url, headers=self.__headers)
            data = get_response.json()
            employer = {'id': data['id'], 'name': data['name'], 'url': data['alternate_url']}
            self.employers.append(employer)
        return self.employers

    def load_vacancies(self, **kwargs) -> list[dict[str, Any]]:
        url = f'https://api.hh.ru/vacancies'

        for self.params['page'] in tqdm(range(0, 5), ncols=100, desc='Загрузка вакансий', leave=False):
            response = requests.get(url, headers=self.__headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
        return self.vacancies

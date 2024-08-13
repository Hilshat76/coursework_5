from config import config
from src.file_work import WorkWithJson
from src.parser import HH
from src.db_manager import DBManager
from src.utils import user_request


def main():
    # Список id выбранных 10 компаний
    employer_ids = [80, 1740, 4181, 4219, 1373, 39305, 3388, 15478, 4233, 3809]

    # Получаем вакансии данных компаний и их вакансий на hh.ru
    hh = HH(employer_ids)
    hh.load_employers()
    hh.load_vacancies()

    # Добавляет компании и вакансии в JSON файлы.
    fv = WorkWithJson()
    fv.save_file(hh.employers, 'employers.json')
    fv.save_file(hh.vacancies, 'vacancies.json')

    # Работа с БВ PostgreSQL.
    params = config()
    db_name = 'hh_vacancies'
    db = DBManager(params)

    if not db.database_exists(db_name):  # Проверяем существование БД
        db.create_database(db_name)  # Создаем БД в случае его отсутствия

    db.create_tables(db_name, hh.employers, hh.vacancies)  # Создание и заполнение таблиц

    # Интерфейс пользователя
    while True:
        user_input = input('\nХотите сделать запрос (да/нет) или (y/n)? : ').lower()
        if user_input in ('нет', 'n'):
            break
        elif user_input in ('да', 'y'):
            user_request(db_name, params)
        else:
            print('Ошибка: Некорректный ответ')


if __name__ == '__main__':
    main()

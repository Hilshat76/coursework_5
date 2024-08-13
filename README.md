# coursework_5

**_Задание_**

**Проект по БД**
В рамках проекта вам необходимо получить данные о компаниях и вакансиях с сайта hh.ru, спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.

**Основные шаги проекта**
* Получить данные о работодателях и их вакансиях с сайта hh.ru. Для этого используйте публичный API hh.ru и библиотеку requests.
* Выбрать не менее 10 интересных вам компаний, от которых вы будете получать данные о вакансиях по API.
* Спроектировать таблицы в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях. Для работы с БД используйте библиотеку psycopg2.
* Реализовать код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.
* Создать класс DBManager для работы с данными в БД.

**Класс DBManager**
Создайте класс DBManager, который будет подключаться к БД PostgreSQL и иметь следующие методы:
* get_companies_and_vacancies_count() — получает список всех компаний и количество вакансий у каждой компании.
* get_all_vacancies() — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
* get_avg_salary() — получает среднюю зарплату по вакансиям.
* get_vacancies_with_higher_salary() — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
* get_vacancies_with_keyword() — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
Класс DBManager должен использовать библиотеку psycopg2 для работы с БД.

**_Для подключения к БД PostgreSQL необходимо создать конфигурационный файл database.ini_**
[postgresql]
host=localhost
user=postgres
password=user_password
port=5432
**_Этот файл надо добавить в .gitignore._**

**Критерии оценки**
Наставник примет вашу работу, если в ней соблюдаются следующие условия. Проверьте работу по критериям перед тем, как отправить ее.

**1. Общие критерии для проекта**
1. [ ] Функциональный код разбит на модули: модуль для взаимодействия с API, модуль для взаимодействия с файлами, модуль для взаимодействия с вакансиями.
2. [ ] Решение выложено на GitHub.
3. [ ] В проекте есть .gitignore.
4. [ ] В коммиты не добавлены игнорируемые файлы.
5. [ ] В проекте есть файл с зависимостями.
6. [ ] Нет грубых нарушений PEP 8 в оформлении кода.
7. [ ] В проекте есть «точка входа» — модуль, запустив который можно получить результат всех реализованных в проекте функциональностей.
8. [ ] Классы соответствуют минимум первым двум принципам SOLID.
9. [ ] Все классы задокументированы.
10. [ ] Все методы классов задокументированы.
11. [ ] Все методы классов типизированы.

**2. Работа по созданию базы данных и таблиц**
1. [ ] Реализован код автоматического создания БД.
2. [ ] Код для создания БД вызывается в основном скрипте программы.
3. [ ] Реализован код для создания таблиц в БД.
4. [ ] Код для создания таблиц в БД вызывается в основном скрипте программы.
5. [ ] Создается таблица для организаций.
6. [ ] Создается таблица для вакансий.
7. [ ] Таблица вакансий связана с таблицей организаций через FK.
8. [ ] Использованы средства скрытия данных для доступа к БД.

**3. Заполнение данных**
1. [ ] Таблица организаций заполняется 10 записями о компаниях для сбора вакансий.
2. [ ] Таблица вакансий заполняется записями о вакансиях компаний через запросы к hh.ru.

**4. Взаимодействие с базой данных**
1. [ ] Реализован класс DBManager.
2. [ ] Реализован метод получения списка всех компаний и количества вакансий у каждой компании.
3. [ ] В методе используется SQL-запрос, выводящий информацию о вакансиях и компаниях через JOIN.
4. [ ] Реализован метод получения списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
5. [ ] В методе используется SQL-запрос, выводящий информацию о вакансиях и компаниях через JOIN.
6. [ ] Реализован метод получения средней зарплаты по вакансиям.
7. [ ] В методе используется SQL-запрос, выводящий информацию о средней зарплате через функцию AVG.
8. [ ] Реализован метод получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям.
9. [ ] В методе используется SQL-запрос, выводящий информацию о средней зарплате через фильтрацию WHERE.
10. [ ] Реализован метод получения списка всех вакансий, в названии которых содержатся переданные в метод слова, например python.
11. [ ] В методе используется SQL-запрос, выводящий список всех вакансий, в названии которых содержатся переданные в метод слова через оператор LIKE.

**5. Интерфейс управления**
1. [ ] Создана функция взаимодействия с пользователем.
2. [ ] Функция использует экземпляры классов и их методы, реализованные ранее.
3. [ ] Не дублируется функциональность, реализованная в классах.
4. [ ] Интерфейс взаимодействия с пользователем реализован понятным текстом, т. е. в выводе не используются коллекции, только человекочитаемые строки.
5. [ ] Функция взаимодействия с пользователем не перегружена.

**6. Тестирование**
1. [ ] Написаны тесты для функциональностей проекта.
2. [ ] Общее покрытие функционального кода — более 70%.
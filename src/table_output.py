from prettytable import PrettyTable


def table_output(rows: list, columns: list) -> None:
    """
    Функция для вывода запросов в табличном виде
    """
    table = PrettyTable()
    table.field_names = columns
    if 'Вакансия' or 'Ссылка' in columns:
        table.align['Вакансия'] = "l"
        table.align['Ссылка'] = "l"

    for row in rows:
        table.add_row(row)
    print(table)

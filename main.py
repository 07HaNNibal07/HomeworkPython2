import csv
import re
from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Создаем словарь для хранения уникальных записей
unique_contacts = {}

for contact in contacts_list:
    # Извлекаем ФИО из первых трех элементов
    name_parts = contact[:3]
    full_name = " ".join(name_parts).split(" ")

    # Приводим к нужному формату
    lastname = full_name[0] if len(full_name) > 0 else ''
    firstname = full_name[1] if len(full_name) > 1 else ''
    surname = full_name[2] if len(full_name) > 2 else ''

    # Приведение телефона к нужному формату
    phone = contact[5]
    phone_pattern = re.compile(r'(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(?:\s*доб\.(\d+))?')
    match = phone_pattern.match(phone)

    if match:
        formatted_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
        if match.group(6):  # Если есть добавочный номер
            formatted_phone += f" доб.{match.group(6)}"
    else:
        formatted_phone = phone  # Если формат не совпадает, оставляем как есть

    # Объединяем данные в одну запись
    key = (lastname, firstname)  # Используем ФИ для ключа
    if key not in unique_contacts:
        unique_contacts[key] = [lastname, firstname, surname, contact[3], contact[4], formatted_phone, contact[6]]
    else:
        # Если запись уже существует, объединяем информацию
        existing_contact = unique_contacts[key]
        existing_contact[3] = existing_contact[3] or contact[3]  # organization
        existing_contact[4] = existing_contact[4] or contact[4]  # position
        existing_contact[5] = formatted_phone  # обновляем телефон

# Преобразуем словарь обратно в список
contacts_list = list(unique_contacts.values())

# TODO 2: сохраните получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

# Для проверки результата
pprint(contacts_list)

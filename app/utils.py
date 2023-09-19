from PIL import Image
import base64
from loguru import logger
from app.settings import CAPTCHA_RESIZED_IMAGE_FILE_PATH, CAPTCHA_TARGET_NAME_QUESTION_ID_MAPPING, MESSAGE_TEMPLATE, PHONE_NUMBER, MESSAGE_HISTORY_URL, FIRST_NAME, LAST_NAME, COMPANY_NAME, TITLE, EMAIL_ADDRESS, STREET_ADDRESS, CITY, STATE, ZIP_CODE, COUNTRY
import csv
import os
from datetime import datetime

PROGRESS_FILE = "csv/progress.txt"


def get_last_processed():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as file:
            return int(file.read().strip())
    return 0


def save_last_processed(row_num):
    with open(PROGRESS_FILE, "w") as file:
        file.write(str(row_num))


def resize_base64_image(filename, size):
    width, height = size
    img = Image.open(filename)
    new_img = img.resize((width, height))
    new_img.save(CAPTCHA_RESIZED_IMAGE_FILE_PATH)
    with open(CAPTCHA_RESIZED_IMAGE_FILE_PATH, "rb") as f:
        data = f.read()
        encoded_string = base64.b64encode(data)
        return encoded_string.decode('utf-8')


def get_question_id_by_target_name(target_name):
    logger.debug(f'try to get question id by {target_name}')
    question_id = CAPTCHA_TARGET_NAME_QUESTION_ID_MAPPING.get(target_name)
    logger.debug(f'question_id {question_id}')
    return question_id


def convert_string_into_int(value):
    if len(value) == 0:
        return -1
    try:
        return int(value)
    except ValueError:
        return -1


def read_contacts_data(file_path):
    contact_list = []
    last_processed = get_last_processed()
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for index, row in enumerate(csv_reader, start=1):
            # Resume from where we left off
            if index <= last_processed:
                continue
            contact_list.append({
                'message': replace_values_into_templage(row),
                'phone_number': '1' + row.get(PHONE_NUMBER, "").strip(),
                'first_name': row.get(FIRST_NAME, "").strip() if len(FIRST_NAME) else "unknown",
                'last_name': row.get(LAST_NAME, "").strip() if len(LAST_NAME) else "unknown",
                'company': row.get(COMPANY_NAME, "").strip() if len(COMPANY_NAME) else "unknown",
                'title': row.get(TITLE, "").strip() if len(TITLE) else "unknown",
                'email': row.get(EMAIL_ADDRESS, "").strip() if len(FIRST_NAME) else "unknown",
                'street': row.get(STREET_ADDRESS, "").strip() if len(STREET_ADDRESS) else "unknown",
                'city': row.get(CITY, "").strip() if len(CITY) else "unknown",
                'state': row.get(STATE, "").strip() if len(STATE) else "unknown",
                'zip_code': row.get(ZIP_CODE, "").strip() if len(ZIP_CODE) else "unknown",
                'country': row.get(COUNTRY, "").strip() if len(COUNTRY) else "unknown",
            })

            # Save the progress
            save_last_processed(index)

        # If processing finishes, we can delete the progress file
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)

    return contact_list


def replace_values_into_templage(row):
    message = MESSAGE_TEMPLATE
    columns = [PHONE_NUMBER, MESSAGE_HISTORY_URL, FIRST_NAME, LAST_NAME, COMPANY_NAME,
               TITLE, EMAIL_ADDRESS, STREET_ADDRESS, CITY, STATE, ZIP_CODE, COUNTRY]
    for value in columns:
        if len(value): message = message.replace(value, row.get(value, "").strip())
    return message


def write_message_history(phone_number, message):
    current_date = datetime.now().strftime("%Y-%m-%d")
    with open(f'{MESSAGE_HISTORY_URL}{current_date}.txt', 'a') as file:
        current_time = datetime.now().strftime("%H:%M:%S")
        file.write(f'{current_time} phone number: {phone_number}\n')
        file.write(f'\t message: {message}\n')


def contact_create_history(item):
    current_date = datetime.now().strftime("%Y-%m-%d")
    with open(f'{MESSAGE_HISTORY_URL}{current_date}.txt', 'a') as file:
        current_time = datetime.now().strftime("%H:%M:%S")
        file.write(f'{current_time} contact created\n')
        file.write(f'\t  Phone number: {item["phone_number"]} First name: {item["first_name"]} Last name: {item["last_name"]} Company: {item["company"]} Title: {item["title"]} Email Address: {item["email"]} Street Address: {item["street"]} City: {item["city"]} State: {item["state"]} Zip code: {item["zip_code"]} Country: {item["country"]} \n')


def contact_create_failed_history(item):
    current_date = datetime.now().strftime("%Y-%m-%d")
    with open(f'{MESSAGE_HISTORY_URL}{current_date}_failed.txt', 'a') as file:
        current_time = datetime.now().strftime("%H:%M:%S")
        file.write(f'{current_time} contact creation failed\n')
        file.write(f'\t  Phone number: {item["phone_number"]} First name: {item["first_name"]} Last name: {item["last_name"]} Company: {item["company"]} Title: {item["title"]} Email Address: {item["email"]} Street Address: {item["street"]} City: {item["city"]} State: {item["state"]} Zip code: {item["zip_code"]} Country: {item["country"]} \n')

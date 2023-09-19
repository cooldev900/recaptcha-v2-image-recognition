from PIL import Image
import base64
from loguru import logger
from app.settings import CAPTCHA_RESIZED_IMAGE_FILE_PATH, CAPTCHA_TARGET_NAME_QUESTION_ID_MAPPING, MESSAGE_TEMPLATE, REPLACE_POSITIONS, PHONE_NUMBER_POSITION, MESSAGE_HISTORY_URL,FIRST_NAME_POSITION,LAST_NAME_POSITION, COMPANY_NAME_POSITION, TITLE_POSITION, EMAIL_ADDRESS_POSITION, STREET_ADDRESS_POSITION,CITY_POSITION,STATE_POSITION,ZIP_CODE_POSITION,COUNTRY_POSITION
import csv
from datetime import datetime


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
    if len(value) == 0: return -1
    try:
        return int(value)
    except ValueError:
        return -1

# if column is set, return value. if not, return -1
def get_position_infomation():
    return {
        'first_name': convert_string_into_int(FIRST_NAME_POSITION),
        'last_name': convert_string_into_int(LAST_NAME_POSITION),
        'company': convert_string_into_int(COMPANY_NAME_POSITION),
        'title': convert_string_into_int(TITLE_POSITION),
        'email': convert_string_into_int(EMAIL_ADDRESS_POSITION),
        'street': convert_string_into_int(STREET_ADDRESS_POSITION),
        'city': convert_string_into_int(CITY_POSITION),
        'state': convert_string_into_int(STATE_POSITION),
        'zip_code': convert_string_into_int(ZIP_CODE_POSITION),
        'phone_number': convert_string_into_int(COUNTRY_POSITION),
        'country': convert_string_into_int(COUNTRY_POSITION)
    }

def read_contacts_data(file_path):
    position_info = get_position_infomation()
    contact_list = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        index = -1
        for row in csv_reader:
            index += 1
            if index == 0: continue
            contact_list.append({
                'message': replace_values_into_templage(row),
                'phone_number': '1' + row[PHONE_NUMBER_POSITION],
                'first_name': row[position_info['first_name']] if position_info['first_name'] else "unknown",
                'last_name': row[position_info['last_name']] if position_info['last_name'] else "unknown",
                'company': row[position_info['company']] if position_info['company'] else "",
                'title': row[position_info['title']] if position_info['title'] else "",
                'email': row[position_info['email']] if position_info['email'] else "",
                'street': row[position_info['street']] if position_info['street'] else "",
                'city': row[position_info['city']] if position_info['city'] else "",
                'state': row[position_info['state']] if position_info['state'] else "",
                'zip_code': row[position_info['zip_code']] if position_info['zip_code'] else "",
                'country': row[position_info['country']] if position_info['country'] else "",
            })
    return contact_list

def replace_values_into_templage(row):
    message = MESSAGE_TEMPLATE
    for value in REPLACE_POSITIONS.split(','):
        message = message.replace(f'${value}', row[int(value)])
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
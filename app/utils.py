from PIL import Image
import base64
from loguru import logger
from app.settings import CAPTCHA_RESIZED_IMAGE_FILE_PATH, CAPTCHA_TARGET_NAME_QUESTION_ID_MAPPING, MESSAGE_TEMPLATE, REPLACE_POSITIONS, PHONE_NUMBER_POSITION
import csv


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

def read_contacts_data(file_path):
    contact_list = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        index = -1
        for row in csv_reader:
            index += 1
            if index == 0: continue
            contact_list.append({
                'message': replace_values_into_templage(row),
                'phone_number': '1' + row[PHONE_NUMBER_POSITION]
            })
    return contact_list

def replace_values_into_templage(row):
    message = MESSAGE_TEMPLATE
    for value in REPLACE_POSITIONS.split(','):
        message = message.replace(f'${value}', row[int(value)])
    return message
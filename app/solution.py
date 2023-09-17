from pickle import FALSE
from typing import List, Union
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import time
from loguru import logger
from app.captcha_resolver import CaptchaResolver
from app.settings import CAPTCHA_ENTIRE_IMAGE_FILE_PATH, CAPTCHA_SINGLE_IMAGE_FILE_PATH, USER_NAME, PASSWORD, CAPTCHA_SINGLE_IMAGE_FILE_PATH_SERIAL, COTACT_CSV_URL, MESSAGE_TEMPLATE
from app.utils import get_question_id_by_target_name, resize_base64_image, read_contacts_data


class Solution(object):
    def __init__(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.browser = webdriver.Chrome()
        self.browser.get(url)
        self.wait = WebDriverWait(self.browser, 10)
        self.captcha_resolver = CaptchaResolver()
        self.index = 0

    def __del__(self):
        time.sleep(10)
        self.browser.close()

    def get_all_frames(self) -> List[WebElement]:
        self.browser.switch_to.default_content()
        return self.browser.find_elements_by_tag_name('iframe')

    def get_captcha_entry_iframe(self) -> WebElement:
        self.browser.switch_to.default_content()
        captcha_entry_iframe = self.browser.find_element(By.CSS_SELECTOR,
            'iframe[title="reCAPTCHA"]')
        return captcha_entry_iframe

    def switch_to_captcha_entry_iframe(self) -> None:
        captcha_entry_iframe: WebElement = self.get_captcha_entry_iframe()
        self.browser.switch_to.frame(captcha_entry_iframe)

    def get_captcha_content_iframe(self) -> WebElement:
        self.browser.switch_to.default_content()
        captcha_content_iframe = self.browser.find_element(By.CSS_SELECTOR,
            'iframe[src*="bframe?"]')
        return captcha_content_iframe

    def switch_to_captcha_content_iframe(self) -> None:
        captcha_content_iframe: WebElement = self.get_captcha_content_iframe()
        self.browser.switch_to.frame(captcha_content_iframe)

    def get_entire_captcha_element(self) -> WebElement:
        entire_captcha_element: WebElement = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#rc-imageselect-target')))
        return entire_captcha_element

    def get_entire_captcha_natural_width(self) -> Union[int, None]:
        result = self.browser.execute_script(
            "return document.querySelector('div.rc-image-tile-wrapper > img').naturalWidth")
        if result:
            return int(result)
        return None

    def get_entire_captcha_display_width(self) -> Union[int, None]:
        entire_captcha_element = self.get_entire_captcha_element()
        if entire_captcha_element:
            return entire_captcha_element.rect.get('width')
        return None

    def trigger_captcha(self) -> None:
        self.switch_to_captcha_entry_iframe()
        captcha_entry = self.wait.until(EC.presence_of_element_located(
            (By.ID, 'recaptcha-anchor')))
        captcha_entry.click()
        time.sleep(2)
        self.switch_to_captcha_content_iframe()
        entire_captcha_element: WebElement = self.get_entire_captcha_element()
        if entire_captcha_element.is_displayed:
            logger.debug('trigged captcha successfully')

    def get_captcha_target_name(self) -> WebElement:
        captcha_target_name_element: WebElement = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.rc-imageselect-desc-wrapper strong')))
        return captcha_target_name_element.text

    def get_verify_button(self) -> WebElement:
        verify_button = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#recaptcha-verify-button')))
        return verify_button

    def verify_single_captcha(self, index):
        has_object = True
        while has_object: 
            time.sleep(10)
            elements = self.wait.until(EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, '#rc-imageselect-target table td')))
            single_captcha_element: WebElement = elements[index]
            class_name = single_captcha_element.get_attribute('class')
            logger.debug(f'verifiying single captcha {index}, class {class_name}')
            if 'rc-imageselect-tileselected' in class_name:
                logger.debug(f'no new single captcha displayed')
                return
            logger.debug('new single captcha displayed')
            single_captcha_url = single_captcha_element.find_element(By.CSS_SELECTOR,
                'img').get_attribute('src')
            logger.debug(f'single_captcha_url {single_captcha_url}')
            with open(CAPTCHA_SINGLE_IMAGE_FILE_PATH, 'wb') as f:
                f.write(requests.get(single_captcha_url).content)
            with open("".join([CAPTCHA_SINGLE_IMAGE_FILE_PATH_SERIAL, "_", str(index), "_", str(self.index), ".png"]), 'wb') as f:
                self.index += 1
                f.write(requests.get(single_captcha_url).content)
            resized_single_captcha_base64_string = resize_base64_image(
                CAPTCHA_SINGLE_IMAGE_FILE_PATH, (100, 100))
            single_captcha_recognize_result = self.captcha_resolver.create_task(
                resized_single_captcha_base64_string, get_question_id_by_target_name(self.captcha_target_name))
            if not single_captcha_recognize_result:
                logger.error('count not get single captcha recognize result')
                return
            has_object = single_captcha_recognize_result.get(
                'solution', {}).get('hasObject')
            logger.debug(f'HadObject {self.index - 1} {has_object}')
            if has_object is None:
                logger.error('count not get captcha recognized indices')
                return
            if has_object is False:
                logger.debug('no more object in this single captcha')
                return
            if has_object:
                single_captcha_element.click()
                time.sleep(3)
            # check for new single captcha
            # self.verify_single_captcha(index)

    def get_verify_error_info(self):
        self.switch_to_captcha_content_iframe()
        self.browser.execute_script(
            "return document.querySelector('div.rc-imageselect-incorrect-response')?.text")

    def get_is_successful(self):
        self.switch_to_captcha_entry_iframe()
        anchor: WebElement = self.wait.until(EC.visibility_of_element_located((
            By.ID, 'recaptcha-anchor'
        )))
        checked = anchor.get_attribute('aria-checked')
        logger.debug(f'checked {checked}')
        return str(checked) == 'true'

    def get_is_failed(self):
        return bool(self.get_verify_error_info())

    def verify_entire_captcha(self):
        # check the if verify button is displayed
        verify_button: WebElement = self.get_verify_button()
        counter = 0
        while verify_button.is_displayed and verify_button.text != "VERIFY" and counter < 10:
            logger.debug(f'button text {verify_button.text}')
            verify_button.click()
            time.sleep(3)
            verify_button = self.get_verify_button()
            if counter == 10: 
                logger.debug(f'Infinite captcha is more than 10.')
                return FALSE

        self.entire_captcha_natural_width = self.get_entire_captcha_natural_width()
        logger.debug(
            f'entire_captcha_natural_width {self.entire_captcha_natural_width}'
        )
        self.captcha_target_name = self.get_captcha_target_name()
        logger.debug(
            f'captcha_target_name {self.captcha_target_name}'
        )
        entire_captcha_element: WebElement = self.get_entire_captcha_element()
        entire_captcha_url = entire_captcha_element.find_element(By.CSS_SELECTOR,
            'td img').get_attribute('src')
        logger.debug(f'entire_captcha_url {entire_captcha_url}')
        with open(CAPTCHA_ENTIRE_IMAGE_FILE_PATH, 'wb') as f:
            f.write(requests.get(entire_captcha_url).content)
        logger.debug(
            f'saved entire captcha to {CAPTCHA_ENTIRE_IMAGE_FILE_PATH}')
        resized_entire_captcha_base64_string = resize_base64_image(
            CAPTCHA_ENTIRE_IMAGE_FILE_PATH, (self.entire_captcha_natural_width,
                                             self.entire_captcha_natural_width))
        logger.debug(
            f'resized_entire_captcha_base64_string, {resized_entire_captcha_base64_string[0:100]}...')
        entire_captcha_recognize_result = self.captcha_resolver.create_task(
            resized_entire_captcha_base64_string,
            get_question_id_by_target_name(self.captcha_target_name)
        )
        if not entire_captcha_recognize_result:
            logger.error('count not get captcha recognize result')
            return
        recognized_indices = entire_captcha_recognize_result.get(
            'solution', {}).get('objects')
        if not recognized_indices:
            logger.error('count not get captcha recognized indices')
            return
        single_captcha_elements = self.wait.until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, '#rc-imageselect-target table td')))
        logger.debug(f'captcha recogize indices {recognized_indices}')
        for recognized_index in recognized_indices:
            single_captcha_element: WebElement = single_captcha_elements[recognized_index]
            single_captcha_element.click()
            # check if need verify single captcha
            self.verify_single_captcha(recognized_index)

        # after all captcha clicked
        verify_button = self.get_verify_button()
        if verify_button.is_displayed:
            verify_button.click()
            logger.debug('verifed button clicked')
            time.sleep(3)

        is_succeed = self.get_is_successful()
        if is_succeed:
            logger.debug('verifed successfully')
        else:
            verify_error_info = self.get_verify_error_info()
            logger.debug(f'verify_error_info {verify_error_info}')
            # self.verify_entire_captcha()
        # return is_succeed

    def wait_body_loaded(self):
        self.browser.implicitly_wait(20)
    
    def enter_login_info(self):
        username = self.browser.find_element(By.ID, "userid")
        username.send_keys(USER_NAME)
        password = self.browser.find_element(By.ID, "password")
        password.send_keys(PASSWORD)
        remember_me = self.browser.find_element(By.CLASS_NAME, "Vlt-checkbox__button")
        remember_me.click()

    def login(self):
        self.browser.switch_to.default_content()
        login_button: WebElement = self.browser.find_element(By.CLASS_NAME, "login-submit")
        login_button.click()
        time.sleep(30)
        logger.debug(f'current url is {self.browser.current_url}')

    def go_to_sms_page(self):
        self.browser.execute_script(f"window.history.pushState('', '', 'https://app.vonage.com/my-apps/messages/sms')")
        time.sleep(30)
        logger.debug(f'current url is {self.browser.current_url}')

    def get_contacts_data(self):
        return read_contacts_data(COTACT_CSV_URL)

    def get_message_iframe(self) -> WebElement:
        self.browser.switch_to.default_content()
        captcha_entry_iframe = self.browser.find_element(By.CSS_SELECTOR,
            'iframe[src="https://messaging.internal-apps.vonage.com"]')
        return captcha_entry_iframe

    def switch_to_message_iframe(self) -> None:
        captcha_entry_iframe: WebElement = self.get_message_iframe()
        self.browser.switch_to.frame(captcha_entry_iframe)

    def send_sms(self, phone_number, message):
        # click new button
        self.browser.switch_to.default_content()
        new_button = self.browser.find_element(By.CLASS_NAME, "new-button")
        # logger.debug(f'buttons {buttons}')
        # new_button = buttons[1]
        logger.debug(f'new sms button {new_button.get_attribute("outerHTML")}')
        new_button.click()
        time.sleep(1)

        new_dropdowns = self.browser.find_elements(By.CSS_SELECTOR, ".text-ellipsis.item-option-no-border.Vlt-dropdown__link")
        logger.debug(f'buttons {new_dropdowns}')
        new_sms_button = new_dropdowns[1]
        logger.debug(f'new sms button {new_sms_button.get_attribute("outerHTML")}')
        new_sms_button.click()
        time.sleep(3)
        
        # type phone number
        phone_input: WebElement = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#filterElement')))
        logger.debug(f'phone input {phone_input.get_attribute("outerHTML")}')
        phone_input.send_keys(phone_number)
        time.sleep(1)
        
        #click append button
        phone_append_button: WebElement = self.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'button-append')))
        logger.debug(f'phone_append_button {phone_append_button.get_attribute("outerHTML")}')
        phone_append_button.click()
        time.sleep(1)

        #type message
        self.switch_to_message_iframe()
        message_input: WebElement = self.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'ProseMirror')))
        logger.debug(f'phone input {message_input.get_attribute("outerHTML")}')
        message_input.send_keys(message)
        time.sleep(3)

        #send message
        message_send_icon: WebElement = self.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'icon-template-purple')))
        logger.debug(f'phone input {message_send_icon.get_attribute("outerHTML")}')
        message_send_icon.click()
        time.sleep(5)

    def convert_message(self, name, address):
        message = MESSAGE_TEMPLATE.replace('$name', name)
        message = message.replace('$address', address)
        return message

    def send_messages_to_contacts(self):
        contacts_data = self.get_contacts_data()
        for index, item in enumerate(contacts_data):
            if index > 10: break
            self.send_sms(item['phone_number'], item['message'])

    def resolve(self):
        self.wait_body_loaded()
        self.enter_login_info()
        self.trigger_captcha()
        self.verify_entire_captcha()
        self.login()
        self.go_to_sms_page()
        self.send_messages_to_contacts()
        
        
        

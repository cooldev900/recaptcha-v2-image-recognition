from typing import List, Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

import time
from loguru import logger
from app.settings import USER_NAME, PASSWORD, MIN_RAND,MAX_RAND
from app.utils import read_contacts_data, write_message_history, contact_create_history, contact_create_failed_history
from random import uniform
import numpy as np
import scipy.interpolate as si
import os


class Solution(object):
    def __init__(self, url, file_path, columns, begin_row, end_row):
        self.file_path = file_path
        self.columns = columns
        self.begin_row = begin_row
        self.end_row = end_row
        # options = webdriver.ChromeOptions()
        # path = os.path.abspath("./buster_captcha_solver_2.0.1_0.crx")
        # options.add_extension(path)
        self.browser = webdriver.Chrome()
        

        self.browser.get(url)
        self.wait = WebDriverWait(self.browser, 100)
        self.index = 0
    
     # Using B-spline for simulate humane like mouse movments
    def human_like_mouse_move(self, action, start_element):
        points = [[6, 2], [3, 2],[0, 0], [0, 2]];
        points = np.array(points)
        x = points[:,0]
        y = points[:,1]

        t = range(len(points))
        ipl_t = np.linspace(0.0, len(points) - 1, 100)

        x_tup = si.splrep(t, x, k=1)
        y_tup = si.splrep(t, y, k=1)

        x_list = list(x_tup)
        xl = x.tolist()
        x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        yl = y.tolist()
        y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

        x_i = si.splev(ipl_t, x_list)
        y_i = si.splev(ipl_t, y_list)

        startElement = start_element

        action.move_to_element(startElement)
        action.perform()

        c = 5 # change it for more move
        i = 0
        for mouse_x, mouse_y in zip(x_i, y_i):
            action.move_by_offset(mouse_x,mouse_y)
            action.perform()
            logger.debug(f"Move mouse to ({mouse_x}, {mouse_y})")
            i += 1
            if i == c:
                break
    
    def wait_between(self, a, b):
        rand=uniform(a, b)
        time.sleep(rand)

    # def __del__(self):
    #     time.sleep(10)
    #     self.browser.close()

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

    def get_entire_captcha_natural_width(self) -> Union[int, None]:
        result = self.browser.execute_script(
            "return document.querySelector('div.rc-image-tile-wrapper > img').naturalWidth")
        if result:
            return int(result)
        return None

    def do_captcha(self) -> None:
        self.switch_to_captcha_entry_iframe()
        captcha_entry = self.wait.until(EC.visibility_of_element_located(
            (By.ID, 'recaptcha-anchor')))
        self.wait_between(MIN_RAND, MAX_RAND)
        action = ActionChains(self.browser)
        self.human_like_mouse_move(action, captcha_entry)
        captcha_entry.click()
        time.sleep(2)
        if captcha_entry.get_attribute('aria-checked') == "true": return
        else:
            while captcha_entry.get_attribute('aria-checked') != "true":
                time.sleep(1)


    def get_captcha_target_name(self) -> WebElement:
        captcha_target_name_element: WebElement = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.rc-imageselect-desc-wrapper strong')))
        return captcha_target_name_element.text

    def get_verify_button(self) -> WebElement:
        verify_button = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '#recaptcha-verify-button')))
        return verify_button

    def wait_body_loaded(self):
        self.browser.implicitly_wait(20)

    def enter_login_info(self):
        username = self.wait.until(EC.visibility_of_element_located(
            (By.ID, "userid")))
        username.send_keys(USER_NAME)
        password = self.wait.until(EC.visibility_of_element_located(
            (By.ID, "password")))
        password.send_keys(PASSWORD)
        remember_me = self.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "Vlt-checkbox__button")))
        remember_me.click()

    def login(self):
        self.browser.switch_to.default_content()
        login_button: WebElement = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//vwc-button[@data-aid="login-button"]')))
        login_button.click()
        self.wait.until(EC.url_to_be("https://app.vonage.com/whats-new"))
        logger.debug(f'current url is {self.browser.current_url}')

    def go_to_sms_page(self):
        self.browser.switch_to.default_content()
        contact_dropdown = self.browser.find_element(
            By.CSS_SELECTOR, 'a[href="/my-apps/messages/sms"]')
        contact_dropdown.click()
        self.wait.until(EC.url_to_be(
            "https://app.vonage.com/my-apps/messages/sms"))
        logger.debug(f'current url is {self.browser.current_url}')

    def get_contacts_data(self):
        return read_contacts_data(self.file_path, self.columns, self.begin_row, self.end_row)

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
        new_button.click()
        time.sleep(1)

        new_dropdowns = self.browser.find_elements(
            By.CSS_SELECTOR, ".text-ellipsis.item-option-no-border.Vlt-dropdown__link")
        new_sms_button = new_dropdowns[1]
        new_sms_button.click()
        time.sleep(2)

        # type phone number
        phone_input: WebElement = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '#filterElement')))
        phone_input.send_keys(phone_number)

        # click append button
        phone_append_button: WebElement = self.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'button-append')))
        phone_append_button.click()

        # type message
        self.switch_to_message_iframe()
        message_input: WebElement = self.wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, 'ProseMirror')))
        message_input.send_keys(message)

        # send message
        message_send_icon: WebElement = self.wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, 'icon-template-purple')))
        message_send_icon.click()
        time.sleep(2)

    def send_messages_to_contacts(self):
        contacts_data = self.get_contacts_data()
        total = 0
        for index, item in enumerate(contacts_data, start=1):
            self.send_sms(item['phone_number'], item['message'])
            write_message_history(item['phone_number'], item['message'])
            total += 1

        self.browser.quit()
        logger.debug(f'Total {total} of messages were sent successfully')
        return f'Total {total} of messages were sent successfully'

    def go_to_contact_page(self):
        self.browser.switch_to.default_content()
        contact_dropdown = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 'a[href="/contacts"]'
        )))
        contact_dropdown.click()
        self.wait.until(EC.url_to_be("https://app.vonage.com/contacts"))
        logger.debug(f'current url is {self.browser.current_url}')

    def create_contacts(self):
        contacts_data = self.get_contacts_data()
        total = 0
        for index, item in enumerate(contacts_data, start=1):
            successful = self.create_contact(item)
            if successful:
                total += 1
                contact_create_history(item)
                logger.debug(
                    f"The {index}th row of contact was created successfully")
            else:
                contact_create_failed_history(item)
                logger.debug(
                    f"The {index}th row of contact was created successfully")
        logger.debug(f'Total {total} of contacts were created successfully')

    def create_contact(self, item):
        # click new contact button
        new_button = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, '//button[@data-cy="title-button"]'
        )))
        new_button.click()

        self.wait.until(EC.visibility_of_element_located((
            By.XPATH, '//div[@data-cy="edit-contact-modal"]'
        )))

        first_name = self.wait.until(EC.visibility_of_element_located((
            By.XPATH, '//vwc-textfield[@data-cy="edit-contact-first-name"]'
        )))
        first_name = first_name.find_element(By.TAG_NAME, 'input')
        first_name.send_keys(item['first_name'])

        if len(item['last_name']) > 0:
            last_name = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, '//vwc-textfield[@data-cy="edit-contact-last-name"]'
            )))
            last_name = last_name.find_element(By.TAG_NAME, 'input')

            last_name.send_keys(item['last_name'])

        if len(item['company']) > 0:
            company_name = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, '//vwc-textfield[@data-cy="edit-contact-company-name"]'
            )))
            company_name = company_name.find_element(By.TAG_NAME, 'input')

            company_name.send_keys(item['company'])

        if len(item['title']) > 0:
            title = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, '//vwc-textfield[@data-cy="edit-contact-title-name"]'
            )))

            title.send_keys(item['title'])

        phone_number_collpase = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, '//div[@data-cy="phone-number-block"]/div[1]'
        )))
        phone_number_collpase.click()

        phone_number_block0 = self.wait.until(EC.visibility_of_element_located((
            By.XPATH, '//div[@data-cy="edit-contact-phone-number-0"]'
        )))
        phone_number_input = phone_number_block0.find_element(
            By.TAG_NAME, 'input')
        phone_number_input.send_keys(item['phone_number'])

        if len(item['email']) > 0:
            email_address_collpase = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, '//div[@data-cy="email-block"]/div[1]'
            )))
            email_address_collpase.click()

            email_address_block0 = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, '//div[@data-cy="email-block"]/div[2]'
            )))
            email_address_input = email_address_block0.find_element(
                By.TAG_NAME, 'input')
            email_address_input.send_keys(item['email'])

        street_address_collpase = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, '//div[@data-cy="address-block"]/div[1]'
        )))
        street_address_collpase.click()

        street_address_block0 = self.wait.until(EC.visibility_of_element_located((
            By.XPATH, '//div[@data-cy="address-block"]/div[2]/div[1]/div[2]/div[2]'
        )))

        if len(item['street']) > 0:
            city_input = street_address_block0.find_element(
                By.XPATH, '//div[@data-cy="edit-contact-address"]/div[1]/div[1]/input[1]')
            city_input.send_keys(item['street'])
        if len(item['city']) > 0:
            city_input = street_address_block0.find_element(
                By.XPATH, '//div[@data-cy="edit-contact-city"]/div[1]/div[1]/input[1]')
            city_input.send_keys(item['city'])

        if len(item['state']) > 0:
            state_input = street_address_block0.find_element(
                By.XPATH, '//div[@data-cy="edit-contact-state"]/div[1]/div[1]/input[1]')
            state_input.send_keys(item['state'])

        if len(item['zip_code']) > 0:
            zip_input = street_address_block0.find_element(
                By.XPATH, '//div[@data-cy="edit-contact-zipCode"]/div[1]/div[1]/input[1]')
            zip_input.send_keys(item['zip_code'])

        if len(item['country']):
            country_input = street_address_block0.find_element(
                By.XPATH, '//div[@data-cy="edit-contact-country"]/div[1]/div[1]/input[1]')
            country_input.send_keys(item['country'])

        create_button = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, '//div[@class="save-cancel"]/button[2]'
        )))
        if "Vlt-btn--disabled" in create_button.get_attribute('class'):
            close_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, '//div[@class="save-cancel"]/button[1]'
            )))
            close_button.click()
            return False
        else:
            create_button.click()
            time.sleep(2)
            return True

    def resolve(self):
        self.wait_body_loaded()
        self.enter_login_info()
        self.do_captcha()        
        self.login()
        self.go_to_contact_page()
        self.create_contacts()
        self.go_to_sms_page()
        return self.send_messages_to_contacts()

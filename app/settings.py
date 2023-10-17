from environs import Env

env = Env()
env.read_env()

CAPTCHA_DEMO_URL = env.str('CAPTCHA_DEMO_URL')

USER_NAME = env.str('USER_NAME')
PASSWORD = env.str('PASSWORD')
MESSAGE_HISTORY_URL = env.str('MESSAGE_HISTORY_URL')

CAPTCHA_ENTIRE_IMAGE_FILE_PATH = 'csv/captcha_entire_image.png'
CAPTCHA_SINGLE_IMAGE_FILE_PATH = 'csv/captcha_single_image.png'
CAPTCHA_SINGLE_IMAGE_FILE_PATH_SERIAL = 'csv/captcha_single_image'
CAPTCHA_RESIZED_IMAGE_FILE_PATH = 'csv/captcha_resized_image.png'

# Randomization Related
MIN_RAND        = 0.64
MAX_RAND        = 1.27
LONG_MIN_RAND   = 4.78
LONG_MAX_RAND = 11.1
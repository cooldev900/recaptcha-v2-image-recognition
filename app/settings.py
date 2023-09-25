from environs import Env

env = Env()
env.read_env()

CAPTCHA_RESOLVER_API_URL = 'https://api.yescaptcha.com/createTask'
CAPTCHA_RESOLVER_API_KEY = env.str('CAPTCHA_RESOLVER_API_KEY')

CAPTCHA_DEMO_URL = env.str('CAPTCHA_DEMO_URL')

USER_NAME = env.str('USER_NAME')
PASSWORD = env.str('PASSWORD')

CAPTCHA_ENTIRE_IMAGE_FILE_PATH = 'csv/captcha_entire_image.png'
CAPTCHA_SINGLE_IMAGE_FILE_PATH = 'csv/captcha_single_image.png'
CAPTCHA_SINGLE_IMAGE_FILE_PATH_SERIAL = 'csv/captcha_single_image'
CAPTCHA_RESIZED_IMAGE_FILE_PATH = 'csv/captcha_resized_image.png'

COTACT_CSV_URL = env.str('COTACT_CSV_URL')
START_ROW_INDEX = env.str('START_ROW_INDEX')
END_ROW_INDEX = env.str('END_ROW_INDEX')
MESSAGE_TEMPLATE = env.str('MESSAGE_TEMPLATE')
PHONE_NUMBER = env.str('PHONE_NUMBER')
MESSAGE_HISTORY_URL = env.str('MESSAGE_HISTORY_URL')

FIRST_NAME = env.str('FIRST_NAME')
LAST_NAME = env.str('LAST_NAME')
COMPANY_NAME = env.str('COMPANY_NAME')
TITLE = env.str('TITLE')
EMAIL_ADDRESS = env.str('EMAIL_ADDRESS')
STREET_ADDRESS = env.str('STREET_ADDRESS')
CITY = env.str('CITY')
STATE = env.str('STATE')
ZIP_CODE = env.str('ZIP_CODE')
COUNTRY = env.str('COUNTRY')

# Randomization Related
MIN_RAND        = 0.64
MAX_RAND        = 1.27
LONG_MIN_RAND   = 4.78
LONG_MAX_RAND = 11.1


# Update this list with proxybroker http://proxybroker.readthedocs.io
PROXY =[
{"host": "34.65.217.248", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.15, "error_rate": 0.0},
{"host": "198.46.160.38", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.36, "error_rate": 0.0},
{"host": "18.162.100.154", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.62, "error_rate": 0.0},
{"host": "18.210.69.172", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.22, "error_rate": 0.0},
{"host": "204.12.202.198", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.3, "error_rate": 0.0},
{"host": "23.237.100.74", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.32, "error_rate": 0.0},
{"host": "206.189.192.5", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.63, "error_rate": 0.0},
{"host": "23.237.173.109", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.4, "error_rate": 0.0},
{"host": "167.71.83.150", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.41, "error_rate": 0.0},
{"host": "34.93.171.222", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.92, "error_rate": 0.0},
{"host": "157.245.67.128", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.61, "error_rate": 0.0},
{"host": "18.162.89.135", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.71, "error_rate": 0.0},
{"host": "198.98.55.168", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.65, "error_rate": 0.0},
{"host": "157.245.124.217", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.7, "error_rate": 0.0},
{"host": "129.146.181.251", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.76, "error_rate": 0.0},
{"host": "134.209.188.111", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.78, "error_rate": 0.0},
{"host": "68.183.191.140", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.82, "error_rate": 0.0},
{"host": "35.192.138.9", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.29, "error_rate": 0.0},
{"host": "157.245.207.112", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.85, "error_rate": 0.0},
{"host": "68.183.191.248", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.87, "error_rate": 0.0},
{"host": "165.22.54.37", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.88, "error_rate": 0.0},
{"host": "71.187.28.75", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.34, "error_rate": 0.0},
{"host": "157.245.205.81", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.92, "error_rate": 0.0},
{"host": "45.76.255.157", "port": 808, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.45, "error_rate": 0.0},
{"host": "157.245.197.92", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 1.01, "error_rate": 0.0},
{"host": "159.203.87.130", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.47, "error_rate": 0.0},
{"host": "50.195.185.171", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 1.03, "error_rate": 0.0},
{"host": "144.202.20.56", "port": 808, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.51, "error_rate": 0.0},
{"host": "157.230.250.116", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 1.14, "error_rate": 0.0},
{"host": "104.196.70.154", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.64, "error_rate": 0.0}
]


import json
CAPTCHA_TARGET_NAME_QUESTION_ID_MAPPING = {
    "taxis": "/m/0pg52",
    "bus": "/m/01bjv",
    "school bus": "/m/02yvhj",
    "motorcycles": "/m/04_sv",
    "tractors": "/m/013xlm",
    "chimneys": "/m/01jk_4",
    "crosswalks": "/m/014xcs",
    "traffic lights": "/m/015qff",
    "bicycles": "/m/0199g",
    "parking meters": "/m/015qbp",
    "cars": "/m/0k4j",
    "vehicles": "/m/0k4j",
    "bridges": "/m/015kr",
    "boats": "/m/019jd",
    "palm trees": "/m/0cdl1",
    "mountains or hills": "/m/09d_r",
    "fire hydrant": "/m/01pns0",
    "fire hydrants": "/m/01pns0",
    "a fire hydrant": "/m/01pns0",
    "stairs": "/m/01lynh",
    "出租车": "/m/0pg52",
    "巴士": "/m/01bjv",
    "摩托车": "/m/04_sv",
    "机动车": "/m/0k4j",
    "小轿车": "/m/0k4j",
    "拖拉机": "/m/013xlm",
    "烟囱": "/m/01jk_4",
    "人行横道": "/m/014xcs",
    "红绿灯": "/m/015qff",
    "自行车": "/m/0199g",
    "停车计价表": "/m/015qbp",
    "汽车": "/m/0k4j",
    "桥": "/m/015kr",
    "船": "/m/019jd",
    "棕榈树": "/m/0cdl1",
    "山": "/m/09d_r",
    "消防栓": "/m/01pns0",
    "楼梯": "/m/01lynh",
    "交通工具": "/m/0k4j",
    "公交车": "/m/01bjv",
    "彩色玻璃": "/m/011y23",
    "火车站": "/m/0py27",
    "消火栓": "/m/01pns0",
    "过街人行道": "/m/014xcs",
    "车库门": "/m/08l941",
    "公交站": "/m/01jw_1",
    "停车计时器": "/m/015qbp",
    "丘陵": "/m/09d_r",
    "车辆": "/m/0k4j",
    "公共汽车": "/m/01bjv",
    "交通灯": "/m/015qff",
    "停车咪表": "/m/015qbp"
}
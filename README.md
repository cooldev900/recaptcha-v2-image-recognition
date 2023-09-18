# VONAGE SMS SENDER

Sms sender in vonage platform using selenium

## Usage

Clone this repo:

```
https://github.com/cooldev900/recaptcha-v2-image-recognition.git
```

Then go to [https://yescaptcha.com/](https://yescaptcha.com/auth/register) and register your account, then get a `clientKey` from portal.

![image](https://github.com/cooldev900/recaptcha-v2-image-recognition/assets/13826499/de792d6d-b2ce-499d-9a3f-7e73af954c44)



Then create a `.env` file in root of this repo, and write this content:

```
CAPTCHA_RESOLVER_API_KEY=<Your Client Key>
CAPTCHA_DEMO_URL=<vonage login url>
USER_NAME=<username>
PASSWORD=<password>

COTACT_CSV_URL=<contact csv file path>

PHONE_NUMBER_POSITION=<column position in csv, i.e. 38>
REPLACE_POSITIONS=<column positions which will be replaced when creating new message from message template in csv, i.e. "0,36,37">

MESSAGE_TEMPLATE="Hello $36 $37,\n My name is Connor.\n I'm looking to acquire a few properties in the area.\n If you are the owner of $0, would you consider an offer?"
```

Next, you need to install packages:

```
pip3 install -r requirements.txt
```

At last, run demo:

```
python3 main.py
```

Result:

![image](https://github.com/cooldev900/recaptcha-v2-image-recognition/assets/13826499/bde10300-362a-4e97-86b5-9f969b8a006c)



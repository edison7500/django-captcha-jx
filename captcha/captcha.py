from captcha.settings import api_settings as settings


class Captcha(object):


    def __init__(self):

        self.size = settings.CAPTCHA_IMAGE_SIZE
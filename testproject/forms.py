from django import forms
from captcha.fields import CaptchaField


class TestCaptchaForm(forms.Form):
    captcha_code = CaptchaField(
        required=True,
    )
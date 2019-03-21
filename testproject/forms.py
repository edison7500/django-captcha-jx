import logging
from django import forms
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField

logger = logging.getLogger('django')


class TestCaptchaForm(forms.Form):
    captcha_code = CaptchaField(
        required=True,
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_captcha_code(self):
        _captcha_code = self.cleaned_data.get('captcha_code').upper()
        cache_key = self.request.session.get('captcha')
        real_value = cache.get(cache_key)
        logger.info(real_value)
        logger.info(_captcha_code)
        cache.delete(cache_key)
        if _captcha_code != real_value:
            raise ValidationError(_("captcha error"))
        return _captcha_code

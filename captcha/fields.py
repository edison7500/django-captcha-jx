import logging
from django import forms
from django.core.urlresolvers import reverse
from django.forms.utils import flatatt
from django.utils.html import format_html

logger = logging.getLogger('captcha')


class CaptchaTextInput(forms.Widget):
    def __init__(self, attrs=None):
        super(CaptchaTextInput, self).__init__(attrs)

    def build_attrs(self, *args, **kwargs):
        """Disable automatic corrections and completions."""
        attrs = super(CaptchaTextInput, self).build_attrs(*args, **kwargs)
        attrs['autocapitalize'] = 'off'
        attrs['autocomplete'] = 'off'
        attrs['autocorrect'] = 'off'
        attrs['spellcheck'] = 'false'
        return attrs

    def image_url(self):
        return reverse('captcha-image')

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(base_attrs={"name": name}, extra_attrs=attrs)
        _input = format_html(u'<input{} />', flatatt(final_attrs))
        _code_img = format_html(u'<img class="c-image" src={image_url}>'.format(image_url=self.image_url()))
        return _input + _code_img


class CaptchaField(forms.Field):
    widget = CaptchaTextInput

    def __init__(self, *args, **kwargs):
        super(CaptchaField, self).__init__(*args, **kwargs)

    def validate(self, value):
        logger.info(value)
        super().validate(value)

    def clean(self, value):
        super(CaptchaField, self).clean(value)
        return value.lower()

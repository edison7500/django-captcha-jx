import random

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageFilter
)

from captcha import helpers

try:
    from cStringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

from captcha.conf.settings import api_settings as settings


def filter_default(image):
    return helpers.filter_smooth(image, ImageFilter.SMOOTH)


def noise_default(image, draw):
    color = settings.CAPTCHA_FOREGROUND_FUNCTION
    draw = helpers.noise_dots(draw, image, color())
    draw = helpers.noise_arcs(draw, image, color())


def getsize(font, text):
    if hasattr(font, 'getoffset'):
        return tuple(
            [x + y for x, y in zip(font.getsize(text), font.getoffset(text))])
    else:
        return font.getsize(text)


def makeimg(size):
    if settings.CAPTCHA_BACKGROUND_COLOR == "transparent":
        image = Image.new('RGBA', size)
    else:
        image = Image.new('RGB', size, settings.CAPTCHA_BACKGROUND_COLOR)
    return image


class Captcha(object):
    xpos = 2
    from_top = 4

    def __init__(self, word):
        self.size = settings.CAPTCHA_IMAGE_SIZE
        self.word = word
        self.font = ImageFont.truetype(
            settings.CAPTCHA_FONT_PATH,
            settings.CAPTCHA_FONT_SIZE
        )

    def generate_image(self):
        image = makeimg(self.size)
        for char in self.word:
            fgimage = Image.new('RGB', self.size, settings.CAPTCHA_FOREGROUND_COLOR)
            charimage = Image.new('L', getsize(self.font, ' %s ' % char), '#000000')
            chardraw = ImageDraw.Draw(charimage)
            chardraw.text((0, 0), ' %s ' % char, font=self.font, fill='#ffffff')
            if settings.CAPTCHA_LETTER_ROTATION:
                angle = random.randrange(*settings.CAPTCHA_LETTER_ROTATION)
                charimage = charimage.rotate(
                    angle, expand=0, resample=Image.BICUBIC)

            charimage = charimage.crop(charimage.getbbox())
            maskimage = Image.new('L', self.size)

            xpos2 = self.xpos + charimage.size[0]
            from_top2 = self.from_top + charimage.size[1]
            maskimage.paste(charimage, (self.xpos, self.from_top, xpos2, from_top2))
            size = maskimage.size
            image = Image.composite(fgimage, image, maskimage)
            self.xpos = self.xpos + 2 + charimage.size[0]

        if settings.CAPTCHA_IMAGE_SIZE:
            # centering captcha on the image
            tmpimg = makeimg(size)
            xpos2 = int((size[0] - self.xpos) / 2)
            from_top2 = int((size[1] - charimage.size[1]) / 2 - self.from_top)
            tmpimg.paste(image, (xpos2, from_top2))
            image = tmpimg.crop((0, 0, size[0], size[1]))
        else:
            image = image.crop((0, 0, self.xpos + 1, size[1]))

        draw = ImageDraw.Draw(image)

        settings.FILTER_FUNCTION(image)
        settings.NOISE_FUNCTION(image, draw)

        out = StringIO()
        image.save(out, 'PNG')
        content = out.getvalue()
        out.seek(0)
        out.close()

        return content

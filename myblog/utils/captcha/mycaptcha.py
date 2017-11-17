import random
import string
import sys
import math
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from django.conf import settings
from django.core.cache import cache


class Captcha(object):

    font_path = 'utils/captcha/verdana.ttf'
    number = 4
    size = (100,30)
    bgcolor = (255,255,255)
    fontcolor = (random.randint(0, 100),random.randint(0, 100),random.randint(0, 100))
    fontsize = 25
    linecolor = (random.randint(0,100),random.randint(0,100),random.randint(0,100))
    draw_line = True
    draw_point = True
    line_number = 2

    @classmethod
    def __gene_text(cls):
        source = list(string.ascii_letters)
        for index in range(0,10):
            source.append(str(index))
        return ''.join(random.sample(source,cls.number))

    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill = cls.linecolor)

    @classmethod
    def __gene_points(cls, draw, point_chance, width,height):
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w,h), fill=(0, 0, 0))

    @classmethod
    def gene_code(cls):
        width,height = cls.size
        image = Image.new('RGBA', (width, height), cls.bgcolor)
        font = ImageFont.truetype(cls.font_path, cls.fontsize)
        draw = ImageDraw.Draw(image)
        text = cls.__gene_text()
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / 2, (height - font_height) /8), text, font = font,fill = cls.fontcolor)

        if cls.draw_line:
            for i in range(0, cls.line_number):
                cls.__gene_line(draw, width, height)

        if cls.draw_point:
            cls.__gene_points(draw, 10, width, height)



        cache.set(text.lower(),text.lower(),120)
        return (text,image)



    @classmethod
    def check_captcha(cls, captcha):
        captcha_cache = cache.get(captcha)
        if captcha_cache and captcha_cache == captcha:
            cache.delete(captcha)
            return True
        else:
            return False
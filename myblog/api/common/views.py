from django.http import HttpResponse
from utils.captcha.mycaptcha import Captcha
from django.shortcuts import render,redirect,reverse
from PIL import Image
from django.core.cache import cache
from io import BytesIO as StringIO

def common_captcha(request):
    text,image = Captcha.gene_code()
    out = StringIO()
    image.save(out,'png')
    out.seek(0)
    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    # image.save(r'C:\Users\J\Desktop\captcha.png','png')
    # print(image)
    # print(response)
    return response
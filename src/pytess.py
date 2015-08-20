# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image

img = Image.open('../img/8.jpg') # 读入图片
img.show()
img = img.convert("RGBA")
pixdata = img.load()
#二值化
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][0] < 90:
            pixdata[x, y] = (0, 0, 0, 255)
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][1] < 136:
            pixdata[x, y] = (0, 0, 0, 255)
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][2] > 0:
            pixdata[x, y] = (255, 255, 255, 255)
img.show()

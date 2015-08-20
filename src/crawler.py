# -*- coding: utf-8 -*-
import urllib
import random

def getImage(url, file_path):
    u = urllib.urlopen(url)
    data = u.read()

    f = open(file_path, 'wb')
    f.write(data)
    f.close()

for i in range(100):
    rand = random.random()
    url = "http://202.119.113.135/validateCodeAction.do?random=" + str(rand);
    print url
    file_path = "../train/" + str(i) + ".jpg"
    getImage(url,file_path)

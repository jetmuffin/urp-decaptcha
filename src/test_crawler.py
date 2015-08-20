# -*- coding: utf-8 -*-
import sys 
import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re  
from segmentation import NormalSegmenter
from feature_extraction import SimpleFeatureExtractor
from analyzer import KNNAnalyzer
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')

def getCheckCode(url):
    print "+"*20+"getCheckCode"+"+"*20
    response = urllib2.urlopen(url)
    status = response.getcode()
    picData = response.read()
     
    path = "../tmp/vcode.jpg"
    if status == 200:
        localPic = open(path, "wb")
        localPic.write(picData)
        localPic.close() 
        print "保存验证码图片在%s，开始解析验证码..."%path  
        result = analyzer.analyze('../tmp/vcode.jpg')
        if result == None:
            print "解析失败..."
            postData["v_yzm"] = 'Error'
        else:
            print "解析成功，解析结果：%s"%result
            postData["v_yzm"] = result
    else:
        print "failed to get Check Code, status: ",status

def sendPostData(url, data, header):
    print "+"*20+"sendPostData"+"+"*20
    data = urllib.urlencode(data)      
    request = urllib2.Request(url, data, header)
    response = urllib2.urlopen(request)
    #url = response.geturl()
    text = response.read().decode("gbk")
    info = response.info()
    status = response.getcode()
    response.close()
    print status
    print info
    key = '学分制综合教务'
    if key in text:
        print 'Login Successful !!'
        return True
    else:
        print 'Login Failed ...'
        return False
    # print "Response:", text

def login(login_url, vcode_url, postData, headers):
    cookiejar = cookielib.LWPCookieJar()#LWPCookieJar提供可读写操作的cookie文件,存储cookie对象
    cookieSupport= urllib2.HTTPCookieProcessor(cookiejar)
    opener = urllib2.build_opener(cookieSupport, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    #打开登陆页面
    urllib2.urlopen(login_url)
    #此时直接发送post数据包登录
    getCheckCode(vcode_url)
    success_test, failed_test = 0, 0
    return sendPostData(login_url, postData, headers)

if __name__ == "__main__":
    print "初始化分类器..."
    segmenter = NormalSegmenter()
    extractor = SimpleFeatureExtractor( feature_size=20, stretch=False )

    analyzer = KNNAnalyzer( segmenter, extractor)
    analyzer.train('../data/features.jpg')

    print "开始模拟登录..."
    login_url = "http://202.119.113.135/loginAction.do"
    vcode_url = 'http://202.119.113.135/validateCodeAction.do?random=0.2583906068466604'

    #post请求头部
    headers = {
        'x-requestted-with': 'XMLHttpRequest',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate',
        'ContentType': 'application/x-www-form-urlencoded; chartset=UTF-8',
        'Host':    'login.taobao.com',
        'DNT': 1,
        'Cache-Control': 'no-cache',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',  
        'Referer' : 'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fwww.taobao.com%2F',
        'Connection' : 'Keep-Alive'
    }
    #用户名，密码
    username = "1206010411"
    password = "130033"
    #请求数据包
    postData = {   
        'zjh':username, 
        'mm':password,             
    }

    test_number = 3000
    success_test, failed_test = 0, 0
    start = time.time()
    for i in range(test_number):
        print "测试第 %d 个样例子"%i
        if login(login_url, vcode_url, postData, headers):
            success_test += 1
        else:
            failed_test += 1
    end = time.time()

    print "测试 %d 次登录，共耗时 %f s"%(test_number,end-start)
    print "成功测试样例 %d 个，失败测试样例 %d 个，成功率 %f %%"%(success_test,failed_test,float(float(success_test)/float(success_test+failed_test)*100))



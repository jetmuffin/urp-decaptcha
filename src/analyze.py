# -*- coding: utf-8 -*-

import cv2   
import cv
import numpy as np  

class Analyzer(object):
  def __init__(self, img_path):
    self.img_path = img_path
    self.img = cv2.imread(self.img_path)
    self.rows, self.cols, self.channel = self.img.shape
    self.height, self.width = self.img.shape[:2]

  def analyze(self):
    imgray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)    
    ret,self.img = cv2.threshold(imgray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #finding the bounding of character 
    #adding the bound to avoid error
    # self.img = cv2.copyMakeBorder(self.img,5,5,5,5,cv2.BORDER_CONSTANT,value=(255,255,255))
    # ret,thresh = cv2.threshold(imgray,127,255,cv2.THRESH_BINARY)
    # contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    # x,y,w,h = cv2.boundingRect(contours[2])
    # print x,y,w,h
    # cv2.drawContours(self.img, contours, -1, (0,0,255), 1)
    """quzao"""
    direct=[[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]]
    w,h = self.img.shape[:2]
    for x in range(0,w - 1):
      for y in range(0,h - 1):
        flag = True
        if(self.img[x][y] == 0):
          for (a,b) in direct:
            if(self.img[x+a][y+b] == 0):
              flag = False
              break
          if(flag):
            self.img[x][y] = 255
    """split"""
    # self.img = cv2.copyMakeBorder(self.img,5,5,5,5,cv2.BORDER_CONSTANT,value=(255,255,255))
    ret,thresh = cv2.threshold(imgray,127,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    x,y,w,h = cv2.boundingRect(contours[6])
    print x,y,w,h
    roi = self.img[y:y+h,x:x+w]
    print roi
    # threshold = 2
    # xpix = [0 for self.cols in range(self.width)]
    # for i in range(self.rows - 1):
    #   for j in range(self.cols - 1):
    #     if(self.img[i,j] == 0):
    #       xpix[j] += 1
    # print xpix
    # for i in range(len(xpix)):
    #   if(xpix[i-1] < threshold and xpix[i] >= threshold):
    #     print i

  #print code
  def show(self):
    cv2.namedWindow("Image")   
    cv2.imshow("Image", self.img)   
    cv2.waitKey (0)  

# For testing
if __name__ == '__main__':
  analyzer = Analyzer("../img/9.jpg")
  analyzer.analyze()
  analyzer.show()

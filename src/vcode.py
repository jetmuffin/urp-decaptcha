# -*- coding: utf-8 -*-

import cv2   
import cv
import numpy

SEGMENT_DATATYPE=   numpy.uint16
SEGMENT_SIZE=       4
SEGMENTS_DIRECTION= 0 # vertical axis in numpy

def show(img):
  cv2.namedWindow("Image")   
  cv2.imshow("Image", img)   
  cv2.waitKey (0)  

def segments_to_numpy( segments ):
    '''given a list of 4-element tuples, transforms it into a numpy array'''
    segments= numpy.array( segments, dtype=SEGMENT_DATATYPE, ndmin=2)   #each segment in a row
    segments= segments if SEGMENTS_DIRECTION==0 else numpy.transpose(segments)
    return segments

img_path = "../img/5.jpg"
img = cv2.imread(img_path)
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)    
ret,img = cv2.threshold(imgray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
"""quzao"""
direct=[[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]]
w,h = img.shape[:2]
for x in range(0,w - 1):
  for y in range(0,h - 1):
    flag = True
    if(img[x][y] == 0):
      for (a,b) in direct:
        if(img[x+a][y+b] == 0):
          flag = False
          break
      if(flag):
        img[x][y] = 255

"""split"""
xpix = [0 for col in range(h)]
for i in range(w - 1):
  for j in range(h - 1):
    if(img[i,j] == 0):
      xpix[j] += 1
print xpix
left_coord = []
right_coord = []

for i in range(len(xpix) - 1):
  if(xpix[i] == 0 and xpix[i+1] > 0):
    left_coord.append(i)
  if(xpix[i] > 0 and xpix[i+1] == 0):
    right_coord.append(i+1)

if(len(left_coord) != len(right_coord)):
  print 'error'
top_coord = []
bottom_coord = []
for c in range(len(left_coord)):
  l,r = left_coord[c],right_coord[c]
  ypix = [0 for col in range(w)]
  for i in range(w - 1):
    for j in range(l,r):
      if(img[i,j] == 0):
        ypix[i] += 1
  for i in range(len(ypix) - 1):
    if(ypix[i] == 0 and ypix[i+1] > 0):
      top_coord.append(i)
    if(ypix[i] > 0 and ypix[i+1] == 0):
      bottom_coord.append(i+1)

if(len(top_coord) != len(bottom_coord) or len(top_coord) != len(left_coord)):
  print 'error'

param = []
for i in range(len(left_coord)):
  param.append((left_coord[i],top_coord[i],right_coord[i]-left_coord[i]+1,bottom_coord[i]-top_coord[i]+1))
print segments_to_numpy(param)

print left_coord,right_coord,top_coord,bottom_coord    
for i in range(len(left_coord)):
  roi = img[top_coord[i]:bottom_coord[i],left_coord[i]:right_coord[i]]
  # print roi
  # show(roi)
"""show"""
show(img)
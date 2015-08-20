import numpy
import cv2
import os

def show(img):
    cv2.namedWindow("Image")   
    cv2.imshow("Image", img)   
    cv2.waitKey (0)  

feature_box_width = 20*50
feature_box_height = 20

feature_path = "../feature/"
features = os.listdir(feature_path)
print len(features)

feature_box = numpy.zeros((feature_box_height,feature_box_width), numpy.uint8)
feature_box[:,:] = 255
# show(feature_box)
features.sort(lambda x,y:cmp(x,y)) 
for i in range(50):
        feature_image = cv2.imread(feature_path + features[i])
        feature_image = cv2.cvtColor(feature_image,cv2.COLOR_BGR2GRAY)    
        ret,feature_image = cv2.threshold(feature_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        print features[i]
        feature_box[:20,i*20:i*20+20] = feature_image

show(feature_box)
cv2.imwrite("../features.jpg",feature_box)

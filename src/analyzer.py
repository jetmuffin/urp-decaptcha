# -*- coding: utf-8 -*-

import numpy
import cv2

CHAR_DIC = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','J',\
    'K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','d','e',\
    'f','g','h','j','m','n','q','r','t','w','x','y']

def reconstruct_chars( classes ):
    result_string = "".join(map(lambda x:CHAR_DIC[int(x[0])],classes))
    return result_string

def accuracy( expected, result ):
    if( expected.shape!=result.shape ):
        raise Exception("expected "+str(expected.shape)+", got "+str(result.shape))
    correct= expected==result
    return float(numpy.count_nonzero(correct))/correct.shape[0]

class Analyzer( object ):
    def __init__( self, segmenter, feature_extractor):
        self.segmenter = segmenter
        self.feature_extractor = feature_extractor

    def train( self, image_file ):
        '''训练方法'''

    def analyze( self, image_file ):
        '''预测方法'''

    def display( self ):
        '''显示图片(须先analyze)'''
        if (self.test_image == None):
            raise Exception('The image is not tested')
        cv2.namedWindow("Image")   
        cv2.imshow("Image", self.test_image)   
        cv2.waitKey (0)  

    def display_binary(self):
        cv2.namedWindow("Image")   
        cv2.imshow("Image", self.segmenter.binary)   
        cv2.waitKey (0)  

class KNNAnalyzer( Analyzer ):
    def __init__( self, segmenter, feature_extractor ):
        self.knn = cv2.KNearest()
        self.segmenter = segmenter
        self.feature_extractor = feature_extractor        

    '''使用KNN分类器'''
    def train( self, image_file):
        image = cv2.imread(image_file)
        self.train_image = image
        segments = self.segmenter.process(image)
        features = self.feature_extractor.extract(self.segmenter.binary,segments)

        classes =  numpy.array([i for i in range(50)])
        self.knn.train( features, classes )

    def analyze( self, image_file):
        try:
            image = cv2.imread(image_file)
            self.test_image = image
            segments = self.segmenter.process(self.test_image)
            features = self.feature_extractor.extract(self.segmenter.binary,segments)
         
            retval, result_classes, neigh_resp, dists= self.knn.find_nearest(features, k= 1)
            return reconstruct_chars(result_classes)
        except Exception, e:
            print e
            return None

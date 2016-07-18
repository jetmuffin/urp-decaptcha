# -*- coding: utf-8 -*-

import numpy
import cv2

CHAR_LIST = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZabdefghjmnqrtwxy'


def reconstruct_chars(classes):
    result_string = "".join(map(lambda x: CHAR_LIST[int(x[0])], classes))
    return result_string


def accuracy(expected, result):
    if(expected.shape != result.shape):
        raise Exception("Expected {}, got {}".format(expected.shape, result.shape))
    correct = (expected == result)
    return float(numpy.count_nonzero(correct)) / correct.shape[0]


class Analyzer(object):
    def __init__(self, segmenter, feature_extractor):
        self.segmenter = segmenter
        self.feature_extractor = feature_extractor

    def train(self, image_file):
        '''
        Train method

        '''
        pass

    def analyze(self, image_file):
        '''
        Analyze method

        '''
        pass

    def display(self):
        '''
        Display input image, must be called after analyze

        '''
        if not self.test_image:
            raise Exception("The image has not been tested")
        cv2.namedWindow("Image")
        cv2.imshow("Image", self.test_image)
        cv2.waitKey(0)

    def display_binary(self):
        '''
        Display binary image, must be called after analyze

        '''
        if not self.test_image:
            raise Exception("The image has not been tested")
        cv2.namedWindow("Binary Image")
        cv2.imshow("Binary Image", self.segmenter.binary)
        cv2.waitKey(0)


class KNNAnalyzer(Analyzer):
    def __init__(self, segmenter, feature_extractor):
        Analyzer.__init__(self, segmenter, feature_extractor)
        self.knn = cv2.KNearest()

    def train(self, image_file):
        image = cv2.imread(image_file)
        self.train_image = image
        segments = self.segmenter.process(image)
        features = self.feature_extractor.extract(self.segmenter.binary, segments)

        classes = numpy.array([i for i in range(50)])
        self.knn.train(features, classes)

    def analyze(self, image_file):
        try:
            image = cv2.imread(image_file)
            self.test_image = image
            segments = self.segmenter.process(self.test_image)
            features = self.feature_extractor.extract(self.segmenter.binary, segments)

            return_val, result_classes, neigh_resp, dists = self.knn.find_nearest(features, k=1)
            return reconstruct_chars(result_classes)
        except Exception, e:
            print e
            return None

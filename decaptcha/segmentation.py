# -*- coding: utf-8 -*-

import numpy
import cv2

MAX_SEGMENT_WIDTH = 20
ADHESION_CHAR_WIDTH = [16, 15, 15]
SEGMENT_DATATYPE = numpy.uint16
SEGMENT_SIZE = 4
SEGMENTS_DIRECTION = 0  # vertical axis in numpy


def segments_from_numpy(segments):
    '''
    numpy to tuple

    '''
    segments = segments if SEGMENTS_DIRECTION == 0 else segments.tranpose()
    segments = [map(int, s) for s in segments]
    return segments


def segments_to_numpy(segments):
    '''
    tuple to numpy

    '''

    # each segment in a row
    segments = numpy.array(segments, dtype=SEGMENT_DATATYPE, ndmin=2)
    segments = segments if SEGMENTS_DIRECTION == 0 else numpy.transpose(segments)
    return segments


def region_from_segment(image, segment):
    '''
    crop image to a small region

    '''
    x, y, w, h = segment
    return image[y: y + h, x: x + w]


class BasicSegmenter():
    '''
    Basic Segmenter

    '''
    def _segment(self, image):
        '''
        分割图片，返回(x,y,width, height)元组'''
        pass

    def process(self, image):
        segments = self._segment(image)
        self.image, self.segments = image, segments
        return segments


class NormalSegmenter(BasicSegmenter):

    def _segment(self, image):
        self.image = image
        self.width, self.height = image.shape[:2]

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        image = self.denoise(image)
        image_new = numpy.zeros((self.width + 2, self.height + 2), numpy.uint8)
        image_new[:, :] = 255
        image_new[1:self.width + 1, 1:self.height + 1] = image

        self.binary = image_new
        segments = self.split(image)
        return segments

    def denoise(self, image):
        copy = image.copy()
        directions = [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]]
        for x in range(0, self.width - 1):
            for y in range(0, self.height - 1):
                noise_flag = True
                if(copy[x][y] == 0):
                    for (a, b) in directions:
                        if(copy[x + a][y + b] == 0):
                            noise_flag = False
                            break
                    if(noise_flag):
                        copy[x][y] = 255
        return copy

    def xais_histogram(self, image, left, right):
        x_histogram = [0 for col in range(self.height)]
        for i in range(self.width - 1):
            for j in range(left, right):
                if(image[i, j] == 0):
                    x_histogram[j] += 1
        return x_histogram

    def yais_histogram(self, image, left, right):
        y_histogram = [0 for col in range(self.width)]
        for i in range(self.width - 1):
            for j in range(left, right):
                if(image[i, j] == 0):
                    y_histogram[i] += 1
        return y_histogram

    def adhesion(self, left_coord, right_coord, x_histogram):
        for i in range(len(left_coord)):
            if((right_coord[i] - left_coord[i]) > MAX_SEGMENT_WIDTH):
                three_pix_sum = sum(x_histogram[left_coord[i]: left_coord[i] + 4])
                three_pix_difference = [abs(three_pix_sum - 16), abs(three_pix_sum - 21), abs(three_pix_sum - 30)]
                possible_index = three_pix_difference.index(min(three_pix_difference))
                char_width = ADHESION_CHAR_WIDTH[possible_index]
                left_coord.insert(i + 1, left_coord[i] + char_width)
                right_coord.insert(i, left_coord[i] + char_width - 1)
        return left_coord, right_coord

    def split(self, image):
        x_histogram = self.xais_histogram(image, 0, self.height - 1)
        left_coord = []
        right_coord = []
        for i in range(len(x_histogram) - 1):
            if(x_histogram[i] == 0 and x_histogram[i + 1] > 0):
                left_coord.append(i)
            if(x_histogram[i] > 0 and x_histogram[i + 1] == 0):
                right_coord.append(i + 1)

        left_coord, right_coord = self.adhesion(left_coord, right_coord, x_histogram)

        top_coord = []
        bottom_coord = []
        for c in range(len(left_coord)):
            left, right = left_coord[c], right_coord[c]
            y_histogram = self.yais_histogram(image, left, right)
            for i in range(len(y_histogram) - 1):
                if(y_histogram[i] == 0 and y_histogram[i + 1] > 0):
                    top_coord.append(i)
                    break
            for i in range(len(y_histogram) - 1, 1, -1):
                if(y_histogram[i] == 0 and y_histogram[i - 1] > 0):
                    bottom_coord.append(i + 1)
                    break

        # error
        if(len(left_coord) != len(top_coord) or len(left_coord) < 4):
            raise Exception("验证码分割错误" + str(left_coord))

        param = []
        for i in range(len(left_coord)):
            param.append((left_coord[i], top_coord[i], right_coord[i] - left_coord[i] + 1, bottom_coord[i] - top_coord[i] + 1))
        return segments_to_numpy(param)

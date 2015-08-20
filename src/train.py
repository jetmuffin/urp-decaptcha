import cv2
from segmentation import NormalSegmenter
from feature_extraction import SimpleFeatureExtractor
import traceback

for i in range(100):
  img_path = "../train/" + str(i) + ".jpg"
  image = cv2.imread(img_path)
  print "train image : " + str(i) + '.jpg'
  try:
    segmenter = NormalSegmenter()
    segments = segmenter.process(image)
    print segments
    extractor = SimpleFeatureExtractor( feature_size=20, stretch=False )
    extractor.extract(segmenter.binary,segments)
  except Exception,e:
    print e
    print traceback.format_exc()

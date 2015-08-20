from segmentation import NormalSegmenter
from feature_extraction import SimpleFeatureExtractor
from analyzer import KNNAnalyzer
import random 
import urllib 

def getImage(url, file_path):
    u = urllib.urlopen(url)
    data = u.read()

    f = open(file_path, 'wb')
    f.write(data)
    f.close()


segmenter = NormalSegmenter()
extractor = SimpleFeatureExtractor( feature_size=20, stretch=False )

analyzer = KNNAnalyzer( segmenter, extractor)
analyzer.train('../data/features.jpg')

for i in range(4):
    rand = random.random()
    url = "http://202.119.113.135/validateCodeAction.do?random=" + str(rand);
    print url
    file_path = "../train/crawler.jpg"
    getImage(url,file_path)

    result = analyzer.analyze('../train/crawler.jpg')
    print result
    analyzer.display()
    analyzer.display_binary()

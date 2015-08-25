# CodeAnalyzer
Python application to break captcha of URP（University Resource Plan）System , using OpenCV(2.1)

## How to Use
* Clone the code to your local project by `git clone git@github.com:JetMuffin/CodeAnalyzer.git`
* Import packages into your python program , for example:
```python
  from segmentation import NormalSegmenter
  from feature_extraction import SimpleFeatureExtractor
  from analyzer import KNNAnalyzer
```
* Using existing image to train classification model  
```python
  segmenter = NormalSegmenter()
  extractor = SimpleFeatureExtractor(feature_size=20, stretch=False)
  analyzer = KNNAnalyzer(segmenter, extractor)
  analyzer.train('../data/features.jpg')
```
* Using classification model to test your own images
```python
  result = analyzer.analyze('../tmp/vcode.jpg')
```
## Contribution
Welcome to fork my code and add more segmentation, feature_extraction, or classification to this project.

## Contact
<564936642@qq.com> or <jeffchen328@gmail.com>

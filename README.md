# urp-decaptcha
Python application to break captcha of URP（University Resource Plan）System , using OpenCV(2.1)

[![Build Status](https://api.travis-ci.org/JetMuffin/urp-decaptcha.svg?branch=master)](https://travis-ci.org/JetMuffin/urp-decaptcha)
## Prerequisites

* pip
* python-opencv (see [python-opencv tutorial](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html) for more details)

## How to Use

Clone the code to your local project by 
```
# git clone git@github.com:JetMuffin/urp-decaptcha.git
```

Install dependencies

```
# cd urp-decaptcha
# pip install -r requirements
```

Run

```
# python decaptcha.py <image_to_decaptcha>
```

Complete usage:

```
Usage: decaptcha.py [options]

Options:
  -h, --help            show this help message and exit
  -s SHOW, --show=SHOW  show input image
  -b SHOW_BINARY, --show_binary=SHOW_BINARY
                        show binary image of input
  -t TRAIN_DATA, --train_data=TRAIN_DATA
                        path of train data

```

## How to use this in your code

Use existing image to train classification model  

```python
  segmenter = NormalSegmenter()
  extractor = SimpleFeatureExtractor(feature_size=20, stretch=False)
  analyzer = KNNAnalyzer(segmenter, extractor)
  analyzer.train('data/features.jpg')
```

* Use classification model to test your own images
```python
  result = analyzer.analyze('data/example.jpg')
```

## Contribution
Welcome to fork my code and add more segmentation, feature_extraction, or classification to this project.

## Contact
<564936642@qq.com> or <jeffchen328@gmail.com>

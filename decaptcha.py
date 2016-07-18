from decaptcha.segmentation import NormalSegmenter
from decaptcha.feature_extraction import SimpleFeatureExtractor
from decaptcha.analyzer import KNNAnalyzer
from optparse import OptionParser


analyzer = None


def setup_analyzer(train_data):
    global analyzer
    segmenter = NormalSegmenter()
    extractor = SimpleFeatureExtractor(feature_size=20, stretch=False)
    analyzer = KNNAnalyzer(segmenter, extractor)
    analyzer.train(train_data)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-s', '--show', help='show input image',
                      default=False)
    parser.add_option('-b', '--show_binary', help='show binary image of input',
                      default=False)
    parser.add_option('-t', '--train_data', help='path of train data',
                      default='data/features.jpg')

    options, args = parser.parse_args()
    if len(args) < 1:
        parser.error('Input path required.')
        parser.print_help()

    setup_analyzer(options.train_data)
    result = analyzer.analyze(args[0])
    print result

    if options.show:
        analyzer.display()

    if options.show_binary:
        analyzer.display_binary()

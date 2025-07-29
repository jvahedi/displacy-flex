import unittest
from displacy_flex import DisplaCyFlex

class TestDisplaCyFlex(unittest.TestCase):
    def setUp(self):
        labels = ['ORG', 'LOC', 'PERSON']
        frequencies = [100, 80, 50]
        self.visualizer = DisplaCyFlex(labels, frequencies)

    def test_prepare_labels(self):
        labels = ['ORG', 'LOC']
        frequencies = [10, 20]
        result = self.visualizer._prepare_labels(labels, frequencies)
        self.assertEqual(result, ['Misc', 'LOC', 'ORG'])

    def test_indices(self):
        text = "OpenAI is in San Francisco."
        words = ["OpenAI", "San", "Francisco"]
        indices = self.visualizer.indices(words, text)
        expected = [(0, 6), (13, 16), (17, 26)]
        self.assertEqual(indices, expected)

if __name__ == '__main__':
    unittest.main()
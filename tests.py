import unittest
import sys
import endingDetecter

class Tester(unittest.TestCase):
    def testFrame(self):
        self.assertEqual(endingDetecter.endingDetecter("samples/sample_video1.mp4"), 301)
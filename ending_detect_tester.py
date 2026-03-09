import unittest
import ending_detecter

class TestDetectingEnding(unittest.TestCase):
    
    def setUp(self):
        
        # add your samples to samples/with-outro, add as a key name of video, and value first frame when an outro starts
        self.ending_starts_for_samples = {
            "sample-1.mp4": 740,
            "sample-2.mp4": 491,
            "sample-3.mp4": 391,
            "sample-4.mp4": 289,
            "sample-5.mp4": 462,
            "sample-6.mp4": 573,
            "sample-7.mp4": 862,
            "sample-8.mp4": 300
        }

    def test_check_outro_presence(self):
        failed_samples = []
        succeded_samples = []

        # user set
        frame_tolerace = 10

        for video_sample, frame_outro_starts in self.ending_starts_for_samples.items():
            get_detection = ending_detecter.ending_detect(f"samples/with-outro/{video_sample}")

            if get_detection.get("detected"):
                succeded_samples.append(video_sample)
            else:
                failed_samples.append(video_sample)

            with self.subTest(video_sample):
                self.assertIsInstance(get_detection, dict, "Result is not a dictionary")
                self.assertTrue(get_detection["detected"], f"outro not detected in {video_sample}!")

                # check if returned correct frame is within user's chosen tolerance
                detected_frame = get_detection.get("frames", 0)
                self.assertTrue(
                    frame_outro_starts - frame_tolerace <= detected_frame <= frame_outro_starts + frame_tolerace,
                                f"Frame {detected_frame} is out of tolerance for {video_sample}"
                                )


        print("---RESULTS---")
        print(f"Failed detection in: {failed_samples}, succeded samples: {succeded_samples}")

if __name__ == '__main__':
    unittest.main()
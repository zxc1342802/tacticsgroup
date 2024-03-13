import unittest
from videoProcessor import VideoProcessor, FFMpegException

class TestVideoOperation(unittest.TestCase):
    def setUp(self):
        # 在每个测试用例执行之前设置必要的环境
        self.ffmpeg_exe = "/usr/local/bin/ffmpeg"
        self.video_processor = VideoProcessor.builder(self.ffmpeg_exe)
        self.input_video = "/Users/leijm/ffmpeg/transparent/touming.mov"
        self.output_video = "/Users/leijm/ffmpeg/transparent/beijing.mov"
        self.color = "#0000FF"  # 例如：蓝色

    def test_replace_video_background(self):
        try:
            result = self.video_processor.replace_video_background(self.input_video, self.output_video, self.color)
            self.assertEqual(result.code, 0)
            self.assertIsNotNone(result.out_path)
            # 这里可以添加更多的断言来检查输出路径是否符合预期，以及其他期望的结果
            print(f"result: {result.__dict__}")
        except FFMpegException as e:
            self.fail(f"FFMpegException occurred: {str(e)}")

if __name__ == "__main__":
    unittest.main()
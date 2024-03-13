import unittest
from videoProcessor import VideoProcessor, FFMpegException

class TestVideoProcessor(unittest.TestCase):

    def setUp(self):
        # 在每个测试用例执行之前设置必要的环境
        self.ffmpeg_exe = "/usr/local/bin/ffmpeg"
        self.video_processor = VideoProcessor.builder(self.ffmpeg_exe)

    def test_convert_green_screen_to_transparent(self):
        input_video_path = "/Users/leijm/Documents/VideoTest/touming.avi"
        result = self.video_processor.convert_green_screen_to_transparent(input_video_path)
        self.assertEqual(result.code, 0)
        self.assertIsNotNone(result.out_path)
        # 这里可以添加更多的断言来检查输出路径是否符合预期，以及其他期望的结果
        print(f"result: {result.__dict__}")
    # 可以添加更多的测试用例来测试其他方法
if __name__ == '__main__':
    unittest.main()

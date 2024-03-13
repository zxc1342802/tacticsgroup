import unittest
from videoProcessor import VideoProcessor, FFMpegException

class TestVideoOperation(unittest.TestCase):
    def setUp(self):
        # 在每个测试用例执行之前设置必要的环境
        self.ffmpeg_exe = "/usr/local/bin/ffmpeg"
        self.video_processor = VideoProcessor.builder(self.ffmpeg_exe)

    def test_add_material(self):
        # 输入参数
        input_video = "/Users/leijm/ffmpeg/transparent/beijing_image.mov"
        output_video = "/Users/leijm/ffmpeg/transparent/add_image.mov"
        watermark_image = "/Users/leijm/Documents/VideoTest/logo.png"
        scale_width = 100
        scale_height = 50
        overlay_x = 10
        overlay_y = 20

        # 调用被测试的方法
        result = self.video_processor.add_material(
            input_video, output_video, watermark_image,
            scale_width, scale_height, overlay_x, overlay_y
        )
        print(f"result: {result.__dict__}")


if __name__ == "__main__":
    unittest.main()
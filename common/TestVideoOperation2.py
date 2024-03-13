import unittest
from videoProcessor import VideoProcessor, FFMpegException

class TestVideoOperation(unittest.TestCase):
    def setUp(self):
        # 在每个测试用例执行之前设置必要的环境
        self.ffmpeg_exe = "/usr/local/bin/ffmpeg"
        self.video_processor = VideoProcessor.builder(self.ffmpeg_exe)

    def test_replace_background_image(self):
        try:
              input_video = "/Users/leijm/ffmpeg/temp/download/lei-01.mov"  # 替换为实际的视频路径
              background_image_path = "/Users/leijm/Documents/VideoTest/bj.png"  # 替换为实际的背景图片路径
              
              canvas_width = 1440  # 替换为实际的画布宽度
              canvas_height = 2560  # 替换为实际的画布高度

              overlay_x = 0.4661  # 替换为实际的视频左上角 X 坐标相对画布的比例
              overlay_y = 0.4661  # 替换为实际的视频左上角 Y 坐标相对画布的比例
              scale_width = 884  # 替换为实际的视频宽度
              scale_height = 1351  # 替换为实际的视频高度

              # 执行替换背景操作
              result = self.video_processor.replace_background_image(
                input_video,  background_image_path,
                canvas_width, canvas_height, scale_width, scale_height, overlay_x, overlay_y
              )
              # 这里可以添加更多的断言来检查输出路径是否符合预期，以及其他期望的结果
              print(f"result: {result.__dict__}")
        except FFMpegException as e:
            self.fail(f"FFMpegException occurred: {str(e)}")

if __name__ == "__main__":
    unittest.main()
import unittest
from videoProcessor import VideoProcessor, FFMpegException,LayerInfo

class TestVideoOperation(unittest.TestCase):
    def setUp(self):
        # 在每个测试用例执行之前设置必要的环境
        self.ffmpeg_exe = "/usr/local/bin/ffmpeg"
        self.video_processor = VideoProcessor.builder(self.ffmpeg_exe)

    def test_add_material(self):
        # 输入参数
        input_video = "/Users/leijm/ffmpeg/transparent/beijing_image.mov"
        
        layers = [
            LayerInfo(path="/Users/leijm/Documents/VideoTest/logo.png", scale_width=100, scale_height=100, overlay_x=10, overlay_y=10),
            LayerInfo(path="/Users/leijm/Documents/VideoTest/logo.png", scale_width=200, scale_height=200, overlay_x=20, overlay_y=20),
            LayerInfo(path="/Users/leijm/Documents/VideoTest/logo.png", scale_width=300, scale_height=300, overlay_x=30, overlay_y=30),

            # 添加更多图层信息作为测试数据
        ]


        # 调用被测试的方法
        result = self.video_processor.add_materials(input_video, layers)

        print(f"result: {result.__dict__}")


if __name__ == "__main__":
    unittest.main()
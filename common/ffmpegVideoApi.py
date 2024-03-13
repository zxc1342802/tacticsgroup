import os
from videoProcessor import VideoProcessor, LayerInfo
from typing import Optional, List
import requests

ffmpeg_exe = "/usr/local/bin/ffmpeg"


class VideoAPI:
    def __init__(self):
        self.video_operation = VideoProcessor(ffmpeg_exe)

    def video_editing(self, input_video_url: str, watermark_image_url: str,
                      canvas_width: int, canvas_height: int,
                      scale_width: int, scale_height: int,
                      overlay_x: int, overlay_y: int,
                      layers: List['LayerInfo']) -> str:
        """
        视频编辑函数

        :param input_video: 原始视频的文件路径
        :param watermark_image: 水印图片的文件路径
        :param canvas_width: 画布宽度
        :param canvas_height: 画布高度
        :param scale_width: 水印图片缩放后的宽度
        :param scale_height: 水印图片缩放后的高度
        :param overlay_x: 水印图片在原始视频中的水平叠加位置
        :param overlay_y: 水印图片在原始视频中的垂直叠加位置
        :param layers: 图层信息列表，包含LayerInfo对象的列表
        :return: 最终输出视频的路径
        """
        try:
            if input_video_url and watermark_image_url:
                # # 下载远程视频文件到临时文件夹
                # input_video_path = self.download_file(input_video_url)

                # if input_video_path:
                #     # 下载图片到临时文件夹
                #     watermark_image_path = self.download_file(watermark_image_url)

                # if watermark_image_path:

                # 转换透明背景
                result = self.video_operation.convert_green_screen_to_transparent(input_video_url)
                if result.code != 0 and result.out_path:
                    return f"Error: {result.message}"

                # 替换背景
                result = self.video_operation.replace_background_image(
                    result.out_path, watermark_image_url,
                    canvas_width, canvas_height, scale_width, scale_height, overlay_x, overlay_y
                )
                if result.code != 0 and result.out_path:
                    return f"Error: {result.message}"

                output_video = result.out_path

                # 循环添加图层到输出视频
                if layers:
                    # 添加图层素材到输出视频
                    result = self.video_operation.add_materials(output_video, layers)
                    if result.code != 0:
                        return f"Error: {result.message}"
                    # 更新输出视频路径为临时输出视频路径
                    output_video = result.out_path
                return output_video  # 返回最终输出视频路径
                # else:
                #     return "Error: 合成失败"
            else:
                return "Error: 合成失败"
        except Exception as e:
            return f"Error: {str(e)}"


def download_file(self, file_url: str) -> Optional[str]:
    """
    下载文件到指定路径，并返回文件路径

    :param file_url: 文件的远程URL地址
    :param save_path: 文件保存的本地路径
    :return: 下载成功则返回文件保存的本地路径，否则返回空字符串
    """
    temp_folder_path = os.path.join(os.path.expanduser("~"), "ffmpeg", "temp", "download")
    os.makedirs(temp_folder_path, exist_ok=True)
    file_path = os.path.join(temp_folder_path, self.get_filename_from_url(file_url))
    # 如果文件已经存在，则直接返回本地文件路径
    if os.path.exists(file_path):
        return file_path
    try:
        # 下载文件到指定路径
        response = requests.get(file_url, verify=False)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return file_path
        else:
            print(f'error 下载文件出错 response ：{response}')
            return ""
    except Exception as e:
        print(f'error 下载文件出错：{e}')
        return ""


def get_filename_from_url(self, url: str) -> str:
    """
    从URL中获取文件名

    :param url: 文件的远程URL地址
    :return: 文件名
    """
    return os.path.basename(url)


# 测试代码
if __name__ == "__main__":
    api = VideoAPI()
    input_video_url = "https://oss.zkszr.com/lei-01.avi"
    watermark_image_url = "https://oss.zkszr.com/2e002668f.png"
    canvas_width = 1440  # 替换为实际的画布宽度
    canvas_height = 2560  # 替换为实际的画布高度
    scale_width = 884  # 替换为实际的视频宽度
    scale_height = 1351  # 替换为实际的视频高度
    overlay_x = 0.4
    overlay_y = 0.4
    layers = [
        LayerInfo("https://oss.zkszr.com/2e002668fccc0186d23895a570e94d565c4076a942d1536999f0126f63755a7d.png", 100,
                  100, 0.4, 0.4),
        LayerInfo("https://oss.zkszr.com/2e002668fccc0186d23895a570e94d565c4076a942d1536999f0126f63755a7d.png", 150,
                  150, 0.7, 0.1)
    ]
    output_video = api.video_editing(input_video_url, watermark_image_url,
                                     canvas_width, canvas_height,
                                     scale_width, scale_height,
                                     overlay_x, overlay_y,
                                     layers)

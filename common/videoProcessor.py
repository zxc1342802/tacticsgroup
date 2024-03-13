import os
import subprocess
import logging
import sys
from typing import Optional, List
import time
import re

# 创建日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # 设置日志级别为 INFO


class VideoProcessor:
    def __init__(self, ffmpeg_exe: str):
        # 初始化 VideoOperation 类
        self.ffmpeg_exe = ffmpeg_exe
        # 设置临时文件夹路径
        self.temp_folder_path = os.path.join(os.path.expanduser("~"), "ffmpeg")
        # 设置输出视频文件扩展名
        self.output_video_extension = ".mov"

    @staticmethod
    def builder(ffmpeg_exe: str):
        # 静态方法用于创建 VideoOperation 实例
        return VideoProcessor(ffmpeg_exe)

    def get_video_resolution(self,video_path):

        commands = [self.ffmpeg_exe,"-i",video_path]
        print("执行命令:", " ".join(commands))

        process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if process.returncode == 0:
            # 从输出中查找分辨率信息
            output_str = output.decode()
            matches = re.findall(r'\b(\d+)x(\d+)\b', output_str)

            # 如果找到匹配的分辨率信息，则返回第一个匹配项
            if matches:
                width, height = map(int, matches[0])
                return width, height
            else:
                print("未找到分辨率信息")
                return None, None
        else:
            print("Error:", error.decode().strip())
            return None, None

    # 将绿幕背景转换为透明背景
    def convert_green_screen_to_transparent(self, input_video):
        result = Result()
        try:
            if not input_video:
                # 如果输入视频路径为空，则抛出异常
                raise FFMpegException("请输入视频路径")

            name = os.path.splitext(os.path.basename(input_video))[0]
            # 设置输出视频路径
            output_video = os.path.join(self.temp_folder_path, "temp", name + self.output_video_extension)
            print(f'视频输出路径 output_video：{output_video}')
            if os.path.isfile(output_video):
                # 如果输出视频已存在，则直接返回结果
                result.code = 0
                result.out_path = output_video
                return result

            os.makedirs(os.path.dirname(output_video), exist_ok=True)

            # 调用示例
            width, height = self.get_video_resolution(input_video)
            print("视频分辨率:", width, "x", height)
            commands = [
                self.ffmpeg_exe,
                "-i", input_video,
                "-vf", "chromakey=#00DA00:0.1:0.04",
                "-c:v", "qtrle",
                "-c:a", "copy",
                "-r", "25",  # 保持帧率为 25fps
                "-s", "1440x2560",  # 保持分辨率为 1440x2560
                output_video
            ]

            # 打印执行的命令
            print("执行命令:", " ".join(commands))

            # 执行命令
            process = subprocess.Popen(commands, stderr=subprocess.PIPE)
            result = self.close_stream_quietly(process, result)
            if result.code != 0:
                # 如果命令执行失败，则抛出异常
                raise FFMpegException(result.err_message)

            result.out_path = output_video
            return result

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # 处理异常情况
            raise FFMpegException(str(e))

    # 替换背景颜色
    def replace_video_background(self, input_video, output_video, color):
        result = Result()
        try:
            if not input_video or not output_video or not color:
                raise FFMpegException("请输入视频路径、输出视频路径和背景颜色")
            print(f'视频输出路径 output_video：{output_video}')
            if os.path.isfile(output_video):
                # 如果输出视频已存在，则直接返回结果
                result.code = 0
                result.out_path = output_video
                return result

            os.makedirs(os.path.dirname(output_video), exist_ok=True)

            commands = [
                self.ffmpeg_exe,
                "-i", input_video,
                "-vf",
                f"color=color={color}:size=1440x2560 [bg]; [bg][0:v] overlay=shortest=1",
                output_video
            ]

            print(commands)  # 打印命令，用于调试

            process = subprocess.Popen(commands, stderr=subprocess.PIPE)
            result = self.close_stream_quietly(process, result)
            if result.code != 0:
                raise FFMpegException(result.err_message)
            result.out_path = output_video
            return result

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise FFMpegException(str(e))

    def replace_background_image(self, input_video, background_image_path,
                                 canvas_width, canvas_height, scale_width, scale_height, overlay_x, overlay_y):
        """
        替换视频背景图片

        :param input_video: 原始视频绝对路径
        :param background_image_path: 背景图片路径
        :param canvas_width: 画布宽度
        :param canvas_height: 画布高度
        :param overlay_x: 视频 x 坐标
        :param overlay_y: 视频 y 坐标
        :param scale_width: 视频宽度
        :param scale_height: 视频高度
        :return: 进程返回码
        """
        result = Result()
        try:
            # 检查输入路径是否为空
            if not input_video or not background_image_path:
                raise FFMpegException("请输入视频路径、背景图片路径")

            name = os.path.splitext(os.path.basename(input_video))[0]
            # 设置输出视频路径
            output_video = os.path.join(self.temp_folder_path, "temp", name + "_beijing" + self.output_video_extension)
            print(f'视频输出路径 output_video：{output_video}')

            if os.path.isfile(output_video):
                # 如果输出视频已存在，则直接返回结果
                result.code = 0
                result.out_path = output_video
                return result

            # 创建输出文件夹
            os.makedirs(os.path.dirname(output_video), exist_ok=True)

            commands = [
                self.ffmpeg_exe,
                "-i", input_video,
                "-i", background_image_path,
                "-shortest",
                "-filter_complex",
                "[1:v]scale={canvas_width}x{canvas_height} [bg];" \
                "[0:v]scale={scale_width}x{scale_height}[scaled_video];" \
                "[bg][scaled_video]overlay={overlay_x}:{overlay_y} [out]".format(
                    canvas_width=canvas_width, canvas_height=canvas_height,
                    scale_width=scale_width, scale_height=scale_height,
                    overlay_x=overlay_x * canvas_width, overlay_y=overlay_y * canvas_height
                ),
                "-map", "[out]",
                "-map", "0:a",
                "-c:v", "libx264",
                "-crf", "0",
                "-c:a", "copy",
                output_video
            ]

            print("执行命令:", commands)
            process = subprocess.Popen(commands, stderr=subprocess.PIPE)
            result = self.close_stream_quietly(process, result)
            if result.code != 0:
                raise FFMpegException(result.message)
            result.out_path = output_video
            return result

        except Exception as e:
            raise FFMpegException(str(e))

    def add_material(self, input_video, output_video, watermark_image,
                     scale_width, scale_height, overlay_x, overlay_y):
        # input_video: 原始视频的文件路径。
        # output_video: 输出视频的文件路径。
        # watermark_image: 要叠加到原始视频上的水印图片的文件路径。
        # scale_width: 水印图片缩放后的宽度。
        # scale_height: 水印图片缩放后的高度。
        # overlay_x: 水印图片在原始视频中的水平叠加位置。
        # overlay_y: 水印图片在原始视频中的垂直叠加位置。
        result = Result()
        try:
            # 检查输入参数是否为空
            if not input_video or not output_video or not watermark_image:
                raise FFMpegException("请输入视频路径、输出视频路径和滤镜路径")

            # 创建输出文件夹
            os.makedirs(os.path.dirname(output_video), exist_ok=True)

            # 构建 FFmpeg 命令参数列表
            commands = [
                self.ffmpeg_exe,  # FFmpeg 执行文件路径
                "-i", input_video,  # 输入视频路径
                "-i", watermark_image,  # 水印图片路径
                "-filter_complex",
                # 滤镜链：将水印图片缩放为指定尺寸，并与输入视频叠加
                "[1:v]scale={}:{}[watermark];[0:v][watermark]overlay={}:{}".format(
                    scale_width, scale_height, overlay_x, overlay_y),
                "-c:v",
                "libx264",  # 视频编码器
                "-crf", "0",  # 设置视频质量参数，可根据需要调整
                "-c:a", "copy",  # 不重新编码音频
                output_video  # 输出视频路径
            ]
            print("执行命令:", commands)

            # 使用 subprocess 执行 FFmpeg 命令
            process = subprocess.Popen(commands, stderr=subprocess.PIPE)
            result = self.close_stream_quietly(process, result)
            if result.code != 0:
                raise FFMpegException(result.message)
            result.out_path = output_video
            return result
        except Exception as e:
            print(f"错误信息: {str(e)}")
            # 抛出异常，以便上层处理
            raise FFMpegException(str(e))

    def add_materials(self, input_video: str, layers: List['LayerInfo']) -> str:
        # 添加图层素材到视频
        result = Result()
        temp_output_video_paths = []  # 存储临时输出视频地址列表
        try:
            if not input_video or not layers:
                raise ValueError("请输入视频路径和图层信息")

            for layer in layers:
                output_video = self.generate_temp_output_video_path()
                print(f"临时输出视频路径: {output_video}")
                temp_output_video_paths.append(output_video)

                ret = self.add_material(input_video, output_video, layer.path, layer.scale_width, layer.scale_height,
                                        layer.overlay_x, layer.overlay_y)

                if result.code == 0:
                    input_video = output_video
                    result.code = 0
                    result.out_path = output_video
                else:
                    result.code = 10
                    result.message = "操作失败"
                    break  # 如果添加失败，则直接退出循环
            return result
        except Exception as e:
            print(f"错误信息: {str(e)}")
            raise FFMpegException(str(e))

    def generate_temp_output_video_path(self) -> str:
        """生成临时输出视频文件路径"""
        current_timestamp = int(time.time())
        return os.path.join(self.temp_folder_path, "temp", f"output_{current_timestamp}{self.output_video_extension}")

    @staticmethod
    def close_stream_quietly(proc, result):
        try:
            output = []
            while True:
                line = proc.stderr.readline().decode(sys.stdout.encoding).strip()
                if not line:
                    break
                output.append(line)
                print(line)

            # 等待进程结束
            code = proc.wait()
            # 关闭 stderr 流
            proc.stderr.close()
            result.code = code
            result.message = "ok"
        except Exception as e:
            raise RuntimeError(e)
        return result


class FFMpegException(Exception):
    pass


class Result:
    def __init__(self, code=0, message=None, out_path=None):
        # 初始化 Result 实例
        self.code = code
        self.out_path = out_path
        self.message = message


class LayerInfo:
    def __init__(self, path: str, scale_width: int, scale_height: int, overlay_x: int, overlay_y: int):
        # 初始化图层信息
        self.path = path  # 图层文件路径
        self.scale_width = scale_width  # 缩放宽度
        self.scale_height = scale_height  # 缩放高度
        self.overlay_x = overlay_x  # 叠加在视频上的横坐标位置
        self.overlay_y = overlay_y  # 叠加在视频上的纵坐标位置
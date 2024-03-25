import subprocess
import os
import ffmpeg
import requests
from io import BytesIO
import tempfile
from common.ffmpeg_handler_cmd import VideoProcessor
from datetime import datetime

temp_folder_path = os.path.join(os.getcwd(), "testf_fmpeg")

ffmpeg_exe = "/usr/local/bin/ffmpeg"

video_operation = VideoProcessor(ffmpeg_exe)

folder_path = os.path.join(os.getcwd(), "ffmpeg")
        # 设置输出视频文件扩展名temp
output_video_extension = ".mov"

def get_video_name(video_name):
    # 获取当前时间戳
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_video = os.path.join(folder_path, "temp", video_name + "_" + timestamp + output_video_extension)
    return output_video


def download_gif(url):
    """
    从 URL 下载 GIF 并返回字节流
    """
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        return None

def composite_materials(canvas_width, canvas_height, background_image, layers=[], texts=[], watermarks=[], videos=[], gifs=[], output_file='output.mp4'):
    """
    合成素材函数

    参数:
    - canvas_width: 画布宽度
    - canvas_height: 画布高度
    - background_image: 背景图片路径
    - layers: 图层列表，每个元素是一个字典，包括图层的路径、位置、大小等信息
    - texts: 文本列表，每个元素是一个字典，包括文本内容、位置、大小、字体颜色等信息
    - watermarks: 水印列表，每个元素是一个字符串，表示水印图片路径
    - videos: 视频列表，每个元素是一个字典，包括视频路径、位置、大小等信息
    - gifs: GIF 列表，每个元素是一个字典，包括 GIF 路径、位置、大小等信息
    - output_file: 输出文件路径，默认为'output.mp4'
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 构建背景图片的视频流
    background = ffmpeg.input(background_image).filter('scale', canvas_width, canvas_height)

    # 添加图层
    for layer in layers:
        layer_input = ffmpeg.input(layer['path']).filter('scale', layer['width'], layer['height'])
        background = background.overlay(layer_input, x=layer['x'], y=layer['y'])

    # 添加文本
    for text in texts:
        background = background.drawtext(text['content'], x=text['x'], y=text['y'], fontsize=text['font_size'], fontcolor=text['font_color'])

    # 添加水印
    for watermark in watermarks:
        watermark_input = ffmpeg.input(watermark)
        background = background.overlay(watermark_input, x='main_w-overlay_w-10', y=10)

    # 添加视频
    for video in videos:
        video_input = ffmpeg.input(video['path']).filter('scale', video['width'], video['height'])
        background = background.overlay(video_input, x=video['x'], y=video['y'])
         # 获取原始视频的音频流
        audio_input = ffmpeg.input(video['path']).audio

        # 将原始视频的音频流与背景视频流合并
        background = ffmpeg.concat(background, audio_input, v=1, a=1)
    

    # 添加 GIF
    for gif in gifs:
        gif_bytes = download_gif(gif['path'])
        if gif_bytes:
            gif_file = tempfile.NamedTemporaryFile(delete=False)
            gif_file.write(gif_bytes.read())
            gif_file.close()
            gif_input = ffmpeg.input(gif_file.name).filter('scale', w=gif['width'], h=gif['height'])
            background = background.overlay(gif_input, x=gif['x'], y=gif['y'])


    # 输出设置
    background = background.output(output_file, vcodec='libx264',acodec='aac', crf=23, preset='ultrafast', shortest=None)
    try:
        cmd = ffmpeg.compile(background, overwrite_output=True)
        print("执行ffmpeg命令：", " ".join(cmd))
    except ffmpeg.Error as e:
        print('An error occurred:', e.stderr)
        # 在这里手动构建命令

    # 运行命令
    ffmpeg.run(background, overwrite_output=True)



# 测试代码
if __name__ == "__main__":
    # 背景图片 done
    background_image = 'http://oss.zkszr.com/2e002668f.png'
    # 输入路径 done
    input_video_url = "/Users/leijm/dev/ai/zk-video-generator/common/ffmpeg/temp/94693264e54b38d4582bc5a154cee6da1710899160.mov"
    # 输出路径 done
    output_file = temp_output_video = os.path.join(temp_folder_path, "temp", 'output.mp4')  
    # 水印 done
    watermarks = ['/Users/leijm/dev/ai/zk-video-generator/common/test/shuiyin.png']
    # 文本 done
    texts = [{'content': 'Hello World!', 'x': 10, 'y': 10, 'font_size': 24, 'font_color': 'red'},{'content': 'Hello Worldssssssssss!', 'x': 30, 'y': 30, 'font_size': 24, 'font_color': 'red'}]
    # 图层  done
    layers = [{'path': '/Users/leijm/dev/ai/zk-video-generator/common/test/screenshot-20240322-165143.png',  'x': 375, 'y': 830,'width': 800, 'height': 700},{'path': '/Users/leijm/dev/ai/zk-video-generator/common/test/screenshot-20240322-165142.png',  'x': 75, 'y': 330,'width': 400, 'height': 700}]
    # 动图
    gifs = [{'path': 'http://img.gif.cn/temp_makegif/20240227/1709020827417754.gif', 'x': 100, 'y': 100, 'width': 160, 'height': 250},{'path': 'http://img.gif.cn/temp_makegif/20240227/1709020827417754.gif', 'x': 100, 'y': 100, 'width': 60, 'height': 150}]
    # 视频
    videos = [{'path': input_video_url, 'x': 10, 'y': 10, 'width': 1440, 'height': 2560}]
    
    composite_materials(1440, 2560, background_image,watermarks=watermarks,texts=texts, layers=layers ,gifs=gifs,videos=videos, output_file=output_file)
 
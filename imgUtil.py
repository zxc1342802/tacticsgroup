import os
import time
from io import BytesIO
import requests
import urllib.request
import uuid
import fitz
from aip import AipOcr

# 新建一个AipOcr对象
# appId apiKey secretKey 需要在https://cloud.baidu.com/product/ocr.html免费开通文字识别服务后获取
config = {
    'appId': '49860596',
    'apiKey': 'WNwzkGIiMdsZ1uERG81kUtTR',
    'secretKey': 'VmjTFlSVLlcwa5TrWv5Ft4pNPnjmlrmD'
}
client = AipOcr(**config)




# 读取图片
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


# 识别图片里的文字
def img_to_str(image_path):
    image = get_file_content(image_path)
    # 调用通用文字识别, 图片参数为本地图片
    result = client.basicGeneral(image)
    # 结果拼接返回
    words_list = []
    if 'words_result' in result:
        if len(result['words_result']) > 0:
            for w in result['words_result']:
                words_list.append(w['words'])
            print(words_list)
            file_name = get_code(words_list, 7)
            if file_name == None:
                file_name = 'None' + '-' + str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
            print(file_name)
            os.rename(image_path, pic_dir + str(file_name).replace("/", "") + '.jpg')


# 获取字符串列表中最长的字符串
def get_longest_str(str_list):
    return max(str_list, key=len)

# 获取字符串列表中7位服务编号、11位快速服务代码
def get_code(str_list, length):
    code_num = ''
    for str in str_list:
        if len(str.strip()) == length:
            code_num = str
            return code_num
    return None

# 遍历某个文件夹下所有图片
def query_picture(dir_path):
    pic_path_list = []
    for filename in os.listdir(dir_path):
        pic_path_list.append(dir_path + filename)
    return pic_path_list


def download_file(url, save_directory):
    # 生成随机文件名
    file_extension = os.path.splitext(url)[1]
    file_name = str(uuid.uuid4()) + file_extension
    file_path = os.path.join(save_directory, file_name)

    # 下载文件
    urllib.request.urlretrieve(url, file_path)

    # 获取文件扩展名
    file_extension = os.path.splitext(file_path)[1]

    # 如果是PDF文件，则转换为JPEG格式
    if file_extension.lower() == '.pdf':
        # 生成JPEG文件路径
        jpeg_path = os.path.splitext(file_path)[0] + '.jpg'
        # 转换PDF为图像
        pdf_to_image(file_path, jpeg_path)
        # 删除原始PDF文件
        os.remove(file_path)
        # 更新文件路径为JPEG路径
        file_path = jpeg_path

    return file_path



def pdf_to_image(pdf_path, image_path):
    # 打开PDF文件
    pdf = fitz.open(pdf_path)
    # 获取第一页
    page = pdf[0]
    # 将页面转换为图像
    pix = page.get_pixmap()
    # 保存图像
    pix.save(image_path)
    # 关闭PDF文件
    pdf.close()
if __name__ == '__main__':
    pic_dir = r"/Users/leijm/Documents/tes/"
    save_directory = "/Users/leijm/Documents/tes/"
    pic_urls = [
        "https://files.opayweb.com/uat//opay/ka/merchant/cacFiles/29FCD64FED838762947F2AFB3090AD28/256622011049183.jpeg",
        # 添加更多的图片URL
    ]
    if len(pic_urls) > 0:
        for url in pic_urls:
            downloaded_file_path = download_file(url, save_directory)
            print("Downloaded file:", downloaded_file_path)
    pic_list = query_picture(pic_dir)
    if len(pic_list) > 0:
        for i in pic_list:
            img_to_str(i)
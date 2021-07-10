import os
import random
import string

from app.libs.error_code import FormatErrors


def up_image(img):
    allow_ext = ["jpg", "png"]
    if img.filename.find('.'):
        my_format = img.filename.rsplit('.', 1)[1].strip().lower()
        if my_format[-1] == '"':
            my_format = my_format[:-1]
    else:
        return FormatErrors()
    if my_format not in allow_ext:
        return FormatErrors()
    imgName = get_image_name(my_format)
    # 保存图片
    img.save(get_image_path(imgName))
    # 这个是图片的访问路径，需返回前端（可有可无）
    return imgName


def get_image_path(imgName):
    # 图片path和名称组成图片的保存路径
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    path = basedir + "/static/image/"
    file_path = path + imgName
    file_path = file_path.replace("\\", "/")
    return file_path


def get_image_name(my_format):
    # 图片名称 给图片重命名 为了图片名称的唯一性
    imgName = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    imgName = imgName + "." + my_format
    imgName = imgName.replace('"', "")
    return imgName

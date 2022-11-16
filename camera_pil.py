from io import BytesIO
import cv2
from PIL import ImageGrab, Image
from base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Error')

        while True:
            image = ImageGrab.grab()  # 获取屏幕数据
            # w, h = image.size
            image = image.resize((1366, 750), Image.ANTIALIAS)  # 图片缩放
            output_buffer = BytesIO()  # 建立二进制对象
            image.save(output_buffer, format='JPEG', quality=100)  # quality提高图片分辨率
            frame = output_buffer.getvalue()  # 获取二进制数据
            yield frame  # 生成器返回一张图片的二进制数据

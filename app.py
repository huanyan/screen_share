import os
from importlib import import_module
from flask import Flask, render_template, Response
from gevent import pywsgi
import socket
import sys, signal
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_pil import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """
    视图函数
    :return:
    """
    return render_template('index.html')


def gen(camera):
    """
    流媒体发生器
    """
    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """流媒体数据"""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

res = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
res.connect(("8.8.8.8", 80))

def quit(signum, frame):
    print("正在关闭程序,请耐心等待!")
    sys.exit()

signal.signal(signal.SIGINT, quit)
signal.signal(signal.SIGTERM, quit)

if __name__ == '__main__':
    # app.run(threaded=True, host="0.0.0.0", port=5000)
    print("监控方式,浏览器输入{"+str(res.getsockname()[0])+":5000}")
    server = pywsgi.WSGIServer(('0.0.0.0',5000), app)
    server.serve_forever()
    app.run(threaded=True)
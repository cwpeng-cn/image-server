import json
import tornado.web
import tornado.options
from tornado.options import define, options
from tornado.web import RequestHandler
from tornado import httpserver
import tornado.ioloop
import base64
from tornado import web
import cv2
import os
import numpy as np

PATH = "./images"

define('port', default=10086, help='run port', type=int)


class UploadHandler(RequestHandler):
    def get(self):
        self.write("hello world")

    def post(self):
        print(self.request.body.decode('utf-8'))
        img_list = json.loads(self.request.body.decode('utf-8'))['picture']
        for img in img_list:
            filename = img['filename']
            img_str = img['content']
            path = '{}/{}'.format(PATH, filename)

            img_decode_ = img_str.encode('ascii')
            img_decode = base64.b64decode(img_decode_)
            img_np = np.frombuffer(img_decode, np.uint8)
            img = cv2.imdecode(img_np, cv2.COLOR_RGB2BGR)
            cv2.imwrite(path, img)


class WXHandler(RequestHandler):
    def get(self):
        self.write("hello world")

    def post(self):
        img_list = self.request.files['file']
        for img in img_list:
            filename = img['filename']
            img_str = img['body']
            path = '{}/{}'.format(PATH, filename)
            img_np = np.frombuffer(img_str, np.uint8)
            img = cv2.imdecode(img_np, cv2.COLOR_RGB2BGR)
            cv2.imwrite(path, img)

        with open('hah.jpg', 'rb') as f:
            img_byte = base64.b64encode(f.read())
        self.write(img_byte)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/upload', UploadHandler), (r'/wx', WXHandler)]
        super(Application, self).__init__(handlers)


app = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    print('监听端口: ', options.port)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

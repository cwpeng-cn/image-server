import json
import tornado.web
import tornado.options
from tornado.options import define, options
from tornado.web import RequestHandler
import tornado.httpserver
import tornado.ioloop
import base64
import cv2
import numpy as np

PATH = "./images"

define('port', default=80, help='run port', type=int)


class UploadHandler(RequestHandler):
    def get(self):
        self.write("hello world")

    def post(self):
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


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/upload', UploadHandler)]
        super(Application, self).__init__(handlers)


app = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    print('监听端口: ', options.port)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

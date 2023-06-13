import json
from channels.generic.websocket import WebsocketConsumer
# Create your views here.


class Message(WebsocketConsumer):
    # websocket建立连接时执行方法
    def connect(self):
        self.accept()

    # websocket断开时执行方法
    def disconnect(self, close_code):
        self.close()

    # 从websocket接收到消息时执行函数
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.send(text_data=json.dumps({"message": message}))

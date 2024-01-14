import json
from channels.generic.websocket import WebsocketConsumer


# View for consumer to accept websocket connections
# and echo messages it receives from the websocket back to it.
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # accept connection (you reject any connection with self.close())
        self.accept()

    def disconnect(self, close_code):
        pass  # No need to implement any action when a client closes a connection

    def receive(self, text_data=None, bytes_data=None):
        # receive message from WebSocket, you treat the text_data as JSON
        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # send message to WebSocket
            self.send(text_data=json.dumps({'message': message}))

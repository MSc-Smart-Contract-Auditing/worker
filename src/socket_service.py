from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from src.models.requests import Status


class SocketService:

    __active = None
    __incoming_id = None

    @staticmethod
    async def send(message: Status):
        if Socket.__active:
            await Socket.__active.__send(message)

    @staticmethod
    def register_incoming_id(socket_id: str):
        Socket.__incoming_id = socket_id

    @staticmethod
    async def close():
        if Socket.__active:
            await Socket.__active.__close()
            Socket.__active = None
            Socket.__incoming_id = None

    @staticmethod
    def __validate_id(socket_id: str):
        if Socket.__incoming_id == socket_id:
            return
        raise WebSocketException("Invalid Socket ID")

    def __init__(self, websocket: WebSocket, socket_id: str):
        Socket.__validate_id(socket_id)

        self.websocket = websocket
        self.id = socket_id
        Socket.__active = self

    async def __aenter__(self):
        await self.websocket.accept()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.__close()

    async def __close(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

    async def listen(self):
        while True:
            try:
                data = await self.websocket.receive_text()
                print(f"Received message: {data}")
            except WebSocketDisconnect:
                print(f"Socket {self.id} disconnected")
                break

    async def __send(self, message: Status):
        await self.websocket.send_json(message)

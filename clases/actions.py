from socket import socket
from clases.room import Room
class Actions:
    def __init__(self) -> None:
        pass
    def deleteUser(self, ws_client:socket, room:Room):
        del room.users[ws_client]
    def addUser(self, ws_client:socket, name:str, room:Room):
        print('Dentro del addUser')
        room.users[ws_client] = name
    def sizeRoom(self, room:Room):
        return len(room.users)
    async def send_msg(self, ws: socket, msg:str):
        await ws.send(msg)
    def getUsers(self, room:Room):
        return room.users
import socket
from typing import final
import websockets
from websockets import exceptions
import asyncio
from clases.actions import Actions
from clases.room import Room
import json
# Creando la sala de chat para añadir los usuarios
room_chat = Room()
# Creando las acciones dentro del chat
actions_chat = Actions()


# Estilo de una respuesta enviada a los clientes {state: 'new_client', }

async def handlerConn(websocket, path):
    '''Funcion que se ejecutará cada vez que se conecte un cliente'''
    await websocket.send('Escribe tu nombre: ')
    try:
        name = await websocket.recv()
        await notify_new_client(websocket, room_chat, actions_chat)
        actions_chat.addUser(websocket, name, room_chat)
        await websocket.send(f'Bienvenido al servidor {name}')
        await send_msg(name, websocket, actions_chat, room_chat)
    except exceptions.ConnectionClosedOK:
        actions_chat.deleteUser(websocket, room_chat)
    finally:
        # Cuando el cliente cierra la conexion puedo eliminarlo de la sala con la siguiente linea
        actions_chat.deleteUser(websocket, room_chat)
        await notify_logout_client(name, websocket, room_chat, actions_chat)


async def notify_new_client(ws: socket.socket, room: Room, actions: Actions):
    for x in actions.getUsers(room):
        await x.send('Nuevo cliente conectado')
async def notify_logout_client(name:str, ws:socket.socket, room:Room, actions: Actions):
    sizeRoom= actions.sizeRoom(room)
    if sizeRoom >=1:
        response = json.dumps({'status':'logout', 'data':{'user':name,'size':sizeRoom}})
        for x in actions_chat.getUsers(room):
            await x.send(response)

async def send_msg(name: str, ws: socket.socket, actions: Actions, room: Room):
    # response = json.dumps({'status':'msg', 'data':msg})
    # await ws.send(response)
    async for msg in ws:
        response = json.dumps(
            {'status': 'new_msg', 'data': {'user': name, 'msg': msg}})
        if actions.sizeRoom(room) > 1:
            for x in actions.getUsers(room):
                await x.send(response)


async def main():
    async with websockets.serve(handlerConn, "localhost", 7777):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())

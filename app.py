import websockets
from websockets import exceptions
import asyncio
from clases.actions import Actions
from clases.room import Room
# Creando la sala de chat para añadir los usuarios
room_chat = Room()
# Creando las acciones dentro del chat
actions_chat = Actions()


async def handlerConn(websocket, path):
    '''Funcion que se ejecutará cada vez que se conecte un cliente'''

    name = await websocket.recv()
    print(f"<<< {name}")
    actions_chat.addUser(websocket,name, room_chat)
    greeting = f'Bienvenido al servidor {name}'
    await websocket.send(f'Bienvenido al servidor {name}. Conexiones totales {actions_chat.sizeRoom(room_chat)}')
    print(f">>> {greeting}")
    async for msg in websocket: 
        print('Dentro del async for')
        if actions_chat.sizeRoom(room_chat)>1:
            for x in actions_chat.getUsers(room_chat):
                print('ITERANDO')
                try:
                    await x.send(msg)
                except exceptions.ConnectionClosedOK:
                    actions_chat.deleteUser(x,room_chat)
    print('DESPUES DEL ASYNC FOR')
                


async def main():
    async with websockets.serve(handlerConn, "localhost", 7777):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())

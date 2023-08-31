import asyncio
from websockets.server import serve

import asyncio
import itertools
import json

import websockets

PLAYERS = []

async def handler(websocket):
    # Initialize a game.
    # game = Game()

    async for message in websocket:
        await websocket.send(message)
        print(f"Received: {message}")
        try:
            event = json.loads(message)
            PLAYERS.append(event['presence'])
            print(PLAYERS)
            if len(PLAYERS) != 2:
                print('awaiting another player...')
            elif len(PLAYERS) == 2:
                print('starting GAME!')
                for i in PLAYERS:
                    print(f'player name - {i}')

        except:
            pass


async def main():
    async with websockets.serve(handler, "localhost", 8001):
        await asyncio.Future()  # run forever


asyncio.run(main())

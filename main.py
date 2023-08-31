import datetime
import json

import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

import threading
import asyncio
import pygame
import websockets
import asyncio

from websockets.sync.client import connect


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

        self.player_name = str(datetime.datetime.now())
        self.presence()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            if event.type == pg.MOUSEBUTTONDOWN:
                self.player.single_fire_event(event)
                with connect("ws://localhost:8001") as websocket:
                    websocket.send(f"Player {self.player_name} press LMB -> single fire event activated!")
                    message = websocket.recv()
                    print(f"Received: {message}")

    # new
    def data_for_server(self):
        with connect("ws://localhost:8001") as websocket:
            data = {
                'player_name': self.player_name,
                'status': self.player.health,
                'position': self.player.pos
            }
            websocket.send(json.dumps(data))
            message = websocket.recv()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

            self.data_for_server()

    def presence(self):
        with connect("ws://localhost:8001") as websocket:
            data = {'presence': self.player_name}
            websocket.send(json.dumps(data))
            message = websocket.recv()
            print(f"Received: {message}")


if __name__ == '__main__':
    game = Game()
    game.run()

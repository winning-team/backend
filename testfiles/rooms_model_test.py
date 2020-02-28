from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

from queue import Queue
import random
import time


class Room():
    def __init__(self, room_number, i, j):
        self.id = models.IntegerField(default=room_number)
        self.i = models.IntegerField(default=i)
        self.j = models.IntegerField(default=i)
        self.n_to = models.IntegerField(null=True)
        self.s_to = models.IntegerField(null=True)
        self.e_to = models.IntegerField(null=True)
        self.w_to = models.IntegerField(null=True)

    def __repr__(self):
        return f'{self.id}'.rjust(4)


class World():
    def __init__(self):
        starter_room = Room(1, 0, 0)
        self.map = [[starter_room]]
        self.rooms = {1: starter_room}
        self.total_rooms = 1

    def __len__(self):
        return self.total_rooms

    def can_add_room(self, room_id, direction):
        room = self.rooms[room_id]
        i, j = room.i, room.j
        if direction == 'n':
            return not (((i-1 >= 0) and self.map[i-1][j]) or room.n_to)
        elif direction == 's':
            return not (((i+1 < len(self.map)) and self.map[i+1][j]) or room.s_to)
        elif direction == 'e':
            return not (((j+1 < len(self.map[i])) and self.map[i][j+1]) or room.e_to)
        elif direction == 'w':
            return not (((j-1 >= 0) and self.map[i][j-1]) or room.w_to)

    def possible_room_directions(self, room_id):
        return [dir for dir in ['n', 's', 'e', 'w'] if self.can_add_room(room_id, dir)]

    def add_n(self, room_id):
        i, j = self.rooms[room_id].i, self.rooms[room_id].j
        if i-1 < 0:
            self.map.insert(0, [None] * len(self.map[0]))
            for room in self.rooms:
                self.rooms[room].i += 1
            i += 1
        self.total_rooms += 1
        room = Room(self.total_rooms, i-1, j)
        self.map[i-1][j] = room
        self.rooms[self.total_rooms] = room
        self.rooms[room_id].n_to = room.id
        room.s_to = room_id
        return True

    def add_s(self, room_id):
        i, j = self.rooms[room_id].i, self.rooms[room_id].j
        if i + 1 >= len(self.map):
            self.map.append([None] * len(self.map[0]))
        self.total_rooms += 1
        room = Room(self.total_rooms, i+1, j)
        self.map[i+1][j] = room
        self.rooms[self.total_rooms] = room
        self.rooms[room_id].s_to = room.id
        room.n_to = room_id
        return True

    def add_e(self, room_id):
        i, j = self.rooms[room_id].i, self.rooms[room_id].j
        if j + 1 >= len(self.map[i]):
            for row in self.map:
                row.append(None)
        self.total_rooms += 1
        room = Room(self.total_rooms, i, j+1)
        self.map[i][j+1] = room
        self.rooms[self.total_rooms] = room
        self.rooms[room_id].e_to = room.id
        room.w_to = room_id
        return True

    def add_w(self, room_id):
        i, j = self.rooms[room_id].i, self.rooms[room_id].j
        if j-1 < 0:
            for row in self.map:
                row.insert(0, None)
            for room in self.rooms:
                self.rooms[room].j += 1
            j += 1
        self.total_rooms += 1
        room = Room(self.total_rooms, i, j-1)
        self.map[i][j-1] = room
        self.rooms[self.total_rooms] = room
        self.rooms[room_id].w_to = room.id
        room.e_to = room_id
        return True

    def print_map(self):
        for row in self.map:
            print(row)

    def print_rooms(self):
        for room in self.rooms:
            print(
                f'Room {self.rooms[room].id} ({self.rooms[room].i},{self.rooms[room].j})' +
                f' n: {self.rooms[room].n_to}' +
                f' s: {self.rooms[room].s_to}' +
                f' e: {self.rooms[room].e_to}' +
                f' w: {self.rooms[room].w_to}' +
                f' possible: {self.possible_room_directions(room)}'
            )

    def add_rooms(self, number):
        max = self.total_rooms + number
        room_queue = Queue()
        room_queue.enqueue(self.total_rooms)
        while self.total_rooms < max:
            room_id = room_queue.dequeue()
            if not room_id:
                for room in self.rooms:
                    if len(self.possible_room_directions(room)) > 1:
                        room_id = self.rooms[room].id
            possible = self.possible_room_directions(room_id)
            if len(possible):
                for i in range(random.randint(1, len(possible))):
                    dir = possible.pop(random.randint(0, len(possible) - 1))
                    if (
                        dir == 'n' and self.add_n(room_id) or
                        dir == 's' and self.add_s(room_id) or
                        dir == 'e' and self.add_e(room_id) or
                        dir == 'w' and self.add_w(room_id)
                    ):
                        room_queue.enqueue(self.total_rooms)


start_time = time.time()
world = World()

world.add_rooms(10000)
world.print_map()

print(len(world))
end_time = time.time()
print(f"runtime: {end_time - start_time} seconds")

from adventure.models import Player, Room, World
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from util.queue import Queue
import random
import time
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            Room.objects.all().delete()

            # class CreateRoom():
            #     def __init__(self, room_number, i, j):
            #         self.id = room_number
            #         self.i = i
            #         self.j = j
            #         self.n_to = 0
            #         self.s_to = 0
            #         self.e_to = 0
            #         self.w_to = 0

            # def __repr__(self):
            #     if self.n_to and self.e_to and self.s_to and self.w_to:
            #         return '1'.rjust(4)
            #     elif self.n_to and self.e_to and self.s_to:
            #         return '2'.rjust(4)
            #     elif self.n_to and self.e_to and self.w_to:
            #         return '3'.rjust(4)
            #     elif self.n_to and self.s_to and self.w_to:
            #         return '4'.rjust(4)
            #     elif self.e_to and self.s_to and self.w_to:
            #         return '5'.rjust(4)
            #     elif self.n_to and self.e_to:
            #         return '6'.rjust(4)
            #     elif self.n_to and self.s_to:
            #         return '7'.rjust(4)
            #     elif self.n_to and self.w_to:
            #         return '8'.rjust(4)
            #     elif self.e_to and self.s_to:
            #         return '9'.rjust(4)
            #     elif self.e_to and self.w_to:
            #         return '10'.rjust(4)
            #     elif self.s_to and self.w_to:
            #         return '11'.rjust(4)
            #     elif self.n_to:
            #         return '12'.rjust(4)
            #     elif self.e_to:
            #         return '13'.rjust(4)
            #     elif self.s_to:
            #         return '14'.rjust(4)
            #     elif self.w_to:
            #         return '15'.rjust(4)

            # class CreateWorld():
            #     def __init__(self):
            #         starter_room = CreateRoom(1, 0, 0)
            #         self.map = [[starter_room]]
            #         self.rooms = {1: starter_room}
            #         self.total_rooms = 1

            #     def __len__(self):
            #         return self.total_rooms

            #     def can_add_room(self, room_id, direction):
            #         room = self.rooms[room_id]
            #         i, j = room.i, room.j
            #         if direction == 'n':
            #             return not (((i-1 >= 0) and self.map[i-1][j]) or room.n_to)
            #         elif direction == 's':
            #             return not (((i+1 < len(self.map)) and self.map[i+1][j]) or room.s_to)
            #         elif direction == 'e':
            #             return not (((j+1 < len(self.map[i])) and self.map[i][j+1]) or room.e_to)
            #         elif direction == 'w':
            #             return not (((j-1 >= 0) and self.map[i][j-1]) or room.w_to)

            #     def possible_room_directions(self, room_id):
            #         return [dir for dir in ['n', 's', 'e', 'w'] if self.can_add_room(room_id, dir)]

            #     def add_n(self, room_id):
            #         i, j = self.rooms[room_id].i, self.rooms[room_id].j
            #         if i-1 < 0:
            #             self.map.insert(0, [None] * len(self.map[0]))
            #             for room in self.rooms:
            #                 self.rooms[room].i += 1
            #             i += 1
            #         self.total_rooms += 1
            #         room = CreateRoom(self.total_rooms, i-1, j)
            #         self.map[i-1][j] = room
            #         self.rooms[self.total_rooms] = room
            #         self.rooms[room_id].n_to = room.id
            #         room.s_to = room_id
            #         return True

            #     def add_s(self, room_id):
            #         i, j = self.rooms[room_id].i, self.rooms[room_id].j
            #         if i + 1 >= len(self.map):
            #             self.map.append([None] * len(self.map[0]))
            #         self.total_rooms += 1
            #         room = CreateRoom(self.total_rooms, i+1, j)
            #         self.map[i+1][j] = room
            #         self.rooms[self.total_rooms] = room
            #         self.rooms[room_id].s_to = room.id
            #         room.n_to = room_id
            #         return True

            #     def add_e(self, room_id):
            #         i, j = self.rooms[room_id].i, self.rooms[room_id].j
            #         if j + 1 >= len(self.map[i]):
            #             for row in self.map:
            #                 row.append(None)
            #         self.total_rooms += 1
            #         room = CreateRoom(self.total_rooms, i, j+1)
            #         self.map[i][j+1] = room
            #         self.rooms[self.total_rooms] = room
            #         self.rooms[room_id].e_to = room.id
            #         room.w_to = room_id
            #         return True

            #     def add_w(self, room_id):
            #         i, j = self.rooms[room_id].i, self.rooms[room_id].j
            #         if j-1 < 0:
            #             for row in self.map:
            #                 row.insert(0, None)
            #             for room in self.rooms:
            #                 self.rooms[room].j += 1
            #             j += 1
            #         self.total_rooms += 1
            #         room = CreateRoom(self.total_rooms, i, j-1)
            #         self.map[i][j-1] = room
            #         self.rooms[self.total_rooms] = room
            #         self.rooms[room_id].w_to = room.id
            #         room.e_to = room_id
            #         return True

            #     def print_map(self):
            #         # print(str(self.map))
            #         for row in self.map:
            #             print(row)

            #     def print_rooms(self):
            #         for room in self.rooms:
            #             print(
            #                 f'Room {self.rooms[room].id} ({self.rooms[room].i},{self.rooms[room].j})' +
            #                 f' n: {self.rooms[room].n_to}' +
            #                 f' s: {self.rooms[room].s_to}' +
            #                 f' e: {self.rooms[room].e_to}' +
            #                 f' w: {self.rooms[room].w_to}' +
            #                 f' possible: {self.possible_room_directions(room)}'
            #             )

            #     def add_rooms(self, number):
            #         max = self.total_rooms + number
            #         room_queue = Queue()
            #         room_queue.enqueue(self.total_rooms)
            #         while self.total_rooms < max:
            #             room_id = room_queue.dequeue()
            #             if not room_id:
            #                 for room in self.rooms:
            #                     if len(self.possible_room_directions(room)) > 1:
            #                         room_id = self.rooms[room].id
            #             possible = self.possible_room_directions(room_id)
            #             if len(possible):
            #                 for i in range(random.randint(1, len(possible))):
            #                     dir = possible.pop(
            #                         random.randint(0, len(possible) - 1))
            #                     if (
            #                         dir == 'n' and self.add_n(room_id) or
            #                         dir == 's' and self.add_s(room_id) or
            #                         dir == 'e' and self.add_e(room_id) or
            #                         dir == 'w' and self.add_w(room_id)
            #                     ):
            #                         room_queue.enqueue(self.total_rooms)
            class CreateRoom():
                def __init__(self, room_number, i, j):
                    self.id = room_number
                    self.y = i
                    self.x = j
                    self.n_to = None
                    self.s_to = None
                    self.e_to = None
                    self.w_to = None

                def __repr__(self):
                    if self.n_to and self.e_to and self.s_to and self.w_to:
                        return 'nesw'.rjust(4)
                    elif self.n_to and self.e_to and self.s_to:
                        return 'nes'.rjust(4)
                    elif self.n_to and self.e_to and self.w_to:
                        return 'new'.rjust(4)
                    elif self.n_to and self.s_to and self.w_to:
                        return 'nsw'.rjust(4)
                    elif self.e_to and self.s_to and self.w_to:
                        return 'esw'.rjust(4)
                    elif self.n_to and self.e_to:
                        return 'ne'.rjust(4)
                    elif self.n_to and self.s_to:
                        return 'ns'.rjust(4)
                    elif self.n_to and self.w_to:
                        return 'nw'.rjust(4)
                    elif self.e_to and self.s_to:
                        return 'es'.rjust(4)
                    elif self.e_to and self.w_to:
                        return 'ew'.rjust(4)
                    elif self.s_to and self.w_to:
                        return 'sw'.rjust(4)
                    elif self.n_to:
                        return 'n'.rjust(4)
                    elif self.e_to:
                        return 'e'.rjust(4)
                    elif self.s_to:
                        return 's'.rjust(4)
                    elif self.w_to:
                        return 'w'.rjust(4)

            class CreateWorld():
                def __init__(self):
                    starter_room = CreateRoom(1, 0, 0)
                    self.map = [[starter_room]]
                    self.rooms = {1: starter_room}
                    self.total_rooms = 1

                def __len__(self):
                    return self.total_rooms

                def can_add_room(self, room_id, direction):
                    room = self.rooms[room_id]
                    i, j = room.y, room.x
                    if direction == 's':
                        return not (((i-1 >= 0) and self.map[i-1][j]) or room.s_to)
                    elif direction == 'n':
                        return not (((i+1 < len(self.map)) and self.map[i+1][j]) or room.n_to)
                    elif direction == 'e':
                        return not (((j+1 < len(self.map[i])) and self.map[i][j+1]) or room.e_to)
                    elif direction == 'w':
                        return not (((j-1 >= 0) and self.map[i][j-1]) or room.w_to)

                def possible_room_directions(self, room_id):
                    return [dir for dir in ['n', 's', 'e', 'w'] if self.can_add_room(room_id, dir)]

                def add_s(self, room_id):
                    i, j = self.rooms[room_id].y, self.rooms[room_id].x
                    if i-1 < 0:
                        self.map.insert(0, [None] * len(self.map[0]))
                        for room in self.rooms:
                            self.rooms[room].y += 1
                        i += 1
                    self.total_rooms += 1
                    room = CreateRoom(self.total_rooms, i-1, j)
                    self.map[i-1][j] = room
                    self.rooms[self.total_rooms] = room
                    self.rooms[room_id].s_to = room.id
                    room.n_to = room_id
                    return True

                def add_n(self, room_id):
                    i, j = self.rooms[room_id].y, self.rooms[room_id].x
                    if i + 1 >= len(self.map):
                        self.map.append([None] * len(self.map[0]))
                    self.total_rooms += 1
                    room = CreateRoom(self.total_rooms, i+1, j)
                    self.map[i+1][j] = room
                    self.rooms[self.total_rooms] = room
                    self.rooms[room_id].n_to = room.id
                    room.s_to = room_id
                    return True

                def add_e(self, room_id):
                    i, j = self.rooms[room_id].y, self.rooms[room_id].x
                    if j + 1 >= len(self.map[i]):
                        for row in self.map:
                            row.append(None)
                    self.total_rooms += 1
                    room = CreateRoom(self.total_rooms, i, j+1)
                    self.map[i][j+1] = room
                    self.rooms[self.total_rooms] = room
                    self.rooms[room_id].e_to = room.id
                    room.w_to = room_id
                    return True

                def add_w(self, room_id):
                    i, j = self.rooms[room_id].y, self.rooms[room_id].x
                    if j-1 < 0:
                        for row in self.map:
                            row.insert(0, None)
                        for room in self.rooms:
                            self.rooms[room].x += 1
                        j += 1
                    self.total_rooms += 1
                    room = CreateRoom(self.total_rooms, i, j-1)
                    self.map[i][j-1] = room
                    self.rooms[self.total_rooms] = room
                    self.rooms[room_id].w_to = room.id
                    room.e_to = room_id
                    return True

                def print_map(self):
                    for i in range(len(self.map)-1, -1, -1):
                        print(self.map[i])

                def map_to_str(self):
                    pass

                def print_rooms(self):
                    for room in self.rooms:
                        print(
                            f'Room {self.rooms[room].id} ({self.rooms[room].x},{self.rooms[room].y})' +
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
                                dir = possible.pop(
                                    random.randint(0, len(possible) - 1))
                                if (
                                    dir == 'n' and self.add_n(room_id) or
                                    dir == 's' and self.add_s(room_id) or
                                    dir == 'e' and self.add_e(room_id) or
                                    dir == 'w' and self.add_w(room_id)
                                ):
                                    room_queue.enqueue(self.total_rooms)

            start_time = time.time()
            world = CreateWorld()
            world.add_rooms(100)
            rooms = {}
            for i in range(1, world.total_rooms + 1):
                rooms[i] = Room(
                    title=str(i), description=f'Room {i}', x=world.rooms[i].x, y=world.rooms[i].y)
                rooms[i].save()

            for i in range(1, world.total_rooms + 1):
                if world.rooms[i].n_to:
                    rooms[i].n_to = rooms[world.rooms[i].n_to].id
                if world.rooms[i].s_to:
                    rooms[i].s_to = rooms[world.rooms[i].s_to].id
                if world.rooms[i].e_to:
                    rooms[i].e_to = rooms[world.rooms[i].e_to].id
                if world.rooms[i].w_to:
                    rooms[i].w_to = rooms[world.rooms[i].w_to].id
                rooms[i].save()

            players = Player.objects.all()
            for p in players:
                p.currentRoom = rooms[1].id
                p.save()

            r = world.rooms

            n_to = list(filter(lambda x: r[x].n_to, r))
            e_to = list(filter(lambda x: r[x].e_to, r))
            connections = list(
                map(lambda x: [{'x': r[x].x, 'y': r[x].y}, {'x': r[r[x].n_to].x, 'y': r[r[x].n_to].y}], n_to)) + list(
                map(lambda x: [{'x': r[x].x, 'y': r[x].y}, {'x': r[r[x].e_to].x, 'y': r[r[x].e_to].y}], e_to))
            print(connections)

            world.print_map()

            world1 = World()
            world1.map = json.dumps(connections)
            world1.save()

            print(len(world))
            end_time = time.time()
            print(f"runtime: {end_time - start_time} seconds")
        except Exception as e:
            raise CommandError(e)

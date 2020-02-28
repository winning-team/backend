from queue import Queue
import random


class Room():
    def __init__(self, room_number, i, j):
        self.id = room_number
        self.i = i
        self.j = j
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None

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
        i = room.i
        j = room.j

        if direction == 'n':
            if ((i-1 >= 0) and self.map[i-1][j]) or room.n_to:
                return False
        elif direction == 's':
            if ((i+1 < len(self.map)) and self.map[i+1][j]) or room.s_to:
                return False
        elif direction == 'e':
            if ((j+1 < len(self.map[i])) and self.map[i][j+1]) or room.e_to:
                return False
        elif direction == 'w':
            if ((j-1 >= 0) and self.map[i][j-1]) or room.w_to:
                return False
        return True

    def possible_room_directions(self, room_id):
        directions = []
        if self.can_add_room(room_id, 'n'):
            directions.append('n')
        if self.can_add_room(room_id, 's'):
            directions.append('s')
        if self.can_add_room(room_id, 'e'):
            directions.append('e')
        if self.can_add_room(room_id, 'w'):
            directions.append('w')
        return directions

    def add_n(self, room_id):
        i = self.rooms[room_id].i
        j = self.rooms[room_id].j
        try:
            if i-1 < 0:
                raise Exception('North row does not exist!')
        except:
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

    def add_s(self, room_id):
        i = self.rooms[room_id].i
        j = self.rooms[room_id].j
        try:
            if i + 1 >= len(self.map):
                raise Exception('South row does not exist!')
        except:
            self.map.append([None] * len(self.map[0]))
        self.total_rooms += 1
        room = Room(self.total_rooms, i+1, j)
        self.map[i+1][j] = room
        self.rooms[self.total_rooms] = room
        self.rooms[room_id].s_to = room.id
        room.n_to = room_id

    def add_e(self, room_id):
        i = self.rooms[room_id].i
        j = self.rooms[room_id].j
        try:
            if j + 1 >= len(self.map[i]):
                raise Exception('East column does not exist!')
        except:
            for row in self.map:
                row.append(None)
        self.total_rooms += 1
        room = Room(self.total_rooms, i, j+1)
        self.map[i][j+1] = room
        self.rooms[self.total_rooms] = room
        self.rooms[room_id].e_to = room.id
        room.w_to = room_id

    def add_w(self, room_id):
        i = self.rooms[room_id].i
        j = self.rooms[room_id].j
        try:
            if j-1 < 0:
                raise Exception('West column does not exist!')
        except:
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

    def print(self):
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
            possible = self.possible_room_directions(room_id).copy()
            if len(possible):
                for i in range(random.randint(1, len(possible))):
                    dir = possible.pop(random.randint(0, len(possible) - 1))
                    if dir == 'n':
                        if self.add_n(room_id):
                            room_queue.enqueue(self.total_rooms)
                    elif dir == 's':
                        if self.add_s(room_id):
                            room_queue.enqueue(self.total_rooms)
                    elif dir == 'e':
                        if self.add_e(room_id):
                            room_queue.enqueue(self.total_rooms)
                    elif dir == 'w':
                        if self.add_w(room_id):
                            room_queue.enqueue(self.total_rooms)


world = World()

world.add_rooms(500)

world.print()
print(len(world))
# world.print_rooms()


# need to change all room coordinates if adding row/column to north or east

# e = j+1, j

# when adding rooms n, s, e, w of current room their coordinates will be
# n = i-1, j
# s = i+1, j,
# e = i, j-1
# w = i, j+1

# if north and doesnt exist, world.insert(0, [0] * len(world[0]))
# update all room coords i+1, j

# if east and doesnt exist:
# for i in range(len(world)):
#   world[i].append(0)

# if south and doesnt exist, world.append([0] * len(world[0]))

# if west and doesnt exist:
# for i in range(len(world)):
#   world[i].insert(0, 0)
# update all room coords i, j+1

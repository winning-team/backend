import random


class Room():
    def __init__(self, room_number, i, j):
        self.id = room_number
        self.i = i
        self.j = j

    def __repr__(self):
        return f'{self.i},{self.j}'


class World():
    def __init__(self):
        self.map = [[1]]
        self.total_rooms = 1

    def add_n(self, i, j):
        try:
            if i-1 < 0:
                raise Exception('North row does not exist!')
        except:
            self.map.insert(0, [0] * len(self.map[0]))
            i += 1
        self.map[i-1][j] = 1
        self.total_rooms += 1

    def add_s(self, i, j):
        try:
            if i + 1 >= len(self.map):
                raise Exception('South row does not exist!')
        except:
            self.map.append([0] * len(self.map[0]))
        self.map[i+1][j] = 1
        self.total_rooms += 1

    def add_e(self, i, j):
        try:
            if j + 1 >= len(self.map[i]):
                raise Exception('East column does not exist!')
        except:
            for row in self.map:
                row.append(0)
        self.map[i][j+1] = 1
        self.total_rooms += 1

    def add_w(self, i, j):
        try:
            if j-1 < 0:
                raise Exception('West column does not exist!')
        except:
            for row in self.map:
                row.insert(0, 0)
            j += 1
        self.map[i][j-1] = 1
        self.total_rooms += 1

    def print(self):
        for row in self.map:
            print(row)

    def __len__(self):
        return self.total_rooms


world = World()

world.add_e(0, 0)
world.add_s(0, 0)
world.add_w(0, 0)
world.add_n(0, 1)
world.add_e(1, 2)
world.add_n(1, 3)
world.print()
print(len(world))

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

import re
import copy
from collections import defaultdict

class Brick: #x1, y1, z1, x2, y2, z2
    def __init__(self, init_string):
        x1, y1, z1, x2, y2, z2 = re.fullmatch(r'([0-9]+),([0-9]+),([0-9]+)~([0-9]+),([0-9]+),([0-9]+)', init_string).groups()
        x1, y1, z1, x2, y2, z2 = map(lambda x: int(x), (x1, y1, z1, x2, y2, z2))
        if z2 < z1: #make sure z1 is the lowest
            x, y, z = x1, y1, z1
            x1, y1, z1 = x2, y2, z2
            x2, y2, z2 = x, y, z
        self.start = x1, y1, z1
        self.end = x2, y2, z2
        self.supporting = set()
        cubes = self.calc_cubes()
    def calc_cubes(self):
        majorAxis = -1
        for i in range(3):
            if self.start[i] != self.end[i]:
                majorAxis = i
        if self.start[majorAxis] > self.end[majorAxis]:
            start, end = self.end, self.start
        else:
            start, end = self.start, self.end
        cubes = end[majorAxis] - start[majorAxis] + 1
        ls = [[start[i]] * cubes if majorAxis != i else range(start[i], start[i] + cubes) for i in range(3)]
        self.cubes = [(ls[0][i], ls[1][i], ls[2][i]) for i in range(cubes)]
        return self.cubes
    def drop(self, n):
        x1, y1, z1 = self.start
        x2, y2, z2 = self.end
        self.start = x1, y1, z1 - n
        self.end = x2, y2, z2 - n
        self.calc_cubes()
    def getZ(self): #the lowest z if vertical
        return self.start[2]
    def getCubes(self):
        return self.cubes
    def setID(self, id):
        self.id = id
    def getID(self):
        return self.id
    def addSupporting(self, brick):
        self.supporting.add(brick)
    def getSupporting(self):
        return self.supporting
    


class Stack:
    def __init__(self, input):
        self.brick_dict = defaultdict(list)
        self.brick_dict_ids = {}
        self.grounded_cubes = defaultdict(None)
        self.input = input
        self.cubes_init = defaultdict(None)
        for i in range(10):
            for j in range(10):
                self.cubes_init[(i, j, 0)] = 0 
        self.grounded_cubes = dict(self.cubes_init)
        for i, line in enumerate(input.split('\n')):
            b = Brick(line)
            b.setID(i + 1)
            self.brick_dict_ids[i + 1] = b
            self.brick_dict[b.getZ()].append(b)
    def fall_distance(self, brick):
        for d in range(brick.getZ()):
            for c in brick.getCubes():
                if (c[0], c[1], c[2] - d - 1) in self.grounded_cubes.keys():
                    return d
    def get_brick_list(self):
        return sum(self.brick_dict.values(), [])
    def drop_layer(self, n):
        brick_dict_n = list(self.brick_dict[n])
        count = 0
        for brick in brick_dict_n:
            distance = self.fall_distance(brick)
            z_old = brick.getZ()
            if distance > 0:
                brick.drop(distance)
                z_new = brick.getZ()
                self.brick_dict[z_old].remove(brick)
                self.brick_dict[z_new].append(brick)
                count += 1
            for cube in brick.getCubes():
                self.grounded_cubes[cube] = brick
                x, y, z = cube
                sup = self.grounded_cubes.get((x, y, z -1)) #sup is supporting the current brick
                if sup and sup != brick:
                    sup.addSupporting(brick)
        return count

                # print(cube, brick.getID())
        
    def drop_all(self):
        # self.grounded_cubes = {}
        layers = max([brick.getZ() for brick in self.get_brick_list()] + [0])
        count = 0
        for layer in range(layers + 1):
            l = self.drop_layer(layer)
            count += l
        return count
        # for brick in sum(self.brick_dict.values(), []):
        #     print(brick.getID(), list(map(lambda x: x.getID(), brick.getSupporting())))
    def calc_supported_by(self):
        self.supported_by = defaultdict(set)
        for brick in self.get_brick_list():
            supporting = brick.getSupporting()
            for b in supporting:
                self.supported_by[b.getID()].add(brick.getID())
        # for brick in sum(self.brick_dict.values(), []):
        #     print(brick.getID(), list(map(lambda x: x.getID(), self.supported_by[brick])))
    
    def remove_brick(self, brickID):
        brick = self.brick_dict_ids[brickID]
        del self.brick_dict_ids[brick.getID()]
        self.brick_dict[brick.getZ()].remove(brick)
        for c in brick.getCubes():
            del self.grounded_cubes[c]

    def count_fall(self, brick): #counts the number of bricks that will fall if you remove this brick
        self.__init__(self.input)
        self.drop_all()
        self.remove_brick(brick.getID())
        self.grounded_cubes = dict(self.cubes_init)
        fallen = self.drop_all()
        return fallen

    def count_fall_all_slow(self):
        count = 0
        for id, brick in self.brick_dict_ids.items():
            count += self.count_fall(brick)
            # self.__init__(self.input)
        return count
    
    def count_fall_all(self):
        self.drop_all()
        self.calc_supported_by()
        count = 0
        values = dict()
        for id, brick in self.brick_dict_ids.items():
            to_remove = [id]
            sup_by = copy.deepcopy(self.supported_by)
            while to_remove:
                r = self.brick_dict_ids.get(to_remove.pop(0))
                rid = r.getID()
                if r:
                    sup = r.getSupporting()
                else:
                    sup = []
                sup = list(map(lambda x: x.getID(), sup))
                for b in sup:
                    sup_by[b].discard(rid)
                    if not sup_by.get(b, set()):
                        to_remove.append(b)
                        count += 1
        return count



    def count_removable(self):
        self.can_be_removed = {}
        for b in self.get_brick_list():
            b = b.getID()
            self.can_be_removed.setdefault(b, 1)
            if len(self.supported_by[b]) == 1:
                self.can_be_removed[list(self.supported_by[b])[0]] = 0
        self.removable = sum([value for key, value in self.can_be_removed.items()])
        return self.removable


def main():
    data = open("./Day22/day22.txt").read()  # read the file
    # data = open("./Day22/day22Sample.txt").read()  # read the file
    s = Stack(data)
    j = 1
    s.drop_all()
    s.calc_supported_by()
    print(s.count_removable())
    s2 = Stack(data)
    s2.calc_supported_by()
    print(s2.count_fall_all())

main()
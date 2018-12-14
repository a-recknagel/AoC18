from copy import deepcopy
from itertools import cycle
from typing import List, Tuple

from AoC18 import read_data

test_data1 = r'''|
v
|
|
|
^
|'''.split('\n')
test_data2 = r'''/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   '''.split('\n')
test_data3 = r'''/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/'''.split('\n')


class Orientation:
    UP = '^', (0, -1)
    DOWN = 'v', (0, +1)
    LEFT = '<', (-1, 0)
    RIGHT = '>', (+1, 0)

    LEFT_TURN = {UP[0]: LEFT, LEFT[0]: DOWN, DOWN[0]: RIGHT, RIGHT[0]: UP}
    RIGHT_TURN = {UP[0]: RIGHT, RIGHT[0]: DOWN, DOWN[0]: LEFT, LEFT[0]: UP}
    STRAIGHT = {UP[0]: UP, RIGHT[0]: RIGHT, DOWN[0]: DOWN, LEFT[0]: LEFT}

    CURVE = {'/': {UP[0]: RIGHT_TURN, DOWN[0]: RIGHT_TURN,
                   LEFT[0]: LEFT_TURN, RIGHT[0]: LEFT_TURN},
             '\\': {UP[0]: LEFT_TURN, DOWN[0]: LEFT_TURN,
                    LEFT[0]: RIGHT_TURN, RIGHT[0]: RIGHT_TURN}}

    def __init__(self, init: str):
        self.state: str = init
        self.turns = cycle([self.LEFT_TURN, self.STRAIGHT, self.RIGHT_TURN])

    def move(self, rail) -> Tuple[int, int]:
        if rail == '+':
            next_turn = next(self.turns)
        elif rail in r'\/':
            next_turn = self.CURVE[rail][self.state]
        else:  # rail == '|' or rail == '-'
            next_turn = self.STRAIGHT
        self.state, (y, x) = next_turn[self.state]
        return y, x


class Cart:
    def __init__(self, x: int, y: int, o: str):
        self.x = x
        self.y = y
        self.o = Orientation(o)

    def __gt__(self, other):
        return (self.y, self.x) > (other.y, other.x)

    def __eq__(self, other):
        return (self.y, self.x) == (other.y, other.x)

    def __str__(self):
        return self.o.state

    def __repr__(self):
        return str((self.y, self.x, self.o.state))

    def __hash__(self):
        return hash((self.y, self.x))


class Track:
    def __init__(self, data):
        self.crashes: List[Cart] = []
        # parse input data into something mutable
        x_max = max(len(row) for row in data)
        self.field: List[List[str]] = [[' '] * (x_max + 2)]
        for row in data:
            r = [' '] * x_max
            for i, col in enumerate(row):
                r[i] = col
            self.field.append([' '] + r + [' '])
        self.field.append([' '] * (x_max + 2))
        # generate carts & replace cart markers with correct track symbols
        self.carts: List[Cart] = []
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                if self.field[y][x] in '^v<>':
                    self.carts.append(Cart(x, y, self.field[y][x]))
                    if self.field[y][x] in '^v':
                        self.field[y][x] = '|'
                    elif self.field[y][x] in '<>':
                        self.field[y][x] = '-'
                    else:
                        print('Error in Track.__init__')

    def tick(self):
        self.crashes = []
        occupied = {*self.carts}
        for cart in self.carts:
            if cart in self.crashes:
                continue
            occupied.remove(cart)
            d_x, d_y = cart.o.move(self.field[cart.y][cart.x])
            cart.x += d_x
            cart.y += d_y
            if cart not in occupied:
                occupied.add(cart)
            else:
                self.crashes.extend([c for c in occupied if c == cart])
                self.crashes.append(cart)
                occupied.remove(cart)
        for crash in self.crashes:
            self.carts.remove(crash)
        self.carts.sort()

    def draw(self):
        pic = deepcopy(self.field)
        for cart in self.carts:
            pic[cart.y][cart.x] = cart.o.state
        for crash in self.crashes:
            pic[crash.y][crash.x] = 'x'
        print('\n'.join(''.join(line) for line in pic))


def one(data, draw=False):
    track = Track(data)
    while not track.crashes:
        if draw:
            track.draw()
        track.tick()
    if draw:
        track.draw()
    return f'{track.crashes[0].x - 1},{track.crashes[0].y - 1}'


def two(data, draw=False):
    track = Track(data)
    while len(track.carts) > 1:
        if draw:
            track.draw()
        track.tick()
    if draw:
        track.draw()
    try:
        return f'{track.carts[0].x - 1},{track.carts[0].y - 1}'
    except IndexError:
        return 'no survivors D='


if __name__ == '__main__':
    real_inp = read_data('day_13.txt')
    print(one(test_data1))  # 0,3
    print(one(test_data2))  # 7.3
    print(one(test_data3))  # 2,0
    print(one(real_inp))    # 115,138
    print(two(test_data1))  # no survivors D=
    print(two(test_data2))  # no survivors D=
    print(two(test_data3))  # 6,4
    print(two(real_inp))    # 0,98

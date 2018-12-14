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

    def __init__(self, init: str):
        self.state: str = init
        self.turns = cycle([self.LEFT_TURN, self.STRAIGHT, self.RIGHT_TURN])

    def turn(self, rail) -> Tuple[int, int]:
        if rail == '+':
            next_turn = next(self.turns)
        elif rail == '/':
            if self.state == self.UP[0] or self.state == self.DOWN[0]:
                next_turn = self.RIGHT_TURN
            else:  # self.state == self.LEFT[0] or self.state == self.RIGHT[0]
                next_turn = self.LEFT_TURN
        elif rail == '\\':
            if self.state == self.UP[0] or self.state == self.DOWN[0]:
                next_turn = self.LEFT_TURN
            else:  # self.state == self.LEFT[0] or self.state == self.RIGHT[0]
                next_turn = self.RIGHT_TURN
        else:  # rail == '|' or rail == '-'
            next_turn = self.STRAIGHT
        self.state, turn_coords = next_turn[self.state]
        return turn_coords


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
        self.crashes: List[Tuple[int, int]] = []
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
        occupied_positions = {*self.carts}
        for cart in self.carts:
            occupied_positions.remove(cart)
            d_x, d_y = cart.o.turn(self.field[cart.y][cart.x])
            cart.x += d_x
            cart.y += d_y
            if cart not in occupied_positions:
                occupied_positions.add(cart)
            else:
                self.crashes.append((cart.x, cart.y))
        self.carts.sort()

    def draw(self):
        pic = deepcopy(self.field)
        for cart in self.carts:
            pic[cart.y][cart.x] = cart.o.state
        for crash_x, crash_y in self.crashes:
            pic[crash_y][crash_x] = 'x'
        print('\n'.join(''.join(line) for line in pic))


def one(data, draw=False):
    track = Track(data)
    while not track.crashes:
        if draw:
            track.draw()
        track.tick()
    if draw:
        track.draw()
        print(track.carts)
    return f'{track.crashes[0][0] - 1},{track.crashes[0][1] - 1}'


if __name__ == '__main__':
    real_inp = read_data('day_13.txt')
    print(one(test_data1))  # 0,3
    print(one(test_data2))  # 7.3
    print(one(test_data3))  # 2,0
    print(one(real_inp))    # 115,138

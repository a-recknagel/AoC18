from copy import deepcopy
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

    def __init__(self, init: str):
        self.state: str = init
        self.current_pref: str = 'left'

    def left_turn(self) -> Tuple[int, int]:
        if self.state == self.RIGHT[0]:
            self.state = self.UP[0]
            return self.UP[1]
        elif self.state == self.UP[0]:
            self.state = self.LEFT[0]
            return self.LEFT[1]
        elif self.state == self.LEFT[0]:
            self.state = self.DOWN[0]
            return self.DOWN[1]
        elif self.state == self.DOWN[0]:
            self.state = self.RIGHT[0]
            return self.RIGHT[1]
        else:
            print('Error in Orientation.left_turn')

    def go_straight(self) -> Tuple[int, int]:
        if self.state == self.UP[0]:
            return self.UP[1]
        elif self.state == self.DOWN[0]:
            return self.DOWN[1]
        elif self.state == self.LEFT[0]:
            return self.LEFT[1]
        elif self.state == self.RIGHT[0]:
            return self.RIGHT[1]
        else:
            print('Error in Orientation.go_straight')

    def right_turn(self) -> Tuple[int, int]:
        if self.state == self.RIGHT[0]:
            self.state = self.DOWN[0]
            return self.DOWN[1]
        elif self.state == self.DOWN[0]:
            self.state = self.LEFT[0]
            return self.LEFT[1]
        elif self.state == self.LEFT[0]:
            self.state = self.UP[0]
            return self.UP[1]
        elif self.state == self.UP[0]:
            self.state = self.RIGHT[0]
            return self.RIGHT[1]
        else:
            print('Error in Orientation.right_turn')

    def turn(self) -> Tuple[int, int]:
        if self.current_pref == 'left':
            self.current_pref = 'straight'
            return self.left_turn()
        elif self.current_pref == 'straight':
            self.current_pref = 'right'
            return self.go_straight()
        elif self.current_pref == 'right':
            self.current_pref = 'left'
            return self.right_turn()
        else:
            print('Error in Orientation.turn')

    def apply(self, rail) -> Tuple[int, int]:
        if rail == '+':
            return self.turn()
        elif rail == r'/':
            if self.state == self.UP[0] or self.state == self.DOWN[0]:
                return self.right_turn()
            if self.state == self.LEFT[0] or self.state == self.RIGHT[0]:
                return self.left_turn()
        elif rail == '\\':
            if self.state == self.UP[0] or self.state == self.DOWN[0]:
                return self.left_turn()
            if self.state == self.LEFT[0] or self.state == self.RIGHT[0]:
                return self.right_turn()
        elif rail == '|' or rail == '-':
            return self.go_straight()
        else:
            print('Error in Orientation.apply')


class Cart:
    def __init__(self, x: int, y: int, o: str):
        self.x = x
        self.y = y
        self.o = Orientation(o)

    def __gt__(self, other):
        return (self.y, self.x) > (other.y, other.x)

    def __str__(self):
        return self.o.state

    def __repr__(self):
        return str((self.y, self.x, self.o.state, self.o.current_pref))


class Track:
    def __init__(self, data):
        self.crashes = []
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
        self.carts = []
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
        occupied_positions = set()
        for cart in self.carts:
            d_x, d_y = cart.o.apply(self.field[cart.y][cart.x])
            cart.x += d_x
            cart.y += d_y
            new_pos = (cart.x, cart.y)
            if new_pos not in occupied_positions:
                occupied_positions.add(new_pos)
            else:
                self.crashes.append(new_pos)
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
    print(one(real_inp))    # 94,65

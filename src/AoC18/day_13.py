from copy import deepcopy
from typing import Tuple

from AoC18 import read_data

inp = r'''/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/'''.split('\n')


class Track:
    def __init__(self, data):
        # parse input data into something mutable
        x_max = max(len(row) for row in data)
        self.field = [[' '] * (x_max + 2)]
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
                    self.carts.append(Cart(x, y, self.field[y][x], self))
                    if self.field[y][x] in '^v':
                        self.field[y][x] = '|'
                    else:  # self.field[y][x] in '<>'
                        self.field[y][x] = '-'

    def tick(self):
        for cart in self.carts:
            cart.tick()
        self.carts.sort()

    def draw(self, draw=True):
        collision = ''
        pic = deepcopy(self.field)
        for cart in self.carts:
            if pic[cart.y][cart.x] in '^v<>x':
                pic[cart.y][cart.x] = 'x'
                collision = f'{cart.x-1},{cart.y-1}'  # subtract for borders
            else:
                pic[cart.y][cart.x] = cart.o.state
        if draw:
            print('\n'.join(''.join(line) for line in pic))
        return collision


class Orientation:
    UP = '^', (0, -1)
    DOWN = 'v', (0, +1)
    LEFT = '<', (-1, 0)
    RIGHT = '>', (1, 0)

    def __init__(self, init):
        self.state = init
        self.current_pref = 'left'

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
            print('Error in left_turn')

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
            print('Error in go_straight')

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
            print('Error in right_turn')

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
            print('Error in turn')

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
            print('Error in apply')


class Cart:
    def __init__(self, x, y, o, track: Track):
        self.x = x
        self.y = y
        self.o = Orientation(o)
        self.track = track

    def tick(self):
        d_x, d_y = self.o.apply(self.track.field[self.y][self.x])
        self.x += d_x
        self.y += d_y

    def __gt__(self, other):
        return (self.y, self.x) > (other.y, other.x)

    def __str__(self):
        return self.o.state

    def __repr__(self):
        return str((self.y, self.x, self.o.state, self.o.current_pref))


def one(data):
    track = Track(data)
    while True:
        collisions = track.draw(draw=False)
        if collisions:
            return collisions
        track.tick()


if __name__ == '__main__':
    real_inp = read_data('day_13.txt')
    print(one(real_inp))

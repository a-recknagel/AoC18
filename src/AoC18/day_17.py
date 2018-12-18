import itertools
import re
from typing import Set, Tuple

from AoC18 import read_data

test_1 = '''x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504'''.split('\n')


def get_range(r):
    if '..' not in r:
        return [int(r)]
    s, e = map(int, r.split('..'))
    return [*range(s, e+1)]


class Map:
    def __init__(self, data):
        # parse input data into clay-coordinates
        get_y = re.compile(r'y=((\d+\.\.\d+)|(\d+))')
        get_x = re.compile(r'x=((\d+\.\.\d+)|(\d+))')
        clay = []
        for line in data:
            y_range = get_range(get_y.search(line).group(1))
            x_range = get_range(get_x.search(line).group(1))
            clay.extend(itertools.product(y_range, x_range))
        # find area dimensions, initialize area with them
        max_y, min_x, max_x = 0, 500, 500
        for y, x in clay:
            max_y = max(max_y, y)
            min_x = min(min_x, x)
            max_x = max(max_x, x)
        self.area = [['.'] * abs(min_x - (max_x + 3)) for _ in
                     range(max_y+1)]
        # fill with clay
        for y, x in clay:
            self.area[y][x-min_x+1] = '#'
        # add source, add first drop below it. 'drops' is a set to avoid merging streams to create duplicate drops
        self.area[0][501-min_x] = '+'
        self.drops: Set[Tuple[int, int]] = {(1, 501-min_x)}

    def fill(self, y, x):
        # find out how far the water can flow, and if it is an enclosed level
        enclosed_left, enclosed_right = True, True
        left_x, right_x = (x-1, x+1)
        while enclosed_left:
            if self.area[y][left_x] == '#':
                break
            if self.area[y+1][left_x] == '.':
                enclosed_left = False
            left_x -= 1
        left_x += 1
        while enclosed_right:
            if self.area[y][right_x] == '#':
                break
            if self.area[y+1][right_x] == '.':
                enclosed_right = False
            right_x += 1
        # if enclosed to both sides -> standing water + add drop one level above
        if enclosed_left and enclosed_right:
            self.area[y][left_x:right_x] = ['~'] * (right_x - left_x)
            yield (y-1, x)
        # if not -> flowing water and add drops where appropriate
        else:
            self.area[y][left_x:right_x] = ['|'] * (right_x - left_x)
            if not enclosed_left:
                yield (y, left_x)
            if not enclosed_right:
                yield (y, right_x-1)

    def tick(self):
        new_drops: Set[Tuple[int, int]] = set()
        for y, x in self.drops:
            self.area[y][x] = '|'
            try:
                below = self.area[y+1][x]
            except IndexError:
                continue  # not counted: below maximum y value
            if below == '|':
                continue  # don't let water flow on top of flowing water
            if below == '.':
                new_drops.add((y+1, x))  # straight down
            else:
                new_drops |= {*self.fill(y, x)}  # to the sides
        self.drops = new_drops

    def picture(self, draw=True):
        pic = '\n'.join(''.join(row) for row in self.area)
        if draw:
            print(pic)
        return pic.count('|'), pic.count('~')


def one(data):
    m = Map(data)
    while m.drops:
        m.tick()
    flowing, settled = m.picture(draw=True)
    return flowing + settled


def two(data):
    m = Map(data)
    while m.drops:
        m.tick()
    flowing, settled = m.picture(draw=True)
    return settled


if __name__ == '__main__':
    real_inp = read_data('day_17.txt')
    print(one(test_1))    # 57
    print(one(real_inp))  # 30746, incorrect. 9 too many, still dunno why =[
    print(two(real_inp))  # 24699


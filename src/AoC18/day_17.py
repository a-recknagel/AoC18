import itertools
import re
from typing import List, Tuple

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
        get_y = re.compile(r'y=((\d+\.\.\d+)|(\d+))')
        get_x = re.compile(r'x=((\d+\.\.\d+)|(\d+))')
        clay = []
        for line in data:
            y_range = get_range(get_y.search(line).group(1))
            x_range = get_range(get_x.search(line).group(1))
            clay.extend(itertools.product(y_range, x_range))
        self.source = (0, 500)
        self.min_y, self.max_y, self.min_x, self.max_x = (
            self.source[0], self.source[0], self.source[1], self.source[1])
        for y, x in clay:
            self.min_y = min(self.min_y, y)
            self.max_y = max(self.max_y, y)
            self.min_x = min(self.min_x, x)
            self.max_x = max(self.max_x, x)
        self.area = [['.'] * abs(self.min_x - (self.max_x + 3)) for _ in
                     range(self.min_y, self.max_y+1)]
        for y, x in clay:
            self.area[y-self.min_y][x-self.min_x+1] = '#'
        self.area[self.source[0]-self.min_y][self.source[1]-self.min_x+1] = '+'
        self.drops: List[Tuple[int, int]] = [
            (self.source[0]+1-self.min_y, self.source[1]+1-self.min_x)]

    def fill(self, y, x):
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
        if enclosed_left and enclosed_right:
            self.area[y][left_x:right_x] = ['~'] * (right_x - left_x)
            yield (y-1, x)
        else:
            self.area[y][left_x:right_x] = ['|'] * (right_x - left_x)
            if not enclosed_left:
                yield (y, left_x)
            if not enclosed_right:
                yield (y, right_x-1)

    def tick(self):
        if not self.drops:
            return False
        new_drops = []
        for y, x in self.drops:
            self.area[y][x] = '|'
            try:
                below = self.area[y+1][x]
            except IndexError:
                # print(f"(drop ({y+1}, {x}) not counted: below maximum y
                # value)")
                continue
            if below == '|':
                continue  # seems sensible...
            if below == '.':
                new_drops.append((y+1, x))
            else:
                new_drops.extend(self.fill(y, x))
        self.drops = new_drops
        return True

    def draw(self):
        pic = '\n'.join(''.join(row) for row in self.area)
        print(pic)
        print(f"Watery tiles: {pic.count('|') + pic.count('~')}\n")


def one(data):
    m = Map(data)
    count = 0
    m.draw()
    while m.tick():
        count += 1
    m.draw()


if __name__ == '__main__':
    real_inp = read_data('day_17.txt')
    one(real_inp)


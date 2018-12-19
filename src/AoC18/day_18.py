from copy import deepcopy
from typing import List

from AoC18 import read_data

test_1 = '''\
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.'''.split('\n')


class LumberArea:
    def __init__(self, data):
        self.field: List[List[str]] = [[*row] for row in data]
        self.memory = {}

    def get_surroundings(self, y, x):
        ret = {'.': 0, '|': 0, '#': 0}
        for y_d, x_d in [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                         (0, 1), (1, -1), (1, 0), (1, 1)]:
            try:
                if (y+y_d) < 0 or (x+x_d) < 0:  # skip negative indices
                    continue
                acre = self.field[y+y_d][x+x_d]
                ret[acre] += 1
            except IndexError:
                continue
        return ret

    def multi_tick(self, times):
        for t in range(times):
            current = self.picture()
            if current in self.memory:  # cycle found!
                cycle_length = t - self.memory[current]
                jump_idx = (times - t) % cycle_length
                # print(f"jumping ahead {jump_idx} times, skipping {times-t}.")
                for ff in range(jump_idx):
                    self.tick()
                break
            else:
                self.memory[current] = t
            self.tick()

    def tick(self):
        update = deepcopy(self.field)
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                surroundings = self.get_surroundings(y, x)
                if self.field[y][x] == '.' and surroundings['|'] >= 3:
                    update[y][x] = '|'
                if self.field[y][x] == '|' and surroundings['#'] >= 3:
                    update[y][x] = '#'
                if self.field[y][x] == '#':
                    if surroundings['|'] < 1 or surroundings['#'] < 1:
                        update[y][x] = '.'
        self.field = update

    def picture(self):
        return '\n'.join(''.join(row) for row in self.field)

    def value(self):
        pic = self.picture()
        return pic.count('.'), pic.count('|'), pic.count('#')


def one(data):
    l_a = LumberArea(data)
    l_a.multi_tick(10)
    print(l_a.picture())
    free, tree, lumb = l_a.value()
    return lumb * tree


def two(data):
    l_a = LumberArea(data)
    l_a.multi_tick(1000000000)
    print(l_a.picture())
    free, tree, lumb = l_a.value()
    return lumb * tree


if __name__ == '__main__':
    real_inp = read_data('day_18.txt')
    print(one(test_1))    # 1147
    print(two(test_1))    # 0
    print(one(real_inp))  # 588436
    print(two(real_inp))  # 195290



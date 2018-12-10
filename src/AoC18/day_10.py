from AoC18 import read_data

import re

points_re = re.compile(
    r'position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>')


class Stars:
    def __init__(self, data):
        self.count = 0
        self.points = []
        for line in data:
            x, y, x_d, y_d = map(int, points_re.match(line).groups())
            self.points.append([[x, y], (x_d, y_d)])

    def tick(self):
        self.count += 1
        for point in self.points:
            point[0][0] += point[1][0]
            point[0][1] += point[1][1]

    def is_msg(self):
        for point, _ in self.points:
            for comp, _ in self.points:
                if point == comp:
                    continue
                if abs(point[0]-comp[0]) <= 1 and abs(point[1]-comp[1]) <= 1:
                    break
            else:
                return False
        return True

    def msg(self):
        min_x, min_y, max_x, max_y = (
            float('inf'), float('inf'), -float('inf'), -float('inf'))
        for (x, y), d in self.points:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + 1)
            max_y = max(max_y, y + 1)
        field = [['.'] * (max_x - min_x) for _ in range(max_y - min_y)]
        for (x, y), _ in self.points:
            field[y-min_y][x-min_x] = '*'
        return '\n'.join(''.join(row) for row in field)


def one_and_two(data):
    s = Stars(data)
    while True:
        if s.is_msg():
            return s.msg(), s.count
        else:
            s.tick()


if __name__ == '__main__':
    inp = read_data('day_10.txt')
    message, iteration = one_and_two(inp)
    print(message)
    print(iteration)

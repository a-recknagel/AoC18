from AoC18 import read_data


def mh_dist(a, b):
    t0 = a[0] - b[0]
    t0 = -t0 if t0 < 0 else t0
    t1 = a[1] - b[1]
    t1 = -t1 if t1 < 0 else t1
    return t0 + t1


class Field:

    def __init__(self):
        inp = read_data('day_6.txt')
        self.origins = [tuple(map(int, line.split(', '))) for line in inp]
        c_max = max(p[1] for p in self.origins) + 1
        r_max = max(p[0] for p in self.origins) + 1
        self.field = [[None] * c_max for _ in range(r_max)]

    def fill(self):
        for r_idx in range(len(self.field)):
            for c_idx in range(len(self.field[r_idx])):
                closest = None
                min_dist = len(self.field) * len(self.field[r_idx])
                for point in self.origins:
                    d = mh_dist(point, (r_idx, c_idx))
                    if d < min_dist:
                        min_dist = d
                        closest = point
                    elif d == min_dist:
                        closest = None
                self.field[r_idx][c_idx] = closest

    def one(self):
        self.fill()
        to_remove = set()
        for r in range(len(self.field)):
            to_remove.add(self.field[r][0])
            to_remove.add(self.field[r][len(self.field[r]) - 1])
        for c in range(len(self.field[0])):
            to_remove.add(self.field[0][c])
            to_remove.add(self.field[len(self.field) - 1][c])
        to_remove.remove(None)
        area_counts = {a: 0 for a in (set(self.origins) - to_remove)}
        for row in self.field:
            for point in row:
                if point in area_counts:
                    area_counts[point] += 1
        return max(area_counts.values())

    def two(self):
        size = 0
        threshold = 10000
        for r_idx in range(len(self.field)):
            for c_idx in range(len(self.field[r_idx])):
                dist_count = 0
                for o in self.origins:
                    dist_count += mh_dist((r_idx, c_idx), o)
                    if dist_count >= threshold:
                        break
                else:
                    size += 1
        return size


if __name__ == '__main__':
    f = Field()
    print(f.one())
    print(f.two())

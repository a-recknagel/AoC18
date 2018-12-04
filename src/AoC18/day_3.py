import re

from AoC18 import read_data

parse_claim = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
claims = set()


def mark(f, s):
    idx, left, top, width, height = map(int, parse_claim.match(s).groups())
    claims.add(idx)
    for row in range(height):
        for col in range(width):
            f[row+top][col+left].append(idx)


def one():
    field = [[[] for _ in (range(1000))] for _ in range(1000)]
    data = read_data('day_3.txt')
    for claim in data:
        mark(field, claim)
    shared = 0
    for row in field:
        for col in row:
            if len(col) > 1:
                shared += 1
    print(shared)


def two():
    field = [[[] for _ in (range(1000))] for _ in range(1000)]
    data = read_data('day_3.txt')
    for claim in data:
        mark(field, claim)
    # 'claims' is now populated

    for row in field:
        for col in row:
            if len(col) > 1:
                for claim in col:
                    if claim in claims:
                        claims.remove(claim)
    print(*claims)


if __name__ == '__main__':
    one()
    two()

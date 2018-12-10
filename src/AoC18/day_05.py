from AoC18 import read_data

import re
from string import ascii_lowercase, ascii_uppercase


pol_matcher = re.compile(
    '|'.join([f'{l}{u}|{u}{l}' for l, u in zip(ascii_lowercase, ascii_uppercase)])
)


def two():
    base = read_data('day_5.txt')[0]
    res = len(base)
    for x, y in zip(ascii_lowercase, ascii_uppercase):
        inp = base.replace(x, '').replace(y, '')
        res = min(res, one(inp))
    return res


def one(inp=read_data('day_5.txt')[0]):
    while True:
        new = pol_matcher.sub('', inp)
        if inp == new:
            break
        inp = new
    return len(inp)


if __name__ == '__main__':
    print(one())
    print(two())

from typing import Iterable, List, Optional, Tuple

from AoC18 import read_data

test_1 = '^WNE$'
test_2 = '^ENWWW(NEEE|SSE(EE|N))$'
test_3 = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'
test_4 = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
test_5 = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'


def partition_group(s: str) -> Optional[Tuple[int, int, List[int]]]:
    try:
        l_idx = s.index('(') + 1
    except ValueError:
        return None
    lvl, r_idx, b = 1, l_idx, []
    while lvl > 0:
        r_idx += 1
        if s[r_idx] == '(':
            lvl += 1
        if s[r_idx] == ')':
            lvl -= 1
        if s[r_idx] == '|' and lvl == 1:
            b.append(r_idx)
    b.append(r_idx)
    return l_idx, r_idx, b


def unravel(current: str, prefix: str = '') -> Iterable[str]:
    group = partition_group(current)
    if group is None:
        yield prefix + current
    else:
        start, end, branches = group
        prefix += current[:start-1]
        postfix = current[end+1:]
        for branch in branches:
            yield from unravel(current[start:branch] + postfix, prefix)
            start = branch + 1


def one(data):
    data = data[1:-1]
    return sorted(map(len, unravel(data)))[-1]


def two(data):
    ...


if __name__ == '__main__':
    inp = read_data('day_20.txt')[0]
    print(one(test_1))  # 3
    print(one(test_2))  # 10
    print(one(test_3))  # 30
    print(one(test_4))  # 23
    print(one(test_5))  # 31
    print(one(inp))     # ????

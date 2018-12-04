from pathlib import PurePath


def read_data(f_n):
    ret = []
    parent = PurePath(__file__).parent
    with open(parent / 'data' / f_n) as f:
        for line in f:
            ret.append(line.rstrip('\n'))
    return ret

from pathlib import Path


def read_data(f_n):
    ret = []
    with open(Path(f'data/{f_n}')) as f:
        for line in f:
            ret.append(line.rstrip('\n'))
    return ret

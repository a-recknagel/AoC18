from AoC18 import read_data


def one():
    inp = read_data('day_2.txt')
    chars = {char for row in inp for char in row}
    twos = 0
    threes = 0
    for row in inp:
        two_seen = False
        three_seen = False
        for char in chars:
            c = row.count(char)
            if c == 2 and not two_seen:
                twos += 1
                two_seen = True
            if c == 3 and not three_seen:
                threes += 1
                three_seen = True
    print(twos*threes)


def two():
    inp = read_data('day_2.txt')
    tolerance = 1
    for row_idx in range(len(inp)):
        for comp_idx in range(row_idx+1, len(inp)):
            current_tolerance = 0
            sames = []
            for idx in range(len(inp[row_idx])):
                if inp[row_idx][idx] != inp[comp_idx][idx]:
                    if current_tolerance < tolerance:
                        current_tolerance += 1
                    else:
                        break
                else:
                    sames.append(inp[row_idx][idx])
            else:
                print(''.join(sames))


if __name__ == '__main__':
    two()

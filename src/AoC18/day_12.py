from AoC18 import read_data


def plant_generator(data, num_gens):
    offset = num_gens + 5
    current, last = ('.'*offset) + data[0][15:] + ('.'*offset), ''
    rules = [s[:5] for s in data[2:] if s.endswith('#')]
    for _ in range(num_gens):
        new = ['.'] * len(current)
        for rule in rules:
            match = -1
            while True:
                match = current.find(rule, match+1)
                if match < 0:
                    break
                new[match+2] = '#'
        last = current
        current = ''.join(new)
    return sum(idx - offset for idx in range(len(current))
               if current[idx] == '#'), current, last[:-1] == current[1:]

def one(data, num_gens):
    ret, _, _ = plant_generator(data, num_gens)
    return ret


def two(data, num_runs):
    when_cycled = 50
    plants, is_cycle = '', False
    while not is_cycle:
        _, plants, is_cycle = plant_generator(data, when_cycled)
        when_cycled += 50

    print(when_cycled, plants)

    indices = [idx-(when_cycled+5) for idx in range(len(plants))
               if plants[idx] == '#']
    return sum(idx+(num_runs-when_cycled) for idx in indices)


if __name__ == '__main__':
    inp = read_data('day_12.txt')
    print(one(inp, 20))
    print(two(inp, 50000000000))

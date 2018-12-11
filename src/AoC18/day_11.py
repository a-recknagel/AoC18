from AoC18 import read_data


def get_power_level(x, y, serial):
    rack_id = x + 10
    ret = rack_id * y
    ret += serial
    ret *= rack_id
    ret = (ret % 1000) // 100
    return ret - 5


def find_max_region(field, size):
    max_coords = (None, None)
    max_power = -float('inf')
    for x in range(len(field)-size):
        for y in range(len(field[x])-size):
            current = 0
            for offset_x in range(size):
                for offset_y in range(size):
                    current += field[x+offset_x][y+offset_y]
            if current > max_power:
                max_power = current
                max_coords = (x+1, y+1)  # top left with indices starting at one
    return max_coords, max_power


def one(serial):
    field = [[None]*300 for _ in range(300)]
    for x in range(len(field)):
        for y in range(len(field[x])):
            field[x][y] = get_power_level(x+1, y+1, serial)
    max_coords, _ = find_max_region(field, 3)
    return f"{max_coords[0]},{max_coords[1]}"


def two(serial):
    field = [[None]*300 for _ in range(300)]
    for x in range(len(field)):
        for y in range(len(field[x])):
            field[x][y] = get_power_level(x+1, y+1, serial)
    max_coords = (None, None)
    max_grid_size = 0
    max_power = -float('inf')
    for size in range(1, 20):
        coords, power = find_max_region(field, size)
        if power > max_power:
            max_coords, max_power, max_grid_size = coords, power, size
    return f"{max_coords[0]},{max_coords[1]},{max_grid_size}"


if __name__ == '__main__':
    inp = int(read_data('day_11.txt')[0])
    print(one(inp))
    print(two(inp))

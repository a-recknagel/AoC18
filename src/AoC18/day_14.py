from AoC18 import read_data


def digits(num):
    yield from map(int, str(num))


def one(data):
    num_recipes = int(data)
    elf_1, elf_2 = 0, 1
    scores = [3, 7]
    while len(scores) <= (num_recipes + 10):
        recipe = scores[elf_1] + scores[elf_2]
        for digit in digits(recipe):
            scores.append(digit)
        elf_1 = (elf_1 + scores[elf_1] + 1) % len(scores)
        elf_2 = (elf_2 + scores[elf_2] + 1) % len(scores)
    return ''.join(map(str, scores[num_recipes:num_recipes+10]))


def two(data):
    elf_1, elf_2 = 0, 1
    scores = [3, 7]
    target = [int(s) for s in data]
    while True:
        recipe = scores[elf_1] + scores[elf_2]
        for digit in digits(recipe):
            scores.append(digit)
        if len(scores) < len(target):
            continue
        for i in range(len(target)):
            if scores[-(i+1)] != target[-(i+1)]:
                break
        else:
            return len(scores) - 5
        for i in range(len(target)):
            if scores[-(i+2)] != target[-(i+1)]:
                break
        else:
            return len(scores) - 7  # ... why 7 and not 6?
        elf_1 = (elf_1 + scores[elf_1] + 1) % len(scores)
        elf_2 = (elf_2 + scores[elf_2] + 1) % len(scores)


if __name__ == '__main__':
    inp = read_data('day_14.txt')[0]
    print(one(inp))
    print(two(inp))



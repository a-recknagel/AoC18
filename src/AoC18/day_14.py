def digits(num):
    yield from map(int, str(num))


def one(data, num_recipes):
    elf_1 = 0
    elf_2 = 1
    scores = [*digits(data)]
    while len(scores) <= (num_recipes + 10):
        recipe = scores[elf_1] + scores[elf_2]
        for digit in digits(recipe):
            scores.append(digit)
        elf_1 = (elf_1 + scores[elf_1] + 1) % len(scores)
        elf_2 = (elf_2 + scores[elf_2] + 1) % len(scores)
    print(scores)
    return ''.join(map(str, scores[num_recipes:num_recipes+10]))


def two():
    ...


if __name__ == '__main__':
    inp = 681901
    print(one(str(inp), inp))
    two()

from AoC18 import read_data

from ast import literal_eval


class Device:
    OP_CODE_MAP = None

    def __init__(self, reg_0, reg_1, reg_2, reg_3):
        self.regs = [reg_0, reg_1, reg_2, reg_3]

    def addr(self, reg_a, reg_b, reg_c):
        self.regs[reg_c] = self.regs[reg_a] + self.regs[reg_b]

    def addi(self, reg_a, val_b, reg_c):
        self.regs[reg_c] = self.regs[reg_a] + val_b

    def mulr(self, reg_a, reg_b, reg_c):
        self.regs[reg_c] = self.regs[reg_a] * self.regs[reg_b]

    def muli(self, reg_a, val_b, reg_c):
        self.regs[reg_c] = self.regs[reg_a] * val_b

    def banr(self, reg_a, reg_b, reg_c):
        self.regs[reg_c] = self.regs[reg_a] & self.regs[reg_b]

    def bani(self, reg_a, val_b, reg_c):
        self.regs[reg_c] = self.regs[reg_a] & val_b

    def borr(self, reg_a, reg_b, reg_c):
        self.regs[reg_c] = self.regs[reg_a] | self.regs[reg_b]

    def bori(self, reg_a, val_b, reg_c):
        self.regs[reg_c] = self.regs[reg_a] | val_b

    def setr(self, reg_a, _, reg_c):
        self.regs[reg_c] = self.regs[reg_a]

    def seti(self, val_a, _, reg_c):
        self.regs[reg_c] = val_a

    def gtir(self, val_a, reg_b, reg_c):
        self.regs[reg_c] = int(val_a > self.regs[reg_b])

    def gtri(self, reg_a, val_b, reg_c):
        self.regs[reg_c] = int(self.regs[reg_a] > val_b)

    def gtrr(self, reg_a, reg_b, reg_c):
        self.regs[reg_c] = int(self.regs[reg_a] > self.regs[reg_b])

    def eqir(self, val_a, reg_b, reg_c):
        self.regs[reg_c] = int(val_a == self.regs[reg_b])

    def eqri(self, reg_a, val_b, reg_c):
        self.regs[reg_c] = int(self.regs[reg_a] == val_b)

    def eqrr(self, reg_a, reg_b, reg_c):
        self.regs[reg_c] = int(self.regs[reg_a] == self.regs[reg_b])

    def try_all(self, before, params, after):
        op_code_matches = []
        for func in [
                self.addr, self.addi, self.mulr, self.muli, self.banr, self.bani,
                self.borr, self.bori, self.setr, self.seti, self.gtir, self.gtri,
                self.gtrr, self.eqir, self.eqri, self.eqrr]:
            self.__init__(*before)
            func(*params[1:])
            if self.regs == after:
                op_code_matches.append((params[0], func.__name__))
        return op_code_matches


def one(data):
    def parse(stream):
        s = iter(stream)
        while True:
            try:
                yield (literal_eval(next(s)[8:]),
                       [*map(int, next(s).split())],
                       literal_eval(next(s)[8:]))
                next(s)  # should be empty line
            except StopIteration:
                break

    # find answer to part 1
    device = Device(0, 0, 0, 0)
    count = 0
    for before, params, after in parse(data):
        matches = device.try_all(before, params, after)
        if len(matches) >= 3:
            count += 1

    # find op code map
    op_codes = {}
    while len(op_codes) < 16:
        for before, params, after in parse(data):
            matches = device.try_all(before, params, after)
            matches = [m for m in matches if m[1] not in op_codes.values()]
            if len(matches) == 1:
                op_codes[matches[0][0]] = matches[0][1]
    # print(op_codes)
    Device.OP_CODE_MAP = op_codes
    return count


def two(data):
    device = Device(0, 0, 0, 0)
    for line in data:
        op, *params = [*map(int, line.split())]
        getattr(device, Device.OP_CODE_MAP[op])(*params)
    return device.regs[0]


if __name__ == '__main__':
    inp_a = read_data('day_16_a.txt')
    print(one(inp_a))
    inp_b = read_data('day_16_b.txt')
    print(two(inp_b))

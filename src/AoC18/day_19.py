from AoC18 import read_data

test_1 = '''\
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5'''.split('\n')


class Device:

    def __init__(self):
        self.regs = [0, 0, 0, 0, 0, 0]
        self.ip_reg = None

    def __str__(self):
        return f"ip={self.regs[self.ip_reg]}, {self.regs}"

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

    def run(self, raw_program):
        ip_reg, *raw = raw_program
        self.ip_reg = int(ip_reg[4])
        program = []
        for i in raw:
            op, a, b, c = i.split()
            program.append((getattr(self, op), int(a), int(b), int(c)))
        while 0 <= self.regs[self.ip_reg] < len(program):
            op, *args = program[self.regs[self.ip_reg]]
            if VERBOSE:
                print(self, [op.__name__, *args], end=' -> ')
            op(*args)
            if VERBOSE:
                print(self)
            self.regs[self.ip_reg] += 1
        print(self.regs[0])


def one(data):
    d = Device()
    d.run(data)


def two(data):
    d = Device()
    d.regs[0] = 1
    d.run(data)


if __name__ == '__main__':
    VERBOSE = True
    inp = read_data('day_19.txt')
    print(one(inp))  # terminates, 912
    print(two(inp))  # doesn't terminate

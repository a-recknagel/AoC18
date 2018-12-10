class Marble:
    def __init__(self, val, prev, nxt):
        if prev is None:  # handle first marble
            prev = self
        if nxt is None:
            nxt = self
        self.val = val
        self.prev = prev
        self.prev.nxt = self
        self.nxt = nxt
        self.nxt.prev = self


def cycle(num):
    while True:
        yield from range(1, num+1)


def solve(players, tries):
    start = Marble(0, None, None)
    points = [0]*players
    current = start
    for trie in range(1, tries+1):
        player = trie % players
        if (trie % 23) == 0:
            to_remove = current.prev.prev.prev.prev.prev.prev.prev
            points[player] += trie + to_remove.val
            to_remove.prev.nxt = to_remove.nxt
            to_remove.nxt.prev = to_remove.prev
            current = to_remove.nxt
        else:
            new = Marble(trie, current.nxt, current.nxt.nxt)
            current = new
    return max(points)


def one():
    return solve(416, 71975)


def two():
    return solve(416, 7197500)


if __name__ == '__main__':
    print(one())
    print(two())  # 17s wall time

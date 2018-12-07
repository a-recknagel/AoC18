from AoC18 import read_data

import re
from collections import defaultdict
from heapq import heappush, heappop
from string import ascii_uppercase

node_matcher = re.compile(
    r'Step ([A-Z]) must be finished before step ([A-Z]) can begin\.')


def one():
    inp = read_data('day_7.txt')
    finished = []
    work_queue = []
    mappings = defaultdict(lambda: [[], set()])
    for line in inp:
        node, inhibited = node_matcher.match(line).groups()
        mappings[node][0].append(inhibited)
        mappings[inhibited][1].add(node)
    for node in mappings:
        if not mappings[node][1]:
            heappush(work_queue, node)
    while work_queue:
        current = heappop(work_queue)
        finished.append(current)
        for node in mappings[current][0]:
            mappings[node][1].remove(current)
            if not mappings[node][1]:
                heappush(work_queue, node)
    return ''.join(finished)


def two():
    inp = read_data('day_7.txt')
    finished = []
    work_queue = []
    work_times = {step: duration+61 for duration, step
                  in enumerate(ascii_uppercase)}
    free_workers = [0, 1, 2, 3, 4]
    jobs = {}  # job -> [worker, duration]; 'G' -> [0, 5]
    mappings = defaultdict(lambda: [[], set()])
    for line in inp:
        node, inhibited = node_matcher.match(line).groups()
        mappings[node][0].append(inhibited)
        mappings[inhibited][1].add(node)
    for node in mappings:
        if not mappings[node][1]:
            heappush(work_queue, node)
    tick = 0
    while True:
        tick += 1
        for job in [*jobs]:
            jobs[job][1] += 1
            if jobs[job][1] >= work_times[job]:
                finished.append(job)
                free_workers.append(jobs[job][0])
                for node in mappings[job][0]:
                    mappings[node][1].remove(job)
                    if not mappings[node][1]:
                        heappush(work_queue, node)
                del jobs[job]
        while work_queue and free_workers:
            current = heappop(work_queue)
            jobs[current] = [heappop(free_workers), 0]
        if not work_queue and not jobs:
            break
    return ''.join(finished)


if __name__ == '__main__':
    print(one())
    print(two())

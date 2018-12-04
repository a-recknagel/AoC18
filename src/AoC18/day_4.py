import re

from AoC18 import read_data


times_re = re.compile(r'\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.*)')
guard_re = re.compile(r'(#\d+)')


def one():
    times = []
    for entry in read_data('day_4.txt'):
        m = times_re.match(entry)
        if m:
            times.append(m.groups())
        else:
            print(f'something went wrong during times regexing: {entry}')
    times.sort()
    sleep_times = {}
    current_guard = None
    for entry in times:
        guard = guard_re.search(entry[5])
        if guard:
            current_guard = guard.group(1)
            if current_guard not in sleep_times:
                sleep_times[current_guard] = []
        elif entry[5] == 'falls asleep':
            sleep_times[current_guard].append([entry[:5]])
        elif entry[5] == 'wakes up':
            sleep_times[current_guard][-1].append(entry[:5])
        else:
            print(f'something went wrong during sleeptime parsing: {entry}')

    curr_max, max_guard = 0, None
    for guard, sleeps in sleep_times.items():
        sleep_sum = 0
        for start, end in sleeps:
            start_minute, end_minute = map(int, (start[4], end[4]))
            sleep_sum += (end_minute - start_minute)
        if sleep_sum > curr_max:
            curr_max = sleep_sum
            max_guard = guard

    sections = []
    for start, end in sleep_times[max_guard]:
        start_minute, end_minute = map(int, (start[4], end[4]))
        block = [1 if start_minute <= m < end_minute else 0 for m in range(60)]
        sections.append(block)

    max_sleep = 0
    max_minute = None
    for i in range(60):
        current_sum = 0
        for block in sections:
            current_sum += block[i]
        if current_sum > max_sleep:
            max_sleep = current_sum
            max_minute = i
    print(max_minute*int(max_guard[1:]))


def two():
    times = []
    for entry in read_data('day_4.txt'):
        m = times_re.match(entry)
        if m:
            times.append(m.groups())
        else:
            print(f'something went wrong during times regexing: {entry}')
    times.sort()
    sleep_times = {}
    current_guard = None
    for entry in times:
        guard = guard_re.search(entry[5])
        if guard:
            current_guard = guard.group(1)
            if current_guard not in sleep_times:
                sleep_times[current_guard] = []
        elif entry[5] == 'falls asleep':
            sleep_times[current_guard].append([entry[:5]])
        elif entry[5] == 'wakes up':
            sleep_times[current_guard][-1].append(entry[:5])
        else:
            print(f'something went wrong during sleeptime parsing: {entry}')

    max_guard = None
    max_sleep = None
    max_sleeps_count = 0
    for guard, sleeps in sleep_times.items():
        sections = []
        for start, end in sleep_times[guard]:
            start_minute, end_minute = map(int, (start[4], end[4]))
            block = [1 if start_minute <= m < end_minute else 0 for m in range(60)]
            sections.append(block)
        for i in range(60):
            current_sum = 0
            for block in sections:
                current_sum += block[i]
            if current_sum > max_sleeps_count:
                max_sleeps_count = current_sum
                max_sleep = i
                max_guard = guard
    print(max_sleep * int(max_guard[1:]))


if __name__ == '__main__':
    two()

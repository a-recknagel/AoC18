from copy import deepcopy
from typing import List, Optional, Tuple

from AoC18 import read_data

test_1 = '''\
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########'''.split('\n')
test_2 = '''\
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######'''.split('\n')


class GameEndException(Exception):
    pass


class Unit:
    def __init__(self, alliance, y, x, hp=200, dmg=3):
        self.alliance: str = alliance
        self.y: int = y
        self.x: int = x
        self.hp: int = hp
        self.dmg: int = dmg

    def moves(self):
        return [(self.y-1, self.x), (self.y, self.x-1),
                (self.y, self.x+1), (self.y+1, self.x)]

    def __gt__(self, other):
        return (self.y, self.x) > (other.y, other.x)

    def __eq__(self, other):
        return (self.y, self.x) == (other.y, other.x)

    def __str__(self):
        return self.alliance

    def __repr__(self):
        return f'{self.alliance}({self.hp})'

    def __hash__(self):
        return hash((self.y, self.x))


class Map:
    ENMITIES = {'G': 'E', 'E': 'G'}

    def __init__(self, lines) -> None:
        self.turns = 0
        self.units: List[Unit] = []
        self.field: List[List[str]] = [['.'] * len(l) for l in lines]
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] == '#':
                    self.field[y][x] = '#'
                if lines[y][x] in self.ENMITIES:
                    self.units.append(Unit(lines[y][x], y, x))

    def score(self):
        return self.turns * sum(u.hp for u in self.units)

    def draw(self) -> None:
        pic = deepcopy(self.field)
        unit_map = {(u.y, u.x): u for u in self.units}
        for y in range(len(pic)):
            for x in range(len(pic[y])):
                if (y, x) in unit_map:
                    pic[y][x] = unit_map[(y, x)]
        print(f"After {self.turns} rounds:")
        for row in pic:
            print(''.join(map(str, row)), end='   ')  # map
            print(', '.join(map(repr, (u for u in row if isinstance(u, Unit)))))  # stats
        print(f"Score: {self.score()}\n")

    def shortest_path(self, source: Unit, target: Unit):
        ...

    def weight_movements(self, unit: Unit) -> Optional[Tuple[int, int]]:
        enemies: List[Unit] = [u for u in self.units if u.alliance in self.ENMITIES[unit.alliance]]
        if not enemies:
            raise GameEndException(f"No more enemies, '{unit.alliance}' have won!")
        for y, x in unit.moves():
            for enemy in enemies:
                if enemy.y == y and enemy.x == x:
                    return None  # don't move if an enemy is already in range

        blocked = {(u.y, u.x) for u in self.units}
        attack_options: List[Tuple[int, int]] = []
        for enemy in enemies:
            for o in enemy.moves():
                if self.field[o[0]][o[1]] == '.' and o not in blocked:
                    attack_options.append(o)
        attack_target, min_attack_dist = None, float('inf')
        for option in sorted(attack_options):
            dist = abs(option[0] - unit.y) + abs(option[1] - unit.x)
            if dist < min_attack_dist:
                min_attack_dist = dist
                attack_target = option
        if attack_target is None:
            return None  # don't move if no target is in range

        next_move, min_move_dist = None, float('inf')
        for move in unit.moves():
            if self.field[move[0]][move[1]] != '.' or move in blocked:
                continue
            dist = abs(move[0] - attack_target[0]) + abs(move[1] - attack_target[1])
            if dist < min_move_dist:
                min_move_dist = dist
                next_move = move
        return next_move

    def weight_attacks(self, unit: Unit) -> Optional[Unit]:
        enemies: List[Unit] = [u for u in self.units if u.alliance in self.ENMITIES[unit.alliance]]
        unit_range = {*unit.moves()}
        targets: List[Unit] = [u for u in enemies if (u.y, u.x) in unit_range]
        if targets:
            return sorted(targets, key=lambda x: x.hp)[0]
        else:
            return None

    def turn(self):
        for unit in sorted(self.units):
            try:
                move = self.weight_movements(unit)
            except GameEndException as e:
                print(e)
                return unit.alliance
            if move is not None:
                unit.y, unit.x = move
            attacks = self.weight_attacks(unit)
            if attacks is not None:
                target = attacks
                target.hp -= unit.dmg
                if target.hp <= 0:
                    self.units.remove(target)
                continue
        self.turns += 1


def one(data):
    m = Map(data)
    for t in range(48):
        m.draw()
        m.turn()
    m.draw()


def two(data):
    ...


if __name__ == '__main__':
    inp = read_data('day_14.txt')[0]
    one(test_2)
    two(inp)

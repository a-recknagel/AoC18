from AoC18 import read_data


def one(inp):

    def parse(ptr, count=0):
        num_children, num_meta = next(ptr), next(ptr)
        for _ in range(num_children):
            count += parse(ptr)
        return count + sum(next(ptr) for _ in range(num_meta))

    return parse(map(int, inp.split()))


def two(inp):

    def parse(parent, ptr):
        num_children, num_meta = next(ptr), next(ptr)
        current = {'header': (num_children, num_meta), 'meta': [], 'children': []}
        parent['children'].append(current)
        for _ in range(num_children):
            parse(current, ptr)
        for _ in range(num_meta):
            current['meta'].append(next(ptr))

    def get_val(tree):
        num_children = tree['header'][0]
        if not num_children:
            return sum(tree['meta'])
        meta_sum = 0
        for idx in tree['meta']:
            idx -= 1
            if idx >= num_children:
                continue
            meta_sum += get_val(tree['children'][idx])
        return meta_sum

    root_root = {'children': []}
    parse(root_root, map(int, inp.split()))
    return get_val(root_root['children'][0])


def two_fancy(inp):

    class Node:
        def __init__(self):
            self.meta = []
            self.children = []
            self.val_cache = None

        def val(self):
            if self.val_cache is not None:
                return self.val_cache
            if not len(self.children):
                self.val_cache = sum(self.meta)
                return self.val_cache
            self.val_cache = 0
            for idx in self.meta:
                idx -= 1  # I debugged this for > 20 minutes..
                if idx >= len(self.children):
                    continue
                self.val_cache += self.children[idx].val()
            return self.val_cache

    def parse(parent, ptr):
        num_children, num_meta = next(ptr), next(ptr)
        current = Node()
        parent.children.append(current)
        for _ in range(num_children):
            parse(current, ptr)
        for _ in range(num_meta):
            current.meta.append(next(ptr))

    root_root = Node()
    parse(root_root, map(int, inp.split()))
    return root_root.children[0].val()


if __name__ == '__main__':
    data = read_data('day_8.txt')[0]
    print(one(data))
    print(two(data))
    print(two_fancy(data))

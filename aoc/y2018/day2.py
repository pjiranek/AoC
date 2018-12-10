from aoc import utils
from collections import defaultdict


def count_letters(id):
    d = defaultdict(lambda: 0)
    for c in id:
        d[c] += 1
    return d


def checksum(ids):
    n2, n3 = 0, 0
    for id in ids:
        counts = count_letters(id)
        if 2 in counts.values(): n2 += 1
        if 3 in counts.values(): n3 += 1
    return n2 * n3


def diff(s1, s2):
    assert len(s1) == len(s2)
    d = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            d += 1
    return d


def common_letters(s1, s2):
    return ''.join(c1 for c1, c2 in zip(s1, s2) if c1 == c2)


def correct(ids):
    n = len(ids)
    for i in range(0, n):
        for j in range(i + 1, n):
            id1 = ids[i]
            id2 = ids[j]
            d = diff(id1, id2)
            if d == 1:
                return common_letters(id1, id2)


def main():
    ids = utils.read_input('input2.txt')
    print('Part 1:', checksum(ids))
    print('Part 2:', correct(ids))


if __name__ == '__main__':
    main()

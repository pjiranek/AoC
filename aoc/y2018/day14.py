from aoc import utils
from collections import deque


def chart():
    recipes = [3, 7]
    elves = [0, 1]

    yield recipes[0]
    yield recipes[1]

    while True:
        score = sum(recipes[elf] for elf in elves)
        if score > 0:
            digits = []
            while score != 0:
                digits.append(score % 10)
                score = score // 10
        else:
            digits = [0]

        for digit in reversed(digits):
            recipes.append(digit)
            yield digit

        n = len(recipes)
        for i in range(len(elves)):
            elves[i] += 1 + recipes[elves[i]]
            elves[i] %= n


def part1(s):
    n = int(s)
    result = []
    for i, recipe in enumerate(chart()):
        if i >= n:
            result.append(recipe)
        if len(result) == 10:
            break
    print(''.join(str(r) for r in result))


def part2(s):
    q = deque()
    for i, recipe in enumerate(chart()):
        q.append(recipe)
        if len(q) > len(s):
            q.popleft()
        if ''.join(str(r) for r in q) == s:
            print(i - len(s) + 1)
            break


def main():
    s = '554401'
    part1(s)
    part2(s)


if __name__ == '__main__':
    main()

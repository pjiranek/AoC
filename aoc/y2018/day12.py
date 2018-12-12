from aoc import utils
import parse


def main():
    lines = utils.read_input('input12.txt')

    initial_state = parse.compile('initial state: {}').parse(lines[0])[0]
    plants = set(i for i, c in enumerate(initial_state) if c == '#')

    patterns = set()
    parser = parse.compile("{} => {}")
    for note in lines[1:]:
        result = parser.parse(note)
        if result[1] == '#':
            patterns.add(tuple(i-2 for i, c in enumerate(result[0]) if c == '#'))

    prev_diff, curr_diff = None, None
    prev_sum, curr_sum = None, sum(plants)

    generation = 1
    while generation != 1000:
        new_plants = set()
        for pot in range(min(plants) - 2, max(plants) + 3):
            pattern = tuple(i for i in range(-2, 3) if i+pot in plants)
            if pattern in patterns:
                new_plants.add(pot)
        plants = new_plants

        if generation == 20:
            print('Part 1:', sum(plants))

        prev_sum, curr_sum = curr_sum, sum(plants)
        prev_diff, curr_diff = curr_diff, curr_sum - prev_sum

        if prev_diff == curr_diff:
            break

        generation += 1

    diff = curr_diff

    future_sum = curr_sum + diff * (50000000000 - generation)
    print('Part 2:', future_sum)


if __name__ == '__main__':
    main()

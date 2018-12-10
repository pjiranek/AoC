from aoc import utils


def final_frequency(freq_changes):
    freq = 0
    for df in freq_changes:
        freq += df
    return freq


def repeated_frequency(freq_changes):
    freq = 0
    freq_seen = set((freq, ))
    while True:
        for df in freq_changes:
            freq += df
            if freq in freq_seen:
                return freq
            else:
                freq_seen.add(freq)


def main():
    freq_changes = [int(line) for line in utils.read_input('input1.txt')]

    print('Part 1:', final_frequency(freq_changes))
    print('Part 2:', repeated_frequency(freq_changes))


if __name__ == '__main__':
    main()

import numpy as np
import re

article = None;
cost_dict = None;


def init():
    global article
    global cost_dict

    f = open('data/historyTime.txt', 'r')
    file_content = f.read().lower()
    f.close()
    regex = re.compile('[^a-zA-Z;]')
    article = regex.sub('', file_content)

    cost_dict = np.delete(np.delete(np.fromfunction(
        lambda i, j: np.sqrt(47 * 47 * np.power((i // 10 - j // 10), 2) + 77 * 77 * np.power((i % 10 - j % 10), 2)),
        (28, 28)), 20, axis=0), 20, axis=1)


def score_one(layout_string):
    key_maps = {val: i for i, val in enumerate(layout_string)}

    last_index = 15
    total_distance = 0

    for c in article:
        index = key_maps[c]
        total_distance += cost_dict[last_index][index]
        last_index = index

    if key_maps['e'] not in [15, 16, 17]:
        total_distance *= 1.03
    if abs(key_maps['t'] - key_maps['h']) > 1:
        total_distance *= 1.02
    if key_maps[';'] not in [0, 9, 10, 19]:
        total_distance *= 1.02

    return total_distance / 10000


def myprint(layout_string):
    print(' '.join(layout_string[0:10]))
    print(' '.join(layout_string[10:20]))
    print(' ', ' '.join(layout_string[20:]))


if __name__ == "__main__":
    init()
    f = open('known_solutions.txt', 'r')
    for line in f.readlines():
        regex = re.compile('[^a-zA-Z;]')
        line = regex.sub('', line)
        score = score_one(line)
        myprint(line)
        print(score)
    f.close()

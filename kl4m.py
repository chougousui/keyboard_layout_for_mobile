import numpy as np
import time
import re


WORKMAN_LAYOUT = "qdrwbjfup;ashtgyneoizxmcvkl"
QWERTY_LAYOUT = "qwertyuiopasdfghjkl;zxcvbnm"

def main():

    cost_dict = get_cost_dict()
    key_maps = get_indexes_from_string(WORKMAN_LAYOUT)

    # load article file
    f = open("data/historyTime.txt", "r")
    article = f.read().lower()
    f.close()
    regex = re.compile('[^a-zA-Z]')
    article = regex.sub('', article)

    # count
    last_index = 15
    total_distance = 0

    for c in article:
        index = key_maps[c]
        total_distance += cost_dict[last_index][index]
        last_index = index

    return total_distance


def get_indexes_from_string(key_queue):
    # create a key map dictionary to speed up char addressing
    if len(key_queue) > 27:
        print("string length not available.")

    key_position = dict()

    for c in key_queue:
        key_position[c] = key_queue.index(c)

    return key_position


def get_cost_dict():
    def inner_func(i, j):
        return np.sqrt(47 * 47 * np.power((i // 10 - j // 10), 2) + 77 * 77 * np.power((i % 10 - j % 10), 2))

    cost_dict = np.fromfunction(inner_func, (27, 27))
    return cost_dict


if __name__ == "__main__":
    start = time.time()
    result = main()
    print("distance: ", result)
    end = time.time()
    print("time cost: ", end - start)

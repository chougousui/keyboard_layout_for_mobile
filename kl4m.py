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

    # remove non alphabet chars
    regex = re.compile('[^a-zA-Z]')
    article_later = regex.sub('', article)
    article_former = WORKMAN_LAYOUT[15] + article_later[:-1]

    # index lists
    article_former_array = map(lambda x: key_maps[x], article_former)
    article_later_array = map(lambda x: key_maps[x], article_later)

    # calculate all costs and then return
    cost_array = map(lambda x, y: cost_dict[x][y], article_former_array, article_later_array)
    return sum(cost_array)

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

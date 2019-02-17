import numpy as np
import time
WORKMAN_LAYOUT = "qdrwbjfup;ashtgyneoizxmcvkl"
QWERTY_LAYOUT = "qwertyuiopasdfghjkl;zxcvbnm"


def main():
    # load article file
    f = open("data/historyTime.txt", "r")
    article = f.read().lower()
    f.close()

    cost_matrix = get_cost_matrix()

    key_indexes = get_indexes_from_string(WORKMAN_LAYOUT)

    # count
    last_index = 15
    total_distance = 0

    for c in article:
        if c in key_indexes:
            index = key_indexes[c]
            total_distance += cost_matrix[last_index][index]
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


def get_cost_matrix():
    def inner_func(i, j):
        return np.sqrt(47 * 47 * np.power((i // 10 - j // 10), 2) + 77 * 77 * np.power((i % 10 - j % 10), 2))

    cost_matrix = np.fromfunction(inner_func, (27, 27))
    return cost_matrix


if __name__ == "__main__":
    start = time.time()
    result = main()
    print("distance: ", result)
    end = time.time()
    print("time cost: ", end - start)

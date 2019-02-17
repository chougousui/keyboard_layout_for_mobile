import numpy as np
import time


def main():
    key_position = get_position_from_string("qdrwbjfup;ashtgyneoizxmcvkl")

    # load article file
    f = open("data/historyTime.txt", "r")
    article = f.read()
    f.close()
    article = article.lower()

    # count
    last_pos = [44 * 1, 77 * 5]
    total_distance = 0

    for c in article:
        if c in key_position:
            pos1 = key_position[c]
            total_distance += distance(pos1, last_pos)
            last_pos = pos1

    return total_distance


def distance(pos1, pos2):
    return np.linalg.norm(pos1 - pos2)


def get_position_from_string(key_queue):
    if len(key_queue) != 27:
        print("string length not available.")

    key_position = dict()
    for i in range(27):
        key_char = key_queue[i];
        key_position[key_char] = np.array([47 * (i // 10), 77 * (i % 10)])

    return key_position


if __name__ == "__main__":
    start = time.time()
    result = main()
    print("distance: ", result)
    end = time.time()
    print("time cost: ", end - start)

import numpy as np
import re
from tools import generate_cost_dict

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

    cost_dict = generate_cost_dict()

def score_one(layout_string):
    key_maps = {val: i for i, val in enumerate(layout_string)}

    last_index = 15
    total_distance = 0

    for c in article:
        index = key_maps[c]
        total_distance += cost_dict[last_index][index]
        last_index = index

    return total_distance / 10000

def myprint(layout_string):
    print(' '.join(layout_string[0:10]))
    print(' '.join(layout_string[10:20]))
    print(' ', ' '.join(layout_string[20:]))


if __name__ == "__main__":
    init()
    f = open('known_solutions.txt', 'r')
    lines = f.readlines()
    f.close()

    regex = re.compile('[^a-zA-Z;]')

    layouts = np.array([regex.sub('', line) for line in lines])
    scores = np.array([score_one(layout) for layout in layouts])

    layouts = layouts[np.argsort(scores)]
    scores = np.sort(scores)

    for i in range(len(scores)):
        myprint(layouts[i])
        print(scores[i])

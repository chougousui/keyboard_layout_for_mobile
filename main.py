import numpy as np
import re
import time

LIVES = 30
MAXG = 30
OLD_P = 0.1
CHANGE_P = 1.0
TEMPLATE = "abcdefghijklmnopqrstuvwxyz:"

article = None
frequencies = None
keymaps = None
cost_dict = None
all_genes = None
all_scores = None
all_probs = None


def prepare_data():
    global article
    global cost_dict
    global frequencies

    f = open('data/historyTime.txt', 'r')
    file_content = f.read().lower()
    f.close()
    regex = re.compile('[^a-zA-Z]')
    article = regex.sub('', file_content)

    word_freq = [article.count(c) for c in 'abcdefghijklmnopqrstuvwxyz:']
    word_rank = np.argsort(word_freq)[::-1]
    frequencies = np.array(list('abcdefghijklmnopqrstuvwxyz:'))[word_rank].tolist()

    def inner_func(i, j):
        return np.sqrt(47 * 47 * np.power((i // 10 - j // 10), 2) + 77 * 77 * np.power((i % 10 - j % 10), 2))

    cost_dict = np.fromfunction(inner_func, (27, 27))
    return


def init_generation():
    global all_genes

    all_genes = np.array([TEMPLATE] * LIVES)
    for i in range(LIVES):
        indexes = np.random.permutation(27)
        life = ''.join([TEMPLATE[x] for x in indexes])
        all_genes[i] = life
    return


def score_one(layout_string):
    key_maps = dict()

    for c in layout_string:
        key_maps[c] = layout_string.index(c)

    last_index = 15
    total_distance = 0

    for c in article:
        index = key_maps[c]
        total_distance += cost_dict[last_index][index]
        last_index = index

    return total_distance / 10000


def get_probabilities():
    global all_probs
    global all_scores

    all_scores = np.array([score_one(x) for x in all_genes])
    scores = all_scores - all_scores.min() * 0.9
    scores = 1 / scores
    total_scores = sum(scores)
    all_probs = np.array([x / total_scores for x in scores])

    return


def cross_one(father, mother):
    father = np.array(list(father))
    mother = np.array(list(mother))
    child = np.array(['']*27)
    cross_length = 9
    high_set = frequencies[:cross_length]
    low_set = frequencies[cross_length:]
    high_index = [i for i, val in enumerate(father) if val in high_set]
    low_index = [i for i, val in enumerate(mother) if val in low_set]
    child[high_index] = father[high_index]
    child[low_index] = mother[low_index]
    left_list = np.array([i for i in TEMPLATE if i not in child])
    space_index = [i for i, val in enumerate(child) if val == '']
    child[space_index] = left_list

    return ''.join(child)


def change_one(before):
    temp_list = list(before)
    indexes = np.random.choice(np.arange(27), 2)
    temp_list[indexes[0]], temp_list[indexes[1]] = temp_list[indexes[1]], temp_list[indexes[0]]
    indexes = np.random.choice(np.arange(27), 2)
    temp_list[indexes[0]], temp_list[indexes[1]] = temp_list[indexes[1]], temp_list[indexes[0]]
    return ''.join(temp_list)


def rws():
    number_sum = 0
    temp = np.random.random()
    for i in range(len(all_probs)):
        number_sum += all_probs[i]
        if number_sum > temp:
            return i


def generate_new():
    global all_genes

    crosses = []

    top_excellent_index = np.argsort(all_probs)[::-1][:int(OLD_P * LIVES)]
    retains = all_genes[top_excellent_index]

    for i in range(LIVES - len(retains)):
        father = all_genes[rws()]
        mother = all_genes[rws()]
        child = cross_one(father, mother)
        crosses.append(child)
    crosses = np.array(crosses)

    for index in range(len(crosses)):
        if np.random.random() < CHANGE_P:
            crosses[index] = change_one(crosses[index])

    all_genes = np.append(retains, crosses)
    return


def ga():
    prepare_data()
    init_generation()
    print('inited')

    for i in range(MAXG):
        get_probabilities()

        best = all_genes[np.argmax(all_probs)]
        print('the %s th time: %s %s' % (i, best, score_one(best)))
        generate_new()
    get_probabilities()

    return


if __name__ == "__main__":
    start = time.time()
    ga()
    print(all_genes)
    end = time.time()
    print('time cost: %s' % (end - start))

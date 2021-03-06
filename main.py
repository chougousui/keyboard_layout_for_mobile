import numpy as np
import re
import time
import multiprocessing
import sys

REPRODUCTION_RATE = 0.1
MUTATION_RATE = 0.9
TEMPLATE = ";abcdefghijklmnopqrstuvwxyz"

population = 50
iteration_limit = 50
article = None
frequencies = None
cost_dict = None
genotypes = None
scores = None
probabilities = None
cores = 1
pool = None


def prepare_data():
    global population
    global iteration_limit
    global article
    global cost_dict
    global frequencies
    global cores
    global pool

    f = open('data/historyTime.txt', 'r')
    file_content = f.read().lower()
    f.close()
    regex = re.compile('[^a-zA-Z]')
    article = regex.sub('', file_content)

    word_freq = [article.count(c) for c in TEMPLATE]
    word_rank = np.argsort(word_freq)[::-1]
    frequencies = np.array(list(TEMPLATE))[word_rank].tolist()

    cost_dict = np.delete(np.delete(np.fromfunction(
        lambda i, j: np.sqrt(47 * 47 * np.power((i // 10 - j // 10), 2) + 77 * 77 * np.power((i % 10 - j % 10), 2)),
        (28, 28)), 20, axis=0), 20, axis=1)

    cores = multiprocessing.cpu_count() - 1
    pool = multiprocessing.Pool(processes=cores)

    if len(sys.argv) > 1:
        population = int(sys.argv[1])
        iteration_limit = int(sys.argv[2])

    return


def init_generation():
    global genotypes

    genotypes = np.array([TEMPLATE] * population)
    for i in range(population):
        indexes = np.random.permutation(27)
        life = ''.join([TEMPLATE[x] for x in indexes])
        genotypes[i] = life
    return


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

    return total_distance / 10000


def get_probabilities():
    global probabilities
    global scores

    scores = np.array(list(pool.map(score_one, genotypes)))
    adjusted_scores = scores - scores.min() * 0.9
    adjusted_scores = 1 / adjusted_scores
    total_scores = sum(adjusted_scores)
    probabilities = np.array([x / total_scores for x in adjusted_scores])

    return


def crossover_one(father, mother):
    father = np.array(list(father))
    mother = np.array(list(mother))
    child = np.array(['']*27)
    cross_length = np.random.randint(26) + 1
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


def mutation_one(before):
    temp_list = list(before)
    indexes = np.random.choice(np.arange(27), 2)
    temp_list[indexes[0]], temp_list[indexes[1]] = temp_list[indexes[1]], temp_list[indexes[0]]
    indexes = np.random.choice(np.arange(27), 2)
    temp_list[indexes[0]], temp_list[indexes[1]] = temp_list[indexes[1]], temp_list[indexes[0]]
    return ''.join(temp_list)


def rws():
    number_sum = 0
    temp = np.random.random()
    for i in range(len(probabilities)):
        number_sum += probabilities[i]
        if number_sum > temp:
            return i


def generate_new():
    global genotypes

    crosses = []

    top_excellent_index = np.argsort(probabilities)[::-1][:int(REPRODUCTION_RATE * population)]
    retains = genotypes[top_excellent_index]

    for i in range(population - len(retains)):
        father = genotypes[rws()]
        mother = genotypes[rws()]
        child = crossover_one(father, mother)
        crosses.append(child)
    crosses = np.array(crosses)

    for index in range(len(crosses)):
        if np.random.random() < MUTATION_RATE:
            crosses[index] = mutation_one(crosses[index])

    genotypes = np.append(retains, crosses)
    if (len(np.unique(genotypes))< population / 10):
        raise KeyboardInterrupt
    return


def ga():
    prepare_data()
    init_generation()
    print('inited')

    for i in range(iteration_limit):
        get_probabilities()

        best = genotypes[np.argmax(probabilities)]
        print('the %s th time: %s %s' % (i, best, score_one(best)))
        generate_new()
    get_probabilities()

    return


if __name__ == "__main__":
    start = time.time()

    try:
        ga()
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        print(genotypes)

    end = time.time()

    print('time cost: %s' % (end - start))

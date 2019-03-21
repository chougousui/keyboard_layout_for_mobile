import numpy as np
import re
import multiprocessing as mp
import time
import factoradic
import bisect
import sys

TEMPLATE = ":abcdefghijklmnopqrstuvwxyz"


class GA:
    def __init__(self, count):
        self.count = count
        self.population = self.gen_population(count)

        f = open('data/historyTime.txt', 'r')
        file_content = f.read().lower()
        f.close()
        regex = re.compile('[^a-zA-Z:]')
        self.article = regex.sub('', file_content)

        self.cost_dict = np.delete(np.delete(np.fromfunction(
            lambda i, j: np.sqrt(47 * 47 * np.power((i // 10 - j // 10), 2) + 77 * 77 * np.power((i % 10 - j % 10), 2)),
            (28, 28)), 20, axis=0), 20, axis=1)

        word_freq = [self.article.count(c) for c in ':abcdefghijklmnopqrstuvwxyz']
        word_rank = np.argsort(word_freq)[::-1]
        self.frequencies = np.array(list(':abcdefghijklmnopqrstuvwxyz'))[word_rank].tolist()

        self.probabilities = None

        cores = mp.cpu_count() - 1
        self.pool = mp.Pool(processes=cores)

    def gen_population(self, count):
        return np.array([self.gen_chromosome() for i in range(count)])

    def gen_chromosome(self):
        indexes = np.random.permutation(27)
        return ''.join([TEMPLATE[x] for x in indexes])

    def evolve(self, retain_rate=0.2, mutation_rate=0.1):
        parents = self.selection(retain_rate)
        best = self.population[np.argmax(self.probabilities)]
        print('the %s th time: %s %s' % (i, best, self.score_one(best)))

        self.crossover(parents)
        self.mutation(mutation_rate)

    def score_one(self, layout_string):
        key_maps = {val: i for i, val in enumerate(layout_string)}

        last_index = 15
        total_distance = 0

        for c in self.article:
            index = key_maps[c]
            total_distance += self.cost_dict[last_index][index]
            last_index = index

        if key_maps['e'] not in [15, 16, 17]:
            total_distance *= 1.03
        if abs(key_maps['t'] - key_maps['h']) > 1:
            total_distance *= 1.02
        if key_maps[':'] not in [0,9,10,19]:
            total_distance *= 1.02

        return total_distance / 10000

    def selection(self, reproduction_rate):
        parents = []
        scores = np.array(list(self.pool.map(self.score_one, self.population)))
        for i in range(int(reproduction_rate * self.count)):
            index = np.random.randint(0, self.count, size=int(self.count/10.0))
            _, winner = min(zip(scores[index], self.population[index]))
            parents.append(winner)
        return np.array(parents)

    def crossover_one(self, father, mother):
        father = np.array(list(father))
        mother = np.array(list(mother))
        child = np.array([''] * 27)
        cross_length = np.random.randint(26) + 1
        high_set = self.frequencies[:cross_length]
        low_set = self.frequencies[cross_length:]
        high_index = [i for i, val in enumerate(father) if val in high_set]
        low_index = [i for i, val in enumerate(mother) if val in low_set]
        child[high_index] = father[high_index]
        child[low_index] = mother[low_index]
        left_list = np.array([i for i in TEMPLATE if i not in child])
        space_index = [i for i, val in enumerate(child) if val == '']
        child[space_index] = left_list

        return ''.join(child)

    def crossover(self, parents):
        children = []
        for i in range(self.count - len(parents)):
            father = np.random.choice(parents)
            mother = np.random.choice(parents)
            child = self.crossover_one(father, mother)
            children.append(child)
        self.population = np.append(parents, children)

    def mutation_one(self, layout_string):
        temp_list = list(layout_string)
        indexes = np.random.choice(np.arange(27), 2)
        temp_list[indexes[0]], temp_list[indexes[1]] = temp_list[indexes[1]], temp_list[indexes[0]]
        indexes = np.random.choice(np.arange(27), 2)
        temp_list[indexes[0]], temp_list[indexes[1]] = temp_list[indexes[1]], temp_list[indexes[0]]
        return ''.join(temp_list)

    def mutation(self, rate):
        for index in range(self.count):
            if np.random.random() < rate:
                self.population[index] = self.mutation_one(self.population[index])

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)

    # def coding(self, layout_string):
    #     new_strings = list(layout_string)[::-1]
    #     temp = []
    #     return factoradic.from_factoradic([bisect.insort(temp, c) or temp.index(c) for c in new_strings])
    #
    # def decoding(self, chromosome):
    #     new_numbers = (factoradic.to_factoradic(number) + [0] * 27)[:27][::-1]
    #     temp = list(TEMPLATE)
    #     return [temp.pop(i) for i in new_numbers]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
        iteration_limit = int(sys.argv[2])
    else:
        count = 50
        iteration_limit = 50

    start = time.time()

    try:
        ga = GA(count)
        for i in range(iteration_limit):
            ga.evolve()
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        print(ga.population)

    end = time.time()

    print('time cost: %s' % (end - start))

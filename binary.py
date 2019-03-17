# encoding: utf-8
import numpy as np
import re
import multiprocessing as mp
import time
import factoradic
import bisect
import sys
import random

TEMPLATE = ":abcdefghijklmnopqrstuvwxyz"
MAX = np.math.factorial(27)

class GA:
    def __init__(self, count):
        self.count = count
        self.population = self.gen_population(count)

        f = open('data/historyTime.txt', 'r')
        file_content = f.read().lower()
        f.close()
        regex = re.compile('[^a-zA-Z:]')
        self.article = regex.sub('', file_content)

        self.cost_dict = np.fromfunction(
            lambda i, j: np.sqrt(47 * 47 * np.power((i // 10 - j // 10), 2) + 77 * 77 * np.power((i % 10 - j % 10), 2)),
            (27, 27))

        self.probabilities = None

        cores = mp.cpu_count() - 1
        self.pool = mp.Pool(processes=cores)

    def gen_population(self, count):
        return np.array([self.gen_chromosome() for i in range(count)])

    def gen_chromosome(self):
        chromosome = 0
        for i in range(94):
            chromosome |= (1 << i) * random.randint(0, 1)
        return chromosome

    def evolve(self, retain_rate=0.2, mutation_rate=0.1):
        parents = self.selection(retain_rate)
        best = self.population[np.argmax(self.probabilities)]
        print('the %s th time: %s %s' % (i, self.decoding(best), self.score_one(best)))

        self.crossover(parents)
        self.mutation(mutation_rate)

    def score_one(self, chromosome):
        if chromosome >= MAX:
            return 8000
        else:
            layout_string = self.decoding(chromosome)
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
        scores = np.array(list(self.pool.map(self.score_one, self.population)))
        adjusted_scores = scores - scores.min() * 0.9
        adjusted_scores = 1 / adjusted_scores
        total_scores = sum(adjusted_scores)
        self.probabilities = np.array([x / total_scores for x in adjusted_scores])

        top_excellent_index = np.argsort(self.probabilities)[::-1][:int(reproduction_rate * self.count)]
        parents = self.population[top_excellent_index]

        return parents

    def rws(self):
        number_sum = 0
        temp = np.random.random()
        for i in range(len(self.probabilities)):
            number_sum += self.probabilities[i]
            if number_sum >= temp:
                return i

    def crossover_one(self, father, mother):
        cross_pos = random.randint(0, 94)
        # 生成掩码，方便位操作
        mask = 0
        for i in range(cross_pos):
            mask |= (1 << i)
            # 孩子将获得父亲在交叉点前的基因和母亲在交叉点后（包括交叉点）的基因
        child = ((father & mask) | (mother & ~mask)) & ((1 << 94) - 1)

        return child

    def crossover(self, parents):
        children = []
        for i in range(self.count - len(parents)):
            father = self.population[self.rws()]
            mother = self.population[self.rws()]
            child = self.crossover_one(father, mother)
            children.append(child)
        self.population = np.append(parents, children)

    def mutation_one(self, chromosome):
        j = random.randint(0, 94-1)
        new = chromosome ^ 1 << j
        return new

    def mutation(self, rate):
        for index in range(5, self.count):
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

    def decoding(self, chromosome):
        if chromosome >= MAX:
            return TEMPLATE
        else:
            new_numbers = (factoradic.to_factoradic(chromosome) + [0] * 27)[:27][::-1]
            temp = list(TEMPLATE)
            return "".join([temp.pop(i) for i in new_numbers])


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

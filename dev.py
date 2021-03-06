import numpy as np
import re
import multiprocessing as mp
import time
import factoradic
import bisect
import sys
import collections
from tools import generate_cost_dict

TEMPLATE = ";abcdefghijklmnopqrstuvwxyz"


class GA:
    def __init__(self, count):
        self.count = count
        self.population = self.gen_population(count)

        f = open('data/historyTime.txt', 'r')
        file_content = f.read().lower()
        f.close()
        regex = re.compile('[^a-zA-Z;]')
        self.article = regex.sub('', file_content)

        self.cost_dict = generate_cost_dict()

        word_freq = [self.article.count(c) for c in TEMPLATE]
        word_rank = np.argsort(word_freq)[::-1]
        self.frequencies = np.array(list(TEMPLATE))[word_rank].tolist()

        self.scores = None

        cores = mp.cpu_count() - 1
        self.pool = mp.Pool(processes=cores)

        self.cheat_sheet = collections.deque(maxlen=count)

    def gen_population(self, count):
        return np.array([self.gen_chromosome() for i in range(count)])

    def gen_chromosome(self):
        # 0) Randomly initialize each individual, using string encoding directly
        indexes = np.random.permutation(27)
        return ''.join([TEMPLATE[x] for x in indexes])

    def evolve(self, retain_rate=0.05, select_rate = 0.15, mutation_rate=0.1):
        parents = self.selection(retain_rate, select_rate)

        # Show the best individuals at present
        best = self.population[np.argmin(self.scores)]
        print('the', i, 'th time: ', best, self.score_one(best), len(np.unique(self.population)), '/', self.count)

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

        # if abs(key_maps['t'] - key_maps['h']) > 1:
        #     total_distance *= 1.02

        return total_distance / 10000

    def score_one_out(self, layout_string):
        if layout_string in dict(self.cheat_sheet):
            return dict(self.cheat_sheet)[layout_string]
        else :
            score = self.score_one(layout_string)
            self.cheat_sheet.append([layout_string,score])
            return score

    def selection(self, reproduction_rate, select_rate):
        # 1) Calculate the score of each individual
        self.scores = np.array(list(self.pool.map(self.score_one_out, self.population)))

        # 2) Keep some of the best individuals as parents
        top_excellent_index = np.argsort(self.scores)[:int(self.count * reproduction_rate)]
        parents = self.population[top_excellent_index]

        # 3) The rest are selected using the tournament operator
        #    until the parents reaches the set percentage
        for i in range(int(select_rate * self.count)):
            index = np.random.randint(0, self.count, size=5)
            _, winner = min(zip(self.scores[index], self.population[index]))
            parents = np.append(parents, winner)
        return np.array(parents)

    def crossover_one(self, father, mother):
        father = np.array(list(father))
        mother = np.array(list(mother))
        child = np.array([''] * 27)

        # Randomly choose intersections
        cross_length = np.random.randint(26) + 1
        high_set = self.frequencies[:cross_length]
        low_set = self.frequencies[cross_length:]
        high_index = [i for i, val in enumerate(father) if val in high_set]
        low_index = [i for i, val in enumerate(mother) if val in low_set]

        # Keep father's high frequency characters and mother's low frequency characters
        child[high_index] = father[high_index]
        child[low_index] = mother[low_index]

        # Supplement the missing characters due to parental character repetition
        left_list = np.array([i for i in TEMPLATE if i not in child])
        space_index = [i for i, val in enumerate(child) if val == '']
        child[space_index] = left_list

        return ''.join(child)

    def crossover(self, parents):
        # 4) Use crossover operators to generate new children,
        #    until the new population reaches the size of the old population
        children = []
        unique_parent = np.unique(parents)
        if len(unique_parent) == 1:
            raise KeyboardInterrupt
        while len(children) < (self.count - len(parents)):
            father,mother = np.random.choice(unique_parent,2,replace=False)
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
        # 5) For these crossover-generated individuals,
        #    using mutation operators to modify their genes
        for index in range(int(self.count * 0.2), self.count):
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
        print (np.unique(ga.population))
        end = time.time()
        print('time cost: %s' % (end - start))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Find the global maximum for function: f(x) = x + 10sin(5x) + 7cos(4x)
'''


from gaft import GAEngine
from gaft.components import BinaryIndividual
from gaft.components import Population
from gaft.operators import TournamentSelection
from gaft.operators import UniformCrossover
from gaft.operators import FlipBitMutation
import numpy as np
import re
from gaft.plugin_interfaces.analysis import OnTheFlyAnalysis
from gaft.analysis.fitness_store import FitnessStore
from decodeandencode import seq2list

MAX = np.math.factorial(27)

f = open('data/historyTime.txt', 'r')
file_content = f.read().lower()
f.close()
regex = re.compile('[^a-zA-Z]')
article = regex.sub('', file_content)

cost_dict = np.fromfunction(
    lambda i, j: np.sqrt(47 * 47 * np.power((i // 10 - j // 10), 2) + 77 * 77 * np.power((i % 10 - j % 10), 2)),
    (27, 27))

# Define population.
indv_template = BinaryIndividual(ranges=[(0,MAX)], eps=1.0)
population = Population(indv_template=indv_template, size=100).init()

# Create genetic operators.
selection = TournamentSelection()
crossover = UniformCrossover(pc=0.8, pe=0.5)
mutation = FlipBitMutation(pm=0.1)

# Create genetic algorithm engine.
engine = GAEngine(population=population, selection=selection,
                  crossover=crossover, mutation=mutation,
                  analysis=[FitnessStore])


# Define fitness function.
@engine.fitness_register
def fitness(indv):
    x, = indv.solution
    x = round(x)
    if x >= MAX:
        return 0
    layout_string = seq2list(x)

    key_maps = dict()

    for c in layout_string:
        key_maps[c] = layout_string.index(c)

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

    return float(100000000 / total_distance)


# Define on-the-fly analysis.
@engine.analysis_register
class ConsoleOutputAnalysis(OnTheFlyAnalysis):
    interval = 1
    master_only = True

    def register_step(self, g, population, engine):
        best_indv = population.best_indv(engine.fitness)
        msg = 'Generation: {}, best fitness: {:.3f}'.format(g, engine.ori_fmax)
        self.logger.info(msg)

    def finalize(self, population, engine):
        best_indv = population.best_indv(engine.fitness)
        x, = best_indv.solution
        result = "".join(seq2list(round(x)))
        y = engine.ori_fmax
        msg = 'Optimal solution: ({}, {})'.format(result, y)
        self.logger.info(msg)


if '__main__' == __name__:
    # Run the GA engine.
    engine.run(ng=100)

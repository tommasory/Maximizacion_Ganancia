import numpy as np
from productmix import ProductMix

class Solution:
    
    def __init__(self, p: ProductMix):
        self.problem = p
        self.cells = np.zeros(self.problem.size, int)
        self.fitness = 0.0

    def from_solution(self, origin):
        self.problem = origin.problem
        self.cells = np.copy(origin.cells)
        self.fitness = origin.fitness

    def evaluate(self):
        self.fitness = self.problem.evaluate(self.cells)

    def check_restrictions(self, elements):
        if self.problem.check_restrictions(elements):
          self.cells = elements
        else:
          elements = np.random.randint(self.problem.low, self.problem.high, size=self.problem.size)
          self.check_restrictions(elements)

    def randomInitialization(self):
        elements = np.random.randint(self.problem.low, self.problem.high, size=self.problem.size)
        self.check_restrictions(elements)
        self.evaluate()

    def tweak(self):
        pos = np.random.choice(self.problem.size, 1)
        aux = self.cells.copy()
        aux[pos] = aux[pos] + self.problem.tweak
        if self.problem.check_restrictions(aux):
            self.cells[pos] = self.cells[pos] + self.problem.tweak
            self.evaluate()

    def __str__(self):
        result = "Cells:" + str(self.cells) + \
                 "-fitness:" + str(self.fitness)
        return result
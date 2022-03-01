import numpy as np
from solution import Solution
from productmix import ProductMix

class Genetic:
    def __init__(self, problem: ProductMix, pars):
        self.problem = problem
        self.max_iterations = pars[[x[0] for x in pars].index('max_iterations')][1]
        self.population_size = pars[[x[0] for x in pars].index('population_size')][1]
        self.competition_group_size = pars[[x[0] for x in pars].index('competition_group_size')][1]
        self.mutation_probability = pars[[x[0] for x in pars].index('mutation_probability')][1]

    def evolve(self):
        self.best = Solution(self.problem)
        x = np.arange(0, self.max_iterations)
        y = np.zeros(self.max_iterations, float)
        counter = 0

        population = []
        for p in range(self.population_size):
            sol = Solution(self.problem)
            sol.randomInitialization()
            if p == 0:
                self.best.from_solution(sol)
            else:
                if sol.fitness > self.best.fitness:
                    self.best.from_solution(sol)
            y[counter] = self.best.fitness
            counter += 1
            population.append(sol)

        max_generations = int(self.max_iterations / self.population_size)

        for generation in range(1, max_generations):
            offspring = []

            for s in range(round(self.population_size / 2)):
                options = np.random.choice(self.population_size, size=self.competition_group_size + 1, replace=False)
                p1 = options[0]
                p2 = self.restricted_group_competition(population, options)

                song1,song2 = self.crossover(population[p1], population[p2])
                songs = [song1, song2]

                for i in range(2):
                    if np.random.uniform() < self.mutation_probability:
                        songs[i].tweak()
                    else:
                        songs[i].evaluate()
                        
                    if songs[i].fitness > self.best.fitness:
                        self.best.from_solution(songs[i])

                    y[counter] = self.best.fitness
                    counter += 1

                offspring += songs

            population += offspring
            population.sort(reverse=True, key=lambda x: x.fitness)
            del population[self.population_size: self.population_size + self.population_size]

        return [x, y]

    def crossover(self, p1: Solution, p2: Solution):
      song1 = Solution(self.problem)
      song2 = Solution(self.problem)
      song1.from_solution(p1)
      song2.from_solution(p2)
      point = np.random.randint(p1.problem.size - 1, size=1, dtype=int)[0]
      song1.cells[0:point + 1] = p1.cells[0:point + 1]
      song1.cells[point + 1:] = p2.cells[point + 1:]

      song2.cells[0:point + 1] = p2.cells[0:point + 1]
      song2.cells[point + 1:] = p1.cells[point + 1:]

      if self.problem.check_restrictions(song1.cells) == False:
        song1.from_solution(p1)

      if self.problem.check_restrictions(song2.cells) == False:
        song2.from_solution(p2)

      return song1, song2

    @staticmethod
    def restricted_group_competition(population, options):
        p1 = population[options[0]].cells
        pos_min = options[1]
        min_sim = 0
        for i in range(1, len(options)):
            c2 = population[options[i]].cells
            sim_hamming = np.equal(p1, c2).sum()
            if i == 1:
                min_sim = sim_hamming
            else:
                if sim_hamming < min_sim:
                    pos_min = options[i]
                    min_sim = sim_hamming
        return pos_min

    def __str__(self):
        result = "\nGenetic-population_size:" + str(self.population_size) + \
                 "\ncompetition_group_size:" + str(self.competition_group_size) + \
                 "\nmutation_probability:" + str(self.mutation_probability) + '\n'
        return result
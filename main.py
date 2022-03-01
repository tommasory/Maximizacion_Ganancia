import numpy as np
import matplotlib.pyplot as plt
from genetic import Genetic
from productmix import ProductMix


dir_data = 'problema.txt'

if __name__ == '__main__':
    maxRepetitions = 31
    maxIterations = 1000
    myProblem = ProductMix(dir_data)

    my_genetic = Genetic(myProblem, [['max_iterations', maxIterations], ['population_size', 20],['competition_group_size', 6], ['mutation_probability', 0.05]])

    best = np.zeros(maxRepetitions, dtype=float)
    avgX = np.arange(0, maxIterations)
    avgY = np.zeros(maxIterations, float)
    best_list = []
    for i in range(maxRepetitions):
        np.random.seed(i*100)
        [x, y] = my_genetic.evolve()
        best[i] = my_genetic.best.fitness
        best_list.append([my_genetic.best.cells,my_genetic.best.fitness])
        avgY = avgY + y

    print(str(my_genetic) + 'AVG = ', best.mean(), ' +/- ', best.std(), ' MAX = ', best.max(), ' MIN =  ', best.min())

    # plotting
    avgY = avgY / maxRepetitions
    plt.title("Average convergence curve")
    plt.xlabel("Iteration")
    plt.ylabel("Fitness")
    plt.plot(avgX, avgY, 'o', color="red")
    plt.legend(str(my_genetic))
    plt.show()

    fig1, ax1 = plt.subplots()
    ax1.set_title('Box Plot for best solutions')
    ax1.boxplot(best)
    plt.legend(str(my_genetic))
    plt.show()
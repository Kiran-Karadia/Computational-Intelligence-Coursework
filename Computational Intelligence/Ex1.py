from functools import reduce
from random import randint, random
from operator import add
import matplotlib.pyplot as plt


def individual(length, min, max):
    # Create a member of the population #
    return [randint(min, max) for x in range(length)]


def population(count, length, min, max):
    # Create a number of individuals (i.e. a population)

    # count:    The number of individuals in a population
    # length:   The number of values per individual
    # min:      The minimum possible value in an individual's list of values
    # max:      The maximum possible value in an individual's list of values
    return [individual(length, min, max) for x in range(count)]


def fitness(individual, target):
    # Determine the fitness of an individual. Higher is better #

    # individual:   The individual to evaluate
    # target:       The target number individuals are ariming for

    fitness = abs(target - individual[0])

    return abs(target - individual[0])


def grade(pop, target):
    # Find average fitness for a population #

    summed = reduce(add, (fitness(x, target) for x in pop))
    return summed / (len(pop) * 1.0)


def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [(fitness(x, target), x) for x in pop]
    graded = [x[1] for x in sorted(graded)]
    retain_length = int(len(graded) * retain)
    parents = graded[:retain_length]

    # randomly add other individuals to promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)

    # mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual) - 1)
            # this mutation is not ideal, because it
            # restricts the range of possible values,
            # but the function is unaware of the min/max
            # values used to create the individuals,
            individual[pos_to_mutate] = randint(
                min(individual), max(individual))

    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length - 1)
        female = randint(0, parents_length - 1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = len(male) / 2
            child = male[:int(half)] + female[int(half):]
            children.append(child)

    parents.extend(children)
    return parents


# Example usage
p_count = 100
i_length = 1
i_min = -100
i_max = 100
generations = 500

found = 0
for k in range(1):
    target = randint(-50, 50)
    p = population(p_count, i_length, i_min, i_max)
    fitness_history = [grade(p, target), ]
    for i in range(generations):
        p = evolve(p, target)
        fitness_history.append(grade(p, target))
        graded = [(fitness(x, target), x) for x in p]
        graded = [x for x in sorted(graded)]
        if fitness_history[i] == 0:
            print(p)
            found += 1
            break
    #print("The target was " + str(target) + " and " + str(graded[0][1]) + " was found.")
print(found)

plt.plot(fitness_history)
plt.show()




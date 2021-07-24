from functools import reduce
from random import randint, random
from operator import add
import numpy as np
import math
import matplotlib.pyplot as plt


def individual(length, min, max):
    # Randomly choose a number between min and max
    # Loop length number of times
    return [randint(min, max) for x in range(length)]


def population(count, length, min, max):
    # Create the population

    # count:    The number of individuals in a population
    # length:   The number of values per individual
    # min:      The minimum possible value in an individual's list of values
    # max:      The maximum possible value in an individual's list of values
    return [individual(length, min, max) for x in range(count)]


def fitness(individual, target):
    # Determine the fitness of an individual. Lower is better

    # individual:   The individual to evaluate
    # target:       The target number individuals are aiming for

    # Convert target and individual to decimal and find the difference
    return abs(bin2dec(target)-bin2dec(individual))


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


def bin2dec(x):
    # Convert two's complement binary number to integer
    val = 0
    # Check if binary value is negative
    if x[0] == '1' or x[0] == 1:
        # First value is negative
        val = -(2**(len(x)-1))
    # Loop through bits and multiply by 2^n (n is index) then increment val
    for i in range(1, len(x)):
        val = val + (int(x[i]) * 2**(len(x)-1-i))
    return val


def dec2bin(x):
    # Convert decimal number to two's complement binary
    if target != 0:
        return np.binary_repr(x, math.ceil(math.log2(abs(x))+2))
    else:
        # Cannot do log(0) so set manually to 0
        return [0]


p_count = 200
generations = 200
i_min = 0   # Binary min value is 0
i_max = 1   # Binary max value is 1

target = randint(-1000, 1000)
target = dec2bin(target)
# Length of individual is equal to number of bits of target
i_length = len(target)
p = population(p_count, i_length, i_min, i_max)
fitness_history = [grade(p, target), ]
for i in range(generations):
    p = evolve(p, target)
    fitness_history.append(grade(p, target))
    if fitness_history[i+1] == 0:
        print("The target was found in " + str(i+1) + " iterations.")
        break

#for datum in fitness_history:
#    print(datum)

plt.plot(fitness_history)
plt.show()


####### Ex1 using binary representation
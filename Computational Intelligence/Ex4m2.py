import numpy as np
import math
import matplotlib.pyplot as plt
from random import randint, random


def create_individual(length, min, max):
    return [randint(min, max) for i in range(length)]


def create_population(popSize, length, min, max):
    return [create_individual(length, min, max) for i in range(popSize)]


def fitness(target, individual):
    # Get fitness of current individual
    a = bin2dec(target)
    b = bin2dec(individual)
    diff = abs(a-b)
    # Lower is better
    return diff


def make_roulette_wheel(rankedPop):
    # Get the total sum of fitness for the population
    sumFitness = sum([x[0] for x in rankedPop])
    wheel = []

    if sumFitness == 0:
        # Every individual is a correct solution, return wheel of one individual
        wheel.append(rankedPop[0][1])
        return wheel

    # Calculate the percentage of the wheel each individual should take up
    allFitness = [math.ceil((rankedPop[i][0] / sumFitness) * 100) for i in range(len(rankedPop))]
    # Reverse as we want to minimise the fitness function
    allFitness = sorted(allFitness, reverse=True)

    wheel = []
    # Create wheel - Array of 100 elements, each individual repeated depending on fitness
    for i in range(len(allFitness)):
        # Add current individual and repeat according to percentage calculated
        for j in range(allFitness[i]):
            wheel.append(rankedPop[i][1])
    return wheel


def spin_wheel(wheel):
    # Random number (spin the wheel)
    x = randint(0, len(wheel) - 1)
    # Parent is the random index within the wheel
    parent = wheel[x]
    return parent


def random_mutate(child):
    # Set a 10% chance a random bit is changed
    mutate = random()
    if mutate < 0.01:
        # Random bit within the child
        mutateBit = randint(0, len(child)-1)
        # Flip the bit
        if child[mutateBit] == 0:
            child[mutateBit] = 1
        else:
            child[mutateBit] = 0
    return child


def rank_population(population):
    # Rank the population in order of fitness (lower fitness is better)
    fitnessPop = []
    for i in range(len(population)):
        fitnessPop.append((fitness(target, population[i]), population[i]))
    return sorted(fitnessPop)


def evolve(population):
    # Get the population in ranked order
    rankedPop = rank_population(population)
    # Create the wheel
    wheel = make_roulette_wheel(rankedPop)

    children = []

    # Choose top 20% from existing population
    for i in range(int(0.2*len(population))):
        children.append(rankedPop[i][1])

    # Fill the rest of the population
    # Choose a father and mother from wheel
    # Child is first half of father and second half of mother
    while len(children) < len(population):
        father = spin_wheel(wheel)
        mother = spin_wheel(wheel)
        splitPoint = len(father) / 2
        child = father[:int(splitPoint)] + mother[int(splitPoint):]
        child = random_mutate(child)
        children.append(child)

    return children


def grade_population(population, target):
    # Get average fitness of current population
    grade = 0
    for i in range(len(population)):
        grade = grade + fitness(target, population[i])
    return grade / len(population)


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


targets = [25, 18, 31, -14, 7, -19]
popSize = 200
iMin = 0
iMax = 1
generations = 200
found = 0

for k in range(1000):
    history = []
    # Create array to hold solution
    solution = []
    for i in range(len(targets)):
        solution.append('N/A')
    # Loop through each coefficient in targets
    for i in range(len(targets)):
        # Get current coefficient and set as the target
        target = targets[i]
        # Convert to binary representation
        target = dec2bin(target)
        # Individuals have the same number of bits
        iLength = len(targets)
        p = create_population(popSize, iLength, iMin, iMax)
        history.append(grade_population(p, target))
        for g in range(generations):
            p = evolve(p)
            history.append(grade_population(p, target))
            # Check if solution has already been reached
            if history[g+1] == 0:
                # Add individual to the solution
                solution[i] = bin2dec(p[0])
                break
    if targets == solution:
        found += 1

print(found)
print(solution)

#plt.plot(history)
#plt.show()

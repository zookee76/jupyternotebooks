import random
import numpy as np
import math

# population -> fitness -> selection -> crossover -> mutation

# 1. initialize a population of binary bitstrings with random values 
# 2. decode the binary bitstrings into real values and then evaluate the fitness (objective function) of each individual
# 3. select the best individuals from population using tournament selection
# 4. create new offsprings form the selected individuals using crossover then apply mutation
# 5. repeat 2-5 until criteria is met

# objective function is gaussian function centered at 7,9

"""

notes:

a bit string is a continuous string/array where all values are concatenated together, 
we then use the formula i * n_bits and (i * n_bits) + n_bits to extract the substring from the bitstring



"""

def fitness(x):
    y = math.exp(((x[0]-7)**2 + (x[1]-9)**2)/2)
    return y 

def decode(bounds, n_bits, bitstring):

    """
    bounds: list of tuples containing the lower and upper bounds for each variable
    n_bits: number of bits for each variable
    bitstring: binary string to decode
    """

    decoded = []
    largest = 2**n_bits # needed to rescale the decoded values to bounds
    for i in range(len(bounds)):
        start, end = i*n_bits, (i*n_bits)+n_bits #define start and end indices of the substring
        substring = bitstring[start:end] #extract the substring

        chars = ''.join([str(s) for s in substring]) # since bitstring is a list of integers, we need to convert each integer to a char and join them to form a substring

        integer = int(chars, 2) # convert to int

        value = bounds[i][0] + (integer/largest) * (bounds[i][1] - bounds[i][0]) # rescale the integer to the bounds

        decoded.append(value)
    return decoded

"""
test_bounds = [[-10.0, 10.0], [-10.0, 10.0]]
test_n_bits = 16

test_bit_string = [random.randint(0, 1) for _ in range(test_n_bits * len(test_bounds))] # generate random bit string of length n_bits * len(bounds)
decoded_values = decode(test_bounds, test_n_bits, test_bit_string)

print(test_bit_string)
print(decoded_values)
"""

def selection(pop, scores, k=3): # uses tournament selection
    """
    pop: population
    scores: fitness scores
    k: number of individuals to select

    return best indiv frfom the tournament
    """
    
    selection_idx = random.randint(0, len(pop) - 1)

    for idx in random.sample(range(len(pop)), k-1):
        if scores[idx] < scores[selection_idx]:
            selection_idx = idx
    return pop[selection_idx]

def crossover(parent1, parent2, r_cross):
    """
    create two children from two parents using the crossover operation

    r_cross = crossover rate
    returns list: a list containing the two children
    """

    c1, c2 = parent1.copy(), parent2.copy()
    #random.random generates a random floating point number in the range (0.0, 1.0], excluding 1.0
    if random.random() < r_cross: # check if recombination should occur (basically a rate to decide if crossover should occur so that variety is introduced to the solutions)
        pt = random.randint(1, len(parent1)-2) # select crossover point
        c1 = parent1[:pt] + parent2[pt:]
        c2 = parent2[:pt] + parent1[pt:]
    return [c1, c2]

def mutation(bitstring, r_mut):
    """
    bitstring: the bitstring to mutate
    r_mut: mutation rate

    return: the mutated bitstring
    """

    for i in range(len(bitstring)):
        if random.random() < r_mut:
            bitstring[i] = 1 - bitstring[i] # flip the bit
    return bitstring

def genetic_algorithm(fitness, bounds, n_bits, n_iter, n_pop, r_cross, r_mut):
    """
    fitness: the objective function
    bounds: list of tuples containing the lower and upper bounds for each variable
    n_bits: number of bits for each variable
    n_iter: number of iterations
    n_pop: number of individuals in the population
    r_cross: crossover rate
    r_mut: mutation rate
    """

    pop = [[random.randint(0, 1) for _ in range(n_bits * len(bounds))] for _ in range(n_pop)] # generate random bit strings for the population

    best, best_eval = 0, fitness(decode(bounds, n_bits, pop[0])) # initialize solution to the first individual in the population, to be updated accordingly if a better fitness value is found

    for gen in range(n_iter):
        decoded = [decode(bounds, n_bits, p) for p in pop]
        scores = []
        for d in decoded:
            scores.append(fitness(d))

        for i in range(n_pop):
            if scores[i] < best_eval:
                best, best_eval = pop[i], scores[i]
                print(f"Generation {gen}, New Best solution: {best}, Fitness: {best_eval}")

        selected = [selection(pop, scores) for _ in range(n_pop)]

        children = []
        for i in range(0, n_pop, 2):
            p1, p2 = selected[i], selected[i+1]
            for c in crossover(p1, p2, r_cross):
                c = mutation(c, r_mut)
                children.append(c)
        pop = children
    return [best, best_eval]

# define parameters

bounds = [[-10.0, 10.0], [-10.0, 10.0]]
n_iter = 100
n_bits = 16
n_pop = 100
r_cross = 0.9
r_mut = 1.0 / (n_bits * len(bounds))
best, score = genetic_algorithm(fitness, bounds, n_bits, n_iter, n_pop, r_cross, r_mut)
print('---------------------------------------------------')
decoded = decode(bounds, n_bits, best)
print(f"Solution: {decoded}, Fitness: {score}") 
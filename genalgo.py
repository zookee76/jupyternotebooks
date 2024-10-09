import random

# Objective function to be minimized
def foo(x, y, z):
    return 6*x**3 + 9*y**2 + 90*z - 25

# Fitness function to evaluate how close the parameters x, y, z get to 0
def fitness(x, y, z): 
    ans = foo(x, y, z)

    if ans == 0:
        return 999999  # High fitness for perfect solution
    else:
        return abs(1/ans)  # Inverse of the absolute value of the objective function

# Step 1: Generate initial population of solutions
solutions = []
for s in range(1000):
    solutions.append((random.uniform(0, 10000), random.uniform(0, 10000), random.uniform(0, 10000)))

# Step 2: Evolve the population over generations
for i in range(10000):
    rankedsolutions = []
    
    # Step 3: Evaluate fitness of each solution
    for element in solutions:
        rankedsolutions.append((fitness(element[0], element[1], element[2]), element))

    # Step 4: Sort solutions by fitness (highest fitness first)
    rankedsolutions.sort(reverse=True)
    print(f"=== Generation {i} best solutions ===")
    print(rankedsolutions[0])  # Print the best solution of the current generation

    # Step 5: Check if a good enough solution is found, so if it doesnt satisfy a condition, the next generation is started
    if rankedsolutions[0][0] > 999:
        break

    # Step 6: Select the top solutions to form the next generation
    bestsolutions = rankedsolutions[:100]

    # Step 7: Extract parameters from the best solutions
    elements = []
    for element in bestsolutions:
        elements.append(element[1][0])
        elements.append(element[1][1])
        elements.append(element[1][2])

    # Step 8: Create new generation through mutation
    newGen = []
    for s in range(1000):
        e1 = random.choice(elements) * random.uniform(0.99, 1.01)
        e2 = random.choice(elements) * random.uniform(0.99, 1.01)
        e3 = random.choice(elements) * random.uniform(0.99, 1.01)

        newGen.append((e1, e2, e3))

    # Step 9: Replace old generation with new generation
    solutions = newGen

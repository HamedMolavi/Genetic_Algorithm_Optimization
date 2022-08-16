import numpy as np



def run(inputs):
    # Problem information
    objFn = inputs.objective_function
    varMin = inputs.lower_boundary
    varMax = inputs.upper_boundary
    nvar = inputs.nVar

    # Parameters
    maxit = inputs.total_generations
    npop = inputs.population_number
    pc = inputs.crossover_probability
    nchild =  int(round((pc * npop) / 2)) * 2 # Makes it even and integer
    gamma = inputs.gamma
    sigma = inputs.sigma
    pm = inputs.mutation_probability
    tol = inputs.tol
    backChek = inputs.backChek
    betta = inputs.betta
    behave = True if inputs.behave == 'min' else False # min is the True (assumption)


    population =  np.zeros([0, nvar], dtype='float64')
    objectives = np.zeros([0, 1], dtype='float64')
    # pop =[[x1, x2], [x1, x2], ...]; objectives[[o], [o], ...]

    # Best Solution
    bestSol = np.array([[],[np.inf if behave else -np.inf]], dtype='object')

    # Initialize Population
    for i in range(npop):
        population = np.append(population, np.random.uniform(varMin, varMax, nvar).reshape(-1, nvar), axis=0)
        objectives = np.append(objectives,  np.array([[objFn(population[i])]]), axis=0)
        if objectives[i][0] < bestSol[1][0]:
            bestSol[1][0] = objectives[i][0]
            bestSol[0] = population[i]

    # Best cost of iterations
    # bestCost = np.empty(maxit)
    bestCost = []

    # Main Loop
    for it in range(maxit):
        popChildren = np.zeros([0, nvar], dtype='float64')
        objChildren = np.zeros([0, 1], dtype='float64')
        # Make costs list for roullete feed
        costs = np.array([el[0] for el in objectives]) # make a linear copy of objectives
        avg_cost = np.mean(costs)
        if avg_cost != 0:
            costs /= avg_cost # Normalize costs array
        probabilities = np.exp(-betta * costs)
        for _ in range(nchild):

            # Roulette Wheel selection of parents
            parent1 = population[roulette_wheel_selection(probabilities)]
            parent2 = population[roulette_wheel_selection(probabilities)]


            # Perform crossover
            child1, child2 = crossover(parent1, parent2, gamma)
            # Evaluate First Offspring
            costChild1 = np.array([[objFn(child1)]])
            if costChild1[0][0] < bestSol[1][0]:
                bestSol[1][0] = costChild1[0][0]
                bestSol[0] = child1
            # Evaluate Second Offspring
            costChild2 = np.array([[objFn(child2)]])
            if costChild2[0][0] < bestSol[1][0]:
                bestSol[1][0] = costChild2[0][0]
                bestSol[0] = child2


            # Perform mutation
            child1 = mutate(child1, pm, sigma)
            child2 = mutate(child2, pm, sigma)
            # After mutations we must ensure that mutants are in range
            child1 = apply_bound(child1, varMin, varMax)
            child2 = apply_bound(child2, varMin, varMax)

            # Copy Children to the pool
            popChildren = np.append(popChildren, child1.reshape(-1, nvar), axis=0)
            popChildren = np.append(popChildren, child2.reshape(-1, nvar), axis=0)
            objChildren = np.append(objChildren, costChild1, axis=0)
            objChildren = np.append(objChildren, costChild2, axis=0)
        
        # Merging two populations and sort it
        population = np.append(population, popChildren, axis=0)
        objectives = np.append(objectives, objChildren, axis=0)
        pop_list = population.tolist()
        obj_list = objectives.tolist()
        sorted_lists = sort(pop_list, obj_list)
        population, objectives = [np.array(list) for list in sorted_lists]
        # Keeping npop best individuals (Deleting the worst)
        population = population[0:npop]
        objectives = objectives[0:npop]

        # Store best cost
        bestCost.append(bestSol[1][0])
        #Show Iteration Info
        if it % 50 == 0:
            print("Iteration {}: Best Cost = {}".format(it, bestCost[it]))
        # print('Best Solution: ', [round(el, 4) for el in bestSol.pos])

        # Break condition
        if it > backChek:
            if abs(bestCost[it] - bestCost[it - backChek]) < tol:
                print("END BY BREAKING")
                break
    print("Iteration {}: Best Cost = {}".format(it, bestCost[it]))
    print("END OF ITERATION")

    # Output
    out ={
        "population": population,
        "objectives": objectives,
        "bestCost": bestCost
    }
    return out





# =========================================================================
def roulette_wheel_selection(p):
    cum = np.cumsum(p)
    r = sum(p) * np.random.rand()
    inds = np.argwhere(r <= cum)
    return inds[0][0]


def crossover(parent1, parent2, gamma: float = 0.1):
    child1 = np.copy(parent1)
    child2 = np.copy(parent2)
    # Random vecor for uniform crossover
    alpha = np.random.uniform(-gamma, 1 + gamma, *child1.shape)
    child1 = alpha * parent1 + (1 - alpha) * parent2
    child2 = alpha * parent2 + (1 - alpha) * parent1
    return [child1, child2]

def mutate(x, pm: float, sigma: float):
    '''sigma: standard deviation
    pm: mutation probability'''
    y = np.copy(x)
    # Indicate which Genes will mutate
    flag = np.random.rand(*x.shape) <= pm # An array of True and Falses
    inds = np.argwhere(flag) # Returns the indices of True
    y[inds] += sigma * np.random.randn(*inds.shape) # Add the random step to  positions
    return y

def apply_bound(x, varMin: float, varMax: float):
    x = np.maximum(x, varMin) # Pos will be original pos or min if pos is lower
    x = np.minimum(x, varMax) # Pos will be original pos or max if pos is higher
    return x

def swap(a_list: list, first: int, second: int) -> list:
    temp = a_list[first]
    a_list[first] = a_list[second]
    a_list[second] = temp
    return a_list

def sort(a_list: list, based_on_list: list) -> list:
    for count in range(len(a_list)):
        i = based_on_list.index(min(based_on_list[count:]))
        a_list = swap(a_list, i, count)
        based_on_list = swap(based_on_list, i, count)
    return [a_list, based_on_list]

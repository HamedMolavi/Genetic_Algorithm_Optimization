import tools.inps as inputs
from tools import ga

# Sphere test funciton
def f(x):
    # return float((x[0] ** 2 + x[1] - 11) + (x[0] + x[1] ** 2 - 7) ** 2)
    return sum(x)
inputs.objective_function = f


# Run GA
out = ga.run(inputs)


# Results


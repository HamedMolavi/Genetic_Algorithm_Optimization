import sys
__help = '''Welcome to this simple GA program...
    Vriables
================
--Lower or -L       => Lower Boundary, Defaulted to 0, either an integer or number of nVar integers
--Upper or -U       => Upper Boundary, Defaulted to 6, either an integer or number of nVar integers
--variables or -v   => Number of Variables defaulted to 5, in case of a list used for Lower and Upper, use this before them
--generations or -g => Total Iteration number of Generations, Defaulted to 100
--Gamma or -G       => Gamma Value defaulted to  0.1
--Sigma or -S       => Sigma Value defaulted to  0.1
--tolerance or -t   => Tolerance defaulted to  10e-10
--Betta or -b       => Betta Value defaulted to  1
--popNo or -n       => Number of Individuals in population, Defaulted to 20
--cross or -c       => Crossover Rate defaulted to 0.8
--mutate or -m      => Mutation Rate defaulted to 0.09
--behave or -b      => (min || max) Behavior of Objective Function, Defaulted to min
'''

def __boundary(i, nVar):
    if len(sys.argv) <= i + 2:
        check = True
    else:
        if sys.argv[i + 2].startswith('-'):
            check = True
        else:
            check = False
    if check:
        boundary = int(sys.argv[i + 1])
        i += 2
    elif len(sys.argv) > i + 2:
        boundary = []
        for _ in range(nVar):
            i += 1
            if sys.argv[i].isnumeric():
                boundary.append(int(sys.argv[i]))
            else:
                sys.exit("In case of a list used for Lower and Upper, use this before them.")
        i += 1
    return [boundary, i]

# Problem defenition
lower_boundary = 0
upper_boundary = 6
nVar = 2

# GA parameters
total_generations = 100
gamma = 0.1
sigma = 0.1
tol = 10 ** -10
betta = 1
population_number = 20
crossover_probability = 0.8
mutation_probability = 0.05
behave = 'min'

# Calculated parameter
backChek = int(total_generations * 3 / 20)
__both_boudary_changed = True
try:
    if len(sys.argv) > 1:
        inps = {}
        __i = 1 # len(sys.argv)
        while True:
            if (sys.argv[__i] == '--Lower' or sys.argv[__i] == '-L'):       #   Lower Boundary      => L
                __both_boudary_changed = False if __both_boudary_changed else True
                lower_boundary, __i = __boundary(__i, nVar)
            elif (sys.argv[__i] == '--Upper' or sys.argv[__i] == '-U'):       #   Upper Boundary      => U
                __both_boudary_changed = False if __both_boudary_changed else True
                upper_boundary, __i = __boundary(__i, nVar)
            elif (sys.argv[__i] == '--variables' or sys.argv[__i] == '-v'):   #   Number of Variables => v
                nVar = int(sys.argv[__i + 1])
                __i += 2
            elif (sys.argv[__i] == '--generations' or sys.argv[__i] == '-g'): #   Generation Loop     => g
                total_generations = int(sys.argv[__i + 1])
                __i += 2
            elif (sys.argv[__i] == '--Gamma' or sys.argv[__i] == '-G'):       #       Gamma Value     => G
                gamma = int(sys.argv[__i + 1])
                __i += 2
            elif (sys.argv[__i] == '--Sigma' or sys.argv[__i] == '-S'):       #       Sigma Value     => S
                sigma = int(sys.argv[__i + 1])
                __i += 2
            elif (sys.argv[__i] == '--tolerance' or sys.argv[__i] == '-t'):   #       Tolerance       => t
                tol = int(sys.argv[__i + 1])
                __i += 2
            elif (sys.argv[__i] == '--Betta' or sys.argv[__i] == '-b'):       #           Betta       => b
                betta = int(sys.argv[__i + 1])
                __i += 2
            elif (sys.argv[__i] == '--popNo' or sys.argv[__i] == '-n'):       #   Population Number   => n
                population_number = int(sys.argv[__i + 1])
                __i += 2
            elif (sys.argv[__i] == '--cross' or sys.argv[__i] == '-c'):       #   Crossover Rate      => c
                crossover_probability = int(sys.argv[__i + 1])
                __i += 2
            elif (sys.argv[__i] == '--mutate' or sys.argv[__i] == '-m'):      #   Mutation Rate       => m
                mutation_probability = int(sys.argv[__i + 1])
                __i += 2
            elif (sys.argv[__i] == '--behave' or sys.argv[__i] == '-b'):      #   Behavior of Objective Function
                behave = sys.argv[__i + 1]
                __i += 2
            elif (sys.argv[__i] == '--help' or sys.argv[__i] == '-h'):      #   help
                print(__help)
                sys.exit(0)
            else:
                print("### Error ###")
                print("You have entered something I dont understand. What is", sys.argv[__i], "?")
                print('If you cant use our syntax, enter --help or -h.')
                sys.exit(1)
            if __i > len(sys.argv) - 1 :
                break
        if not __both_boudary_changed:
            raise SyntaxError("When using Lower boundary, should use Upper boundary too.")
        if type(lower_boundary) != type(upper_boundary):
            raise SyntaxError("Both lower and upper boundaries must use same way of definition")
except IndexError:
    sys.exit("You made a mistake in syntax. please use --help or -h first")



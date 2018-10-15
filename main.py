import numpy.random
from solver import SATInstance

instance = SATInstance()
instance.from_file('dimacs.txt')
instance.create_random_assignment()
print('+++ Start +++')
print('First assignment: ', instance.variables, '\n\n')

improved = 1
satisfied = 0
movesSinceImprovement = 0
while improved >= 0 and satisfied < len(instance.clauses) and movesSinceImprovement < 10:
    improved = instance.find_next_assignment()
    if improved == 0:
        movesSinceImprovement = movesSinceImprovement + 1
    elif improved > 0:
        movesSinceImprovement = 0
    satisfied = instance.count_satisfied_clauses(instance.variables)
    print('=== Finding next improvement ===')
    print('Assignment: ', instance.variables)
    print('Clauses satisfied: ', satisfied, '\n')

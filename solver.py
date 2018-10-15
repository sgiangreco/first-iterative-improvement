import random

class SATInstance(object):
    def parse_and_add_clause(self, line):
        clause = []
        for literal in line.split():
            negated = 1 if literal.startswith('-') else 0
            variable = literal[negated:] # slices off negative sign of literal
            encoded_literal = int(variable) << 1 | negated # multiplies value by 2 and adds 1 if negative
            clause.append(encoded_literal) # adds integer to current clause
        self.clauses.append(tuple(set(clause))) # adds clause to list of clauses for instance

    def __init__(self):
        self.variables = []
        self.clauses = []

    #@classmethod
    def from_file(self, filename): # using self instead of cls
        #instance = cls()
        #inputFile = open(filename)
        with open(filename) as f:
            for line in f:
                if line.startswith('p'):
                    self.parse_problem_line_and_set_variable_length(line)
                elif len(line) > 0 and not line.startswith('c') and not line.startswith('p'):
                    self.parse_and_add_clause(line[:len(line)-2]) # 0 marks end of line
        return

    def literal_to_string(self, literal):
        s = '-' if literal & 1 else ''
        return s + self.variables[literal >> 1]

    def clause_to_string(self, clause):
        return ' '.join(self.literal_to_string(l) for l in clause)

    # Pre: assignment is a binary array with each element corresponding to the value of its respective index
    #      self.clauses is list of tuples, each of which contains the encoding of its literals
    # Post: Returns positive integer
    # Desc: Takes in an assignment of variables and returns number of clauses it satisfies.
    def count_satisfied_clauses(self, assignment):
        totalSatisfied = 0
        for clause in self.clauses:
            foundTrue = 0
            i = 0
            while not foundTrue and i < len(clause):
                foundTrue = (clause[i] & 1) ^ assignment[(clause[i] >> 1) - 1]
                i = i + 1
            totalSatisfied = totalSatisfied + foundTrue
        return totalSatisfied

    # Pre:  variables list is of desired length
    #       random module is installed
    # Post: Returns list of binary values
    # Desc: Creates a list of random binary values corresponding to assignments of variables
    def create_random_assignment(self):
        assignment = []
        for i in self.variables:
            assignment.append(random.randrange(2))
        self.variables = assignment
        return

    # Pre:  line is problem line of DIMACS graph format
    #       line contains 4 elements
    # Post: Changes variables list to empty of certain size
    # Desc: Parses the problem line of the input file and sets length of variable list
    def parse_problem_line_and_set_variable_length(self, line):
        self.variables = [None] * int(line.split()[2])
        return

    # Pre:  None
    # Post: Returns 1-exchange neighbor of assignment
    # Desc: Flips the bit on the variable in the given index and returns altered assignment
    def create_neighbor(self, assignment, index):
        newAssignment = assignment.copy()
        newAssignment[index] = (newAssignment[index] + 1) % 2
        return newAssignment

    # Pre:  There exists an assignment of variables
    #       The clauses have been compiled
    # Post: Returns integer
    # Desc: Looks at neighboring assignments until an improvement is found or no improvement can be made; returns number of improvements made
    def find_next_assignment(self):
        currentSatisfied = self.count_satisfied_clauses(self.variables)
        newSatisfied = 0
        newAssignment = []
        i = 0
        improved = -1 # 1 indicates improvement, 0 indicates same number of clauses
        while improved < 1 and i < len(self.variables):
            print('--- i = ', i, '---')
            newAssignment = self.create_neighbor(self.variables, i)
            print('Prospective assignment: ', newAssignment)
            newSatisfied = self.count_satisfied_clauses(newAssignment)
            improved = newSatisfied - currentSatisfied
            print('Improvement: ', improved, '\n')
            i = i + 1
        if improved > 0:
            self.variables = newAssignment
            return improved
        else:
            return 0

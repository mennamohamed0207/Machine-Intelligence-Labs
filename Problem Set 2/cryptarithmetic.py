from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        def add_binary_constraint(self, var1, var2, constraint):
            """Add a binary constraint as a lambda function."""
            self.binary_constraints.append((var1, var2, constraint))
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).
        #getting the variables
        problem.variables = []
        for letter in LHS0 + LHS1 + RHS:
            if letter not in problem.variables:
                problem.variables.append(letter)
        #adding carries
        problem.variables.extend([f"C{i}" for i in range(1, len(RHS))])
        print(problem.variables)
        problem.domains = {}
        #adding domains
        #adding 0-9 for letters except for the first letter in LHS1, LHS0 and RHS
        #adding {0,1} for carries
        for letter in problem.variables:
            if letter == LHS0[0] or letter == LHS1[0] or letter == RHS[0]:
                problem.domains[letter] = set(range(1, 10))
            elif letter[0] == "C" and letter[1:].isdigit():
                problem.domains[letter] = set([0, 1])
            else:
                problem.domains[letter] = set(range(10))
        print(problem.domains)
        
        #adding constraints
        problem.constraints = []
        #adding uniqueness for each letter 
        for letter in problem.variables:
            problem.constraints.append(UnaryConstraint(letter, lambda x: x is None or x in problem.domains[letter]))
        #adding constraints for the sum
        # for example if we have TWO + TWO = FOUR
        # we have the following constraints
        # 10*C3 + O = 2*T + C2
        # 10*C2 + U = 2*W + C1
        # 10*C1 + R = 2*O
        # F=C3
        # i want to make it more general
        # for i in range(len(RHS)):
        #     carry = f"C{i}"
        #     r = RHS[i]
        #     d0 = LHS0[i] if i < len(LHS0) else None
        #     d1 = LHS1[i] if i < len(LHS1) else None
        #     cin = carry_vars[i]
        #     carry_out = carry_vars[i + 1]
            
        #     if l0 and l1:  # Full equation: l0 + l1 + carry_in = r + 10 * carry_out
        #         if d0 + d1 + c_in == r_digit + 10 * c_out:
        #                 add_binary_constraint(l0, l1, lambda x, y: x + y == r_digit)
        #                 add_binary_constraint(l1, carry_in, lambda y, z: y + z <= 9)
        #                 add_binary_constraint(carry_in, r, lambda z, w: z + 1 == w)
           
        
            
    
        
       
    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())
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
        carries = [f"C{i}" for i in range( len(RHS))]
        problem.variables.extend(carries)
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
        for i, letter1 in enumerate(problem.variables):
            for letter2 in problem.variables[i + 1:]:
                # the letter is not C1, C2, C3
                if not (letter1[0] == "C" and letter1[1:].isdigit()) and not (letter2[0] == "C" and letter2[1:].isdigit()):
                    problem.constraints.append(
                        BinaryConstraint(
                            (letter1,
                            letter2),
                            lambda x, y: x is None or y is None or x != y
                        )
                    )

        #adding constraints for the sum
        problem.constraints.append(BinaryConstraint((RHS[-1], f"C{len(RHS)-1}"), lambda x, y: x == y))
        for i in range(0, len(RHS)):
            carry = f"C{i}"
            carry_next = f"C{i+1}"
            if i==0:
                problem.constraints.append(BinaryConstraint((LHS0[-1], LHS1[-1]), lambda x, y: x + y == RHS[-1]+carry_next*10))
            elif i<=len(RHS)-1 and i<len(LHS0) and i<len(LHS1):
                problem.constraints.append(BinaryConstraint((LHS0[i], LHS1[i]), lambda x, y: x + y + carry == RHS[i]+carry_next*10))


        
        return problem
    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.domains:
            var = set(self.domains[v])
            for x in var:
                if len(x) != v.length:
                    self.domains[v].remove(x)
                #print(x)
        
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        crossroad = self.crossword.overlaps[x,y]
        #print("crossroad: ", crossroad)
        revised = False
        if crossroad is None:
            return False
        else:
            i,j = crossroad
            #print("i,j", i,j)
        #print("out: ", i,j)
        #print(self.domains[x])

        for xval in set(self.domains[x]):
            #print("xval: ", xval)
            remove = True
            for yval in self.domains[y]:
                if yval[j] == xval[i] and xval != yval:
                    remove = False
            if remove == True:
                self.domains[x].remove(xval)
                revised = True
            else:
                revised = False
        #print("revised: ", revised)
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = list()
            # queue = all arcs in the problems
            for x in self.domains:
                for y in self.crossword.neighbors(x):
                    #if x != y and y in self.crossword.neighbors(x):
                    arc = (x,y)
                    arcs.append(arc)
        #while queue non-empty:              
        while arcs:
            #(X,Y) = DEQUEUE(QUEUE)
            x,y = arcs.pop()
            #if REVISE(X,Y)
            if self.revise(x,y):
                #if size of X.domain == 0
                if len(list(self.domains[x])) == 0:
                    return False
                #for each Z in X.neighbors - {Y}
                for z in self.crossword.neighbors(x)-self.domains[y]:
                    new_arc = (z,x)
                    arcs.append(new_arc)
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # if len(list(assignment.values())) == len(list(assignment.keys())):
        #     return True
        # else:
        #     return False

        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return False
            if assignment[variable] not in self.crossword.words:
                return False
        
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #all values are distinct
        if len(list(assignment.values())) != len(set(assignment.values())):
            return False

        #every value is the correct length
        for v in assignment:
            value1 = assignment[v]
            if len(value1) != v.length:
                return False

        #no conflicts between neighboring variables
            for n in assignment:
                value2 = assignment[n]
                if v != n:
                    crossroad = self.crossword.overlaps[v,n]
                    if crossroad is not None:
                        i,j = crossroad
                        if value1[i] != value2[j]:
                            return False
        return True
                


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        n = dict()

        for value_domain in self.domains[var]:
            key_n = value_domain
            n[key_n] = 0
            for neighbor in self.crossword.neighbors(var) - set(assignment):
                if value_domain in self.domains[neighbor]:
                    n[key_n] += 1
        
        order = sorted(n,key=n.get)
        return order

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        best_variable = 0
        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return variable
        #         if best_variable is None:
        #             best_variable = variable
        #         elif self.crossword.neighbors(variable) > self.crossword.neighbors(best_variable) or len(self.domains[variable]) < len(self.domains[best_variable]):
        #            best_variable = variable
        #         else:
        #             best_variable = variable
        # return best_variable      


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var,assignment):
            assignment[var] = value
            if self.consistent(assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result != None:
                    return result
            assignment.pop(var)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()

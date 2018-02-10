from typing import List
from PuzzleState import PuzzleState as State
from Constraints import Constraints
from Permutation import Permutation
import copy
import time

class PuzzleSolver:
    def __init__(self, constraints: Constraints) -> None:
        self.constraints : Constraints = constraints
        self.permutation: Permutation = Permutation(constraints)

    def _depth_first_search(self, row: int) -> None:
        self.nodes += 1
        if row > self.max_row:
            self.max_row = row
            print("Row: {}, expanded nodes: {}, nodes/s: {:.2f}".format(
                self.max_row, self.nodes, self.nodes / (time.time() - self.start_time)
            ))

        if not self.state.validate(row):
            return

        if row + 1 == self.constraints.height:
            self.solutions.append(copy.deepcopy(self.state))
            return

        for perm in self.permutation.get_permutations(row+1):
            self.state.set_row(row+1, perm)
            self._depth_first_search(row+1)
            
        self.state.set_row(row+1, [None for _ in range(self.constraints.width)])

    def solve(self) -> List[State]:
        self.state : State = State(self.constraints)
        self.solutions : List[State] = []
        
        self.nodes = -1
        self.max_row = 0
        self.start_time = time.time()
        self._depth_first_search(-1)

        return self.solutions
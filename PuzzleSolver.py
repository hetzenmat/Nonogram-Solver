from typing import List
from PuzzleState import PuzzleState as State
from Constraints import Constraints

class PuzzleSolver:
    def __init__(self, constraints: Constraints) -> None:
        self.constraints = constraints

    def _depth_first_search(self, row)

    def solve(self) -> List[State]:
        self.state = State(self.constraints.width, self.constraints.height)
        self.solutions = []

        self._depth_first_search(0)

        return self.solutions
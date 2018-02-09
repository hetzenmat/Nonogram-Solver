from Constraints import Constraints
from typing import Union

class PuzzleState:
    EMPTY = False
    BLOCK = True

    def __init__(self, constraints: Constraints) -> None:
        self.constraints = constraints
        self._state = [
            [None for _ in range(constraints.width)] for _ in range(constraints.height)
        ]

    def _check_limits(self, row: int, column: int) -> bool:
        return (0 <= row < self.constraints.height) and \
               (0 <= column < self.constraints.width)

    def set(self, row: int, column: int, value: Union[bool, None]) -> None:
        assert self._check_limits(row, column)
        self._state[row][column] = value

    def get(self, row: int, column: int) -> Union[bool, None]:
        assert self._check_limits(row, column)
        return self._state[row][column]

    def validate(self, completed_rows: int) -> bool:
        for i in range(self.constraints.width):
            column_constraints = self.constraints.columns[i]

            # if there are no blocks in the current column
            if len(column_constraints) == 0:
                # return false if there is any block
                for j in range(completed_rows):
                    if self.get(j, i):
                        return False
                
                # column is valid
                continue

            in_block = False # flag if the current position is in a block
            block_index = 0 # the index of the next block
            num_cells = None # the number of remaing cells in the current block
            
            for j in range(completed_rows):
                if self.get(j, i): # the current cell is occupied
                    if in_block:
                        num_cells -= 1  # consume one cell of the remaining ones
                        if num_cells < 0:
                            # there are more cells in the block than in the constraint
                            return False
                    else:
                        if block_index >= len(column_constraints):
                            return False # a new block starts but there are no more in the constraints

                        num_cells = column_constraints[block_index] - 1
                        block_index += 1
                        in_block = True
                elif in_block:
                    if num_cells != 0: 
                        return False # if not all cells were consumed the state is not valid
                    in_block = False
            
            if completed_rows == self.constraints.height and block_index != len(column_constraints):
                return False # there were too few blocks in the current state
            
            # check if the column can't be completed with the remaining blocks
            remaining_cells = self.constraints.height - completed_rows
            remaining_constraints = column_constraints[block_index:]
            if sum(remaining_constraints) + len(remaining_constraints) - 1 > remaining_cells:
                return False

        return True # no errors were found so the state is valid

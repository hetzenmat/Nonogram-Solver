from typing import List
from PuzzleState import PuzzleState as State

class Permutation:
    def __init__(self, blocks: List[int], size: int) -> None:
        self.blocks = blocks
        self.size = size
        self.single = (len(blocks) == 0)
        self.stop = False

        # initial state
        self.positions = [0]
        for block_length in blocks[1:]:
            self.positions.append(self.positions[-1] + block_length + 1)

    def _to_cells(self):
        r = [State.EMPTY for _ in range(self.size)]
        for block_index, position in enumerate(self.positions):
            for i in range(position, self.blocks[block_index]):
                r[i] = State.BLOCK
        return r

    def _next_permutation(self):
        pass

    def __iter__(self) -> "Permutation":
        return self

    def __next__(self) -> List[int]:
        if self.stop:
            raise StopIteration
        if self.single:
            self.stop = True
            return [State.EMPTY for _ in range(self.size)]

        return_value = self._to_cells()
        self._next_permutation()
        return return_value
        


from typing import List
from PuzzleState import PuzzleState as State

class Permutation:
    def __init__(self, blocks: List[int], size: int) -> None:
        self.blocks = blocks
        self.size = size
        self.single = (len(blocks) == 0)
        self.stop = False

        # initial state
        positions = [0]
        for block_length in blocks[1:]:
            positions.append(positions[-1] + block_length + 1)
        self.stack = [(len(blocks) - 1, positions)]
        self.stack_index = 0

    def _positions_copy(self, positions: List[int]) -> List[int]:
        return [i for i in positions]

    def _to_cells(self, positions: List[int]) -> List[bool]:
        r = [State.EMPTY for _ in range(self.size)]
        for block_index, position in enumerate(positions):
            for i in range(position, self.blocks[block_index]):
                r[i] = State.BLOCK
        return r

    def _can_shift(self, block_index: int, positions: List[int]) -> bool:
        if block_index + 1 == len(positions):
            # there must be one or more free cells next to the last block
            return positions[block_index] + self.blocks[block_index] < self.size

        # there must be more than one free cell next to the block
        return positions[block_index] + self.blocks[block_index] + 1 < positions[block_index + 1]

    def _next_permutation(self):
        if len(self.stack) == 0:
            self.stop = True
            return

        block_index, positions = self.stack[0]
        if block_index < 0:
            self.stack.pop(0)
            return

        if not self._can_shift(block_index, positions):
            self.stack = self.stack[1:]
            self.stack_index -= 1
            self._next_permutation()
            return

        positions[block_index] += 1
        self.stack.append((block_index - 1, self._positions_copy(positions)))

    def __iter__(self) -> "Permutation":
        return self

    def __next__(self) -> List[int]:
        if self.stop:
            raise StopIteration
        if self.single:
            self.stop = True
            return [State.EMPTY for _ in range(self.size)]

        return_value = self._to_cells(self.stack[self.stack_index][1])
        self.stack_index += 1
        self._next_permutation()
        return return_value

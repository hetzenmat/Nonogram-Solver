#!/bin/python3
import sys
import os
import json
from typing import List, Dict, Any
from Constraints import Constraints
from PuzzleSolver import PuzzleSolver as Solver
from PuzzleState import PuzzleState as State

def print_usage() -> None:
    """
    Prints usage information on how to run this program.
    """

    # TODO
    print("usage")

def process_puzzle(path: str) -> None:
    """
    Processes one puzzle.
    The necessary steps are: Check the file, validate the contents, run the solver and 
    print the solutions, if any are found.
    """
    if not os.path.isfile(path):
        print("{} is not a regular file.".format(path))
        return

    try:
        f = open(path)
        json_object = json.load(f)
    except OSError as error:
        print("An error occurred while opening the file {}".format(path),
              file=sys.stderr)
        print(error.strerror, file=sys.stderr)
        return
    except json.JSONDecodeError as error:
        print("An error occurred while parsing the JSON file {}".format(path),
              file=sys.stderr)
        return
    else:
        f.close()

    errors, instance = Constraints.validate_json(json_object)
    if errors:
        print("The configuration file is not valid.", file=sys.stderr)
        print("Errors:", file=sys.stderr)
        print("\t", end="", file=sys.stderr)
        print("\n\t".join(errors), file=sys.stderr)
        return

    solver: Solver = Solver(instance)
    solutions: List[State] = solver.solve()
    
    first = True
    for index, solution in enumerate(solutions):
        if not first:
            print()
        first = False
        print("Solution {}/{}".format(index + 1, len(solutions)))
        print(solution)
    
def main() -> None:
    if len(sys.argv) < 2 or \
       any(help_command in sys.argv for help_command in ["--help", "-h", "-?"]):
        print_usage()
        return

    puzzles = len(sys.argv) - 1
    for index, path in enumerate(sys.argv[1:]):
        print("Processing puzzle {} of {}".format(index + 1, puzzles))
        process_puzzle(path)

if __name__ == "__main__":
    main()
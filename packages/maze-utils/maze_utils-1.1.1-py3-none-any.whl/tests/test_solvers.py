import pytest

from maze_utils import solvers, mazes


@pytest.mark.parametrize("solver", solvers.__all__)
def test_mazes(solver):
    maze = mazes.KruskalMaze(10, 10).maze
    solver = getattr(solvers, solver)
    print(solver(maze).solution)

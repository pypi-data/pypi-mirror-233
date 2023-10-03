import pytest

from maze_utils import mazes


@pytest.mark.parametrize("maze", mazes.__all__)
def test_mazes(maze):
    maze = getattr(mazes, maze)
    print(maze(10, 10).maze)

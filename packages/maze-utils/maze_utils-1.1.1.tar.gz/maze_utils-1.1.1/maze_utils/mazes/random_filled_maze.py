from random import randint
from typing import Generator

import numpy as np
import numpy.typing as npt

from .base import MazeBase


class RandomMaze(MazeBase):
    def _make_maze(self, n_x, n_y) -> Generator[npt.NDArray[np.int_], None, npt.NDArray[np.int_]]:
        maze_arr = np.zeros([n_x, n_y], dtype=int)
        for i in range(n_x):
            for j in range(n_y):
                maze_arr[i, j] = self._fill_square()
                yield maze_arr
        return maze_arr

    @staticmethod
    def _prepare_final(maze: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
        """Prepare final maze with border of _walls."""
        final = np.full([maze.shape[0] + 2, maze.shape[1] + 2], 1, dtype=int)
        final[1:-1, 1:-1] = maze
        return final

    @staticmethod
    def _fill_square(percentage=50):
        random_ = randint(0, 101)
        if random_ > percentage:
            return 1
        return 0

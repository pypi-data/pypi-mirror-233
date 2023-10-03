from random import randint, random
from typing import Generator

import numpy.typing as npt
from numpy import full, arange, reshape, ravel, ones, int_

from .base import MazeBase


class KruskalMaze(MazeBase):
    def __init__(self, n_x: int, n_y: int) -> None:
        super().__init__(n_x, n_y)
        self._num_cells_last: int = 0
        self._maze: npt.NDArray[int_] = full([], 1, dtype=int)
        self._repeat_iterations: int = 0

    def _make_maze(self, n_x: int, n_y: int) -> Generator[npt.NDArray[int_], None, npt.NDArray[int_]]:
        self._num_cells_last: int = 0
        self._maze: npt.NDArray[int_] = full([], 1, dtype=int)
        self._repeat_iterations: int = 0
        self._num_cells_last = -1
        len_x = n_x + 4
        len_y = n_y + 4
        self._maze = full([len_x, len_y], 1, dtype=int)
        self._make_walls()
        self._make_sets()
        self._repeat_iterations = 0
        while True:
            self._join_cells()
            if self._check_final():
                break
            yield self._maze
        return self._maze

    def _make_walls(self):
        self._walls = arange(0, self._maze.size, dtype=int)
        self._walls = reshape(self._walls, self._maze.shape)
        for i in range(self._maze.shape[0]):
            if (i % 2) == 1:
                self._walls[i, :] = -1
        for j in range(self._maze.shape[1]):
            if (j % 2) == 1:
                self._walls[:, j] = -1
        self._walls[:, 0] = self._walls[:, -1] = -1
        self._walls[0, :] = self._walls[-1, :] = -1

    def _make_sets(self):
        self._sets = []
        for i in range(self._walls.shape[0]):
            for j in range(self._walls.shape[1]):
                wall_id = self._walls[i, j]
                self._sets.append({wall_id})

    def _pick_wall(self):
        while True:
            i = randint(2, self._walls.shape[0] - 3)
            j = randint(2, self._walls.shape[1] - 3)
            wall_id = self._walls[i, j]
            if (
                (self._walls[i + 1, j] == -1)
                and (self._walls[i - 1, j] == -1)
                and (self._walls[i, j + 1] == -1)
                and (self._walls[i, j - 1] == -1)
            ):
                continue
            if wall_id == -1:
                return i, j

    def _check_wall(self):
        id_1 = None
        id_2 = None
        i_1 = None
        i_2 = None
        j_1 = None
        j_2 = None

        for i in range(5):
            i, j = self._pick_wall()
            set_id_left = self._walls[i - 1, j]
            set_id_right = self._walls[i + 1, j]
            set_id_up = self._walls[i, j + 1]
            set_id_down = self._walls[i, j - 1]

            set_left = self._sets[set_id_left]
            set_right = self._sets[set_id_right]
            set_up = self._sets[set_id_up]
            set_down = self._sets[set_id_down]

            rand_flt = random()
            if rand_flt <= 0.5:
                sym_diff = set_left ^ set_right
                if (set_id_left in sym_diff) and (set_id_right in sym_diff):
                    id_1 = set_id_left
                    id_2 = set_id_right
                    i_1, j_1 = i - 1, j
                    i_2, j_2 = i + 1, j

            else:
                sym_diff = set_up ^ set_down
                if (set_id_up in sym_diff) and (set_id_down in sym_diff):
                    id_1 = set_id_up
                    id_2 = set_id_down
                    i_1, j_1 = i, j + 1
                    i_2, j_2 = i, j - 1

            if id_1 is None:
                continue
            self._walls[i, j] = -2

            self._maze[i, j] = 0
            self._maze[i_1, j_1] = 0
            self._maze[i_2, j_2] = 0

            return id_1, id_2

        return None, None

    def _check_final(self) -> bool:
        flat = ravel(self._maze)
        num_cells: int = len(flat[flat == 0])
        if num_cells == self._num_cells_last:
            self._repeat_iterations += 1
        if self._repeat_iterations > 20:
            return True
        if num_cells != self._num_cells_last:
            self._repeat_iterations = 0
            self._num_cells_last = num_cells
        return False

    def _join_cells(self) -> None:
        id_1, id_2 = self._check_wall()
        if id_1 is None:
            return

        for i in range(self._maze.shape[0]):
            for j in range(self._maze.shape[1]):
                if self._maze[i, j] == 0:
                    if self._maze[i + 1, j] == 0:
                        self._sets[self._walls[i, j]].update(self._sets[self._walls[i + 2, j]])
                        self._sets[self._walls[i + 2, j]].update(self._sets[self._walls[i, j]])
                    if self._maze[i - 1, j] == 0:
                        self._sets[self._walls[i, j]].update(self._sets[self._walls[i - 2, j]])
                        self._sets[self._walls[i - 2, j]].update(self._sets[self._walls[i, j]])
                    if self._maze[i, j + 1] == 0:
                        self._sets[self._walls[i, j]].update(self._sets[self._walls[i, j + 2]])
                        self._sets[self._walls[i, j + 2]].update(self._sets[self._walls[i, j]])
                    if self._maze[i, j - 1] == 0:
                        self._sets[self._walls[i, j]].update(self._sets[self._walls[i, j - 2]])
                        self._sets[self._walls[i, j - 2]].update(self._sets[self._walls[i, j]])

    @staticmethod
    def _prepare_final(maze: npt.NDArray[int_]) -> npt.NDArray[int_]:
        maze_temp = ones([maze.shape[0] - 2, maze.shape[1] - 2], dtype=int)
        maze_temp[1:-1, 1:-1] = maze[2:-2, 2:-2]
        return maze_temp

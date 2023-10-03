import random
from typing import List, Tuple, Generator

import numpy as np
import numpy.typing as npt

from .base import MazeBase


class DepthFirstMaze(MazeBase):
    def __init__(self, n_x: int, n_y: int) -> None:
        n_x += 1
        n_y += 1
        super().__init__(n_x, n_y)
        self._visited = set()
        self._stack = []

    def _make_maze(self, n_x: int, n_y: int) -> Generator[npt.NDArray[np.int_], None, npt.NDArray[np.int_]]:
        start_i, start_j = self._pick_start_cell()
        _maze = np.full([n_x, n_y], 1, dtype=int)
        _maze[start_i, start_j] = 0
        self._visited = set()
        self._stack = []
        self._visited.add((start_i, start_j))
        self._stack.append((start_i, start_j))

        num_iter = 0
        while len(self._stack) > 0:
            num_iter += 1
            i, j = self._stack.pop()
            _maze = self._mark_visited(_maze, i, j)
            neighbors = self._get_unvisited_neighbors(i, j)
            if len(neighbors) == 0:
                continue
            self._stack.append((i, j))
            next_i, next_j = self._pick_random_neighbor(neighbors)
            mid_i = (i + next_i) // 2
            mid_j = (j + next_j) // 2
            _maze = self._mark_visited(_maze, mid_i, mid_j)
            self._stack.append((next_i, next_j))
            _maze = self._mark_visited(_maze, next_i, next_j)

            yield _maze
        return _maze

    def _pick_start_cell(self) -> Tuple[int, int]:
        start_i = random.randrange(0, self.n_x, 2)
        return start_i, 0

    def _mark_visited(self, maze: npt.NDArray[np.int_], i: int, j: int) -> npt.NDArray[np.int_]:
        self._visited.add((i, j))
        maze[i, j] = 0
        return maze

    def _get_unvisited_neighbors(self, i: int, j: int) -> List[Tuple[int, int]]:
        neighbors = []
        if i >= 2:
            if not (i - 2, j) in self._visited:
                neighbors.append((i - 2, j))
        if i <= self.n_x - 3:
            if not (i + 2, j) in self._visited:
                neighbors.append((i + 2, j))
        if j >= 2:
            if not (i, j - 2) in self._visited:
                neighbors.append((i, j - 2))
        if j <= self.n_y - 3:
            if not (i, j + 2) in self._visited:
                neighbors.append((i, j + 2))
        return neighbors

    @staticmethod
    def _pick_random_neighbor(neighbors: List[Tuple[int, int]]) -> Tuple[int, int]:
        n = random.randint(0, len(neighbors) - 1)
        return neighbors[n]

    @staticmethod
    def _prepare_final(maze: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
        maze_temp = np.ones([maze.shape[0] + 1, maze.shape[1] + 1], dtype=int)
        maze_temp[1:-1, 1:-1] = maze[:-1, :-1]
        return maze_temp

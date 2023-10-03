"""Base class for maze generator."""
import abc
import random
from typing import Generator

import numpy.typing as npt
import numpy as np

from maze_utils.custom_logging import get_logger


class MazeBase(abc.ABC):
    """Abstract base for maze generator."""

    def __init__(self, n_x: int, n_y: int) -> None:
        self._logger = get_logger(class_=self)
        self.n_x = n_x
        self.n_y = n_y
        self.__maze = None
        self.__steps = []

    @property
    def maze(self) -> npt.NDArray[np.int_]:
        if self.__maze is None:
            self._generate()
        return self.__maze

    @property
    def steps(self) -> list[npt.NDArray[np.int_]]:
        if not self.__steps:
            self._generate()
        return self.__steps

    def _generate(self) -> None:
        percolates = False
        prepped_maze: npt.NDArray[np.int_] = np.array([], dtype=int)

        steps = []
        while not percolates:
            steps = []
            for maze in self._make_maze(self.n_x, self.n_y):
                prepped_maze = self._prepare_final(maze)
                steps.append(prepped_maze)
            prepped_maze = self._set_entrance(prepped_maze)
            prepped_maze = self._set_exit(prepped_maze)
            percolates = self._check_percolation(prepped_maze)

        steps.append(prepped_maze)
        self.__steps = steps
        self.__maze = prepped_maze

    @abc.abstractmethod
    def _make_maze(self, n_x: int, n_y: int) -> Generator[npt.NDArray[np.int_], None, npt.NDArray[np.int_]]:
        ...

    @staticmethod
    @abc.abstractmethod
    def _prepare_final(maze: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
        ...

    def _set_entrance(self, maze: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
        self._logger.info("Setting entrance")
        while True:
            x, y = random.randint(1, maze.shape[0] - 1), 0
            if maze[x, y + 1] == 0:
                break
        maze[x, y] = 2
        return maze

    def _set_exit(self, maze: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
        self._logger.info("Setting exit")
        while True:
            x, y = random.randint(1, maze.shape[0] - 1), maze.shape[1] - 1
            if maze[x, y - 1] == 0:
                break
        maze[x, y] = 3
        return maze

    def _check_percolation(self, maze: npt.NDArray[np.int_]) -> bool:
        """Check if maze path goes from entrance to exit."""
        maze = np.where(np.greater(maze, 1), 0, maze)
        maze = np.subtract(1, maze)
        ghost = np.zeros([maze.shape[0] + 2, maze.shape[1] + 2], dtype=int)
        ghost[1:-1, 1:-1] = maze
        coords, ids = self._find_clusters(ghost)
        check = self._is_percolation(coords, ids, maze.shape[1])
        return check

    @staticmethod
    def _find_clusters(grid):
        """
        Find individual clusters (i.e. neighboring occupied cells) by iterating
        through the grid and reassigning cells' labels accordingly to their
        belonging to the same (or not) cluster

        returns:
            ids: final `array` of IDs
        """

        num_of_ones = np.count_nonzero(grid)

        # 1-D array of labels (IDs) of each occupied cell. At the beginning,
        # all labels are different and are simply counted like 0,1,2,3,...
        ids = np.arange(num_of_ones)
        # 2-D array that storing (y,x) coordinates of occupied cells
        coords = [list(x) for x in np.argwhere(grid > 0)]

        while True:
            cw = []

            for i in np.arange(ids.size):
                # extract coordinates of an i-th current cell
                y, x = coords[i]

                # If only one neighbor is occupied, we change a label of the
                # current cell to the label of that neighbor. First, we need to
                # find ID of this neighbor by its known coordinates
                if grid[y - 1][x] == 1 and grid[y][x - 1] == 0:
                    ids[i] = ids[coords.index([y - 1, x])]
                elif grid[y][x - 1] == 1 and grid[y - 1][x] == 0:
                    ids[i] = ids[coords.index([y, x - 1])]

                # if both neighbors are occupied then we assign a smaller label
                elif grid[y - 1][x] == 1 and grid[y][x - 1] == 1:
                    first_neighbor_id = ids[coords.index([y - 1, x])]
                    second_neighbor_id = ids[coords.index([y, x - 1])]
                    ids[i] = min([first_neighbor_id, second_neighbor_id])

                    # if IDs are unequal then we store them to correct later
                    if first_neighbor_id != second_neighbor_id:
                        cw.append([first_neighbor_id, second_neighbor_id])

            # quit the _loop if there are no more wrong labels
            if not cw:
                break
            # else correct labels
            else:
                for id1, id2 in cw:
                    wrong_id = max([id1, id2])
                    correct_id = min([id1, id2])
                    ids[ids == wrong_id] = correct_id

        return coords, ids

    @staticmethod
    def _is_percolation(coords, ids, grid_x_dimension) -> bool:
        """
        Define whether there is a percolation in the given grid and what its type.
        Correctly works only if the find_clusters() function were called before
        """
        clusters_coordinates = []
        for idx in np.unique(ids):
            clusters_coordinates.append([coords[k] for k in range(len(ids)) if ids[k] == idx])

        # search for percolated cluster(s)
        for cluster in clusters_coordinates:
            cluster_ = np.array(cluster).T
            if (1 in cluster_[1]) and (grid_x_dimension in cluster_[1]):
                return True
        return False

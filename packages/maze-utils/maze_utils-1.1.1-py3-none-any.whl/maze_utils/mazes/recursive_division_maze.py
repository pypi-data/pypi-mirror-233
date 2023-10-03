from random import random, randint
from typing import Generator, Tuple

import numpy as np
import numpy.typing as npt

from .base import MazeBase


class RecursiveDivisionMaze(MazeBase):
    """Make maze using recursive algorithm."""

    def __init__(self, n_x: int, n_y: int) -> None:
        super().__init__(n_x, n_y)
        self._maze = np.full([n_x, n_y], 0, dtype=int)
        self._space = self._maze.copy()

    def _make_maze(self, n_x: int, n_y: int) -> Generator[npt.NDArray[np.int_], None, npt.NDArray[np.int_]]:
        self._maze = np.full([n_x, n_y], 0, dtype=int)
        self._space = self._maze.copy()
        self._maze = self._divide_space(self._space)
        yield self._maze
        return self._maze

    def _divide_space(self, space: npt.NDArray[np.int_], prev_door_index: int = 0) -> npt.NDArray[np.int_]:
        """Performe recursive division of maze and create _walls and doors."""
        # TODO: check for _walls right next to new door placement
        if random() > 0.5 and (space.shape[1] > 5):
            direction = "x"
        elif space.shape[0] > 5:
            direction = "y"
        elif space.shape[1] > 5:
            direction = "x"
        else:
            return space
        space, new_space_1, new_space_2, wall_index, door_index = self._split_space(space, direction, prev_door_index)
        new_space_1 = self._divide_space(new_space_1, door_index)
        new_space_2 = self._divide_space(new_space_2, door_index)
        final_space = self._recombine_space(space, new_space_1, new_space_2, wall_index, direction)

        return final_space

    def _recombine_space(
        self,
        space: npt.NDArray[np.int_],
        new_space_1: npt.NDArray[np.int_],
        new_space_2: npt.NDArray[np.int_],
        wall_index: int,
        direction: str,
    ) -> npt.NDArray[np.int_]:
        """Recombine split spaces into single maze _space."""
        self._check_direction_choice(direction)
        if direction == "x":
            space[:, :wall_index] = new_space_1
            space[:, wall_index + 1 :] = new_space_2
        else:
            space[:wall_index, :] = new_space_1
            space[wall_index + 1 :, :] = new_space_2
        return space

    def _split_space(
        self, space: npt.NDArray[np.int_], direction: str, prev_door_index: int
    ) -> Tuple[npt.NDArray[np.int_], npt.NDArray[np.int_], npt.NDArray[np.int_], int, int]:
        """Split maze _space into two _sections."""
        self._check_direction_choice(direction)
        wall, door = self._rand_index_wall_door(space, direction, prev_door_index)
        if direction == "x":
            space[:, wall] = 1
            space[door, wall] = 0
            new_space_1 = space[:, :wall]
            new_space_2 = space[:, wall + 1 :]
        else:
            space[wall, :] = 1
            space[wall, door] = 0
            new_space_1 = space[:wall, :]
            new_space_2 = space[wall + 1 :, :]
        return space, new_space_1, new_space_2, wall, door

    def _rand_index_wall_door(
        self, space: npt.NDArray[np.int_], direction: str, prev_door_index: int
    ) -> Tuple[int, int]:
        """Pick random _space for wall and door to be created."""
        self._check_direction_choice(direction)
        if direction == "x":
            wall_dir = 1
            door_dir = 0
        else:
            wall_dir = 0
            door_dir = 1
        # Keep wall from block door
        wall_index = prev_door_index
        max_iter = 50
        iteration = 0
        while wall_index == prev_door_index:
            wall_index = randint(2, space.shape[wall_dir] - 3)
            iteration += 1
            if iteration >= max_iter:
                break

        door_index = randint(0, space.shape[door_dir] - 1)

        return wall_index, door_index

    @staticmethod
    def _check_direction_choice(direction: str) -> None:
        """Check direction chosen is either 'x' or 'y'."""
        if direction not in ["x", "y"]:
            raise ValueError("dir must be 'x' or 'y'")

    @staticmethod
    def _prepare_final(maze: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
        """Prepare final maze with border of _walls."""
        final = np.full([maze.shape[0] + 2, maze.shape[1] + 2], 1, dtype=int)
        final[1:-1, 1:-1] = maze
        return final

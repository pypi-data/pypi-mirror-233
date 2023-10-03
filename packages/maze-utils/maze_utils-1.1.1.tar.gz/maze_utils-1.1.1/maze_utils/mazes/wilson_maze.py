import random
from typing import List, Generator, Set, Tuple, Union

import numpy as np
import numpy.typing as npt

from .base import MazeBase


class WilsonMaze(MazeBase):
    def __init__(self, n_x: int, n_y: int) -> None:
        n_x += 1
        n_y += 1
        super().__init__(n_x, n_y)
        self.n_x: int = n_x
        self.n_y: int = n_y
        self._maze = np.full([n_x, n_y], 1, dtype=int)
        self._invalid_random_cells: Set[Tuple[int, int]] = set()
        self._sections: List["MazeSection"] = []

    def _make_maze(self, n_x, n_y) -> Generator[npt.NDArray[np.int_], None, npt.NDArray[np.int_]]:
        self._maze = np.full([n_x, n_y], 1, dtype=int)
        self._invalid_random_cells: Set[Tuple[int, int]] = set()
        self._sections: List["MazeSection"] = []

        while True:
            start_cell = self._pick_random_start()
            if not start_cell:
                break
            self._walk_path(start_cell)
            self._sections = self._merge_overlapping_sections(self._sections)
            yield self._maze

        while True:
            for i, section in enumerate(self._sections):
                closest_section = section.find_closest_section(self._sections[i + 1 :])
                if not closest_section:
                    continue
                bridge = section.connect(closest_section)
                for cell in bridge:
                    self._maze[cell] = 0

            self._sections = self._merge_overlapping_sections(self._sections)
            if len(self._sections) <= 1:
                break
        yield self._maze

        return self._maze

    @staticmethod
    def _merge_overlapping_sections(sections: List["MazeSection"]):
        sec_to_remove = set()
        for i, sec_i in enumerate(sections[:-1]):
            for j, sec_j in enumerate(sections[i + 1 :]):
                if sec_i.check_overlap(sec_j):
                    sec_i.absorb(sec_j)
                    sec_to_remove.add(sec_j)
        for sec in sec_to_remove:
            sections.remove(sec)
        return sections

    def _walk_path(self, start_cell: Tuple[int, int]):
        step = 0
        current_walk = [start_cell]
        current_step = start_cell
        while True:
            step += 1
            valid_neighbors = self._list_valid_neighbors(current_step)
            if len(valid_neighbors) == 0:
                break
            next_step = self._pick_random_neighbor(valid_neighbors)
            current_walk.append(self._get_middle_step(current_step, next_step))
            current_walk.append(next_step)
            current_step = next_step
            current_walk = self._remove_loop(current_step, current_walk)
            if self._check_in_maze(current_step):
                break
            if step > self.n_x * 2:
                break
        self._sections.append(MazeSection(set(current_walk)))
        self._add_walk_to_maze(current_walk)

    def _maze_to_coord(self) -> List[Tuple[int, int]]:
        coords = []
        for i in range(self.n_x):
            for j in range(self.n_y):
                if self._maze[i, j] == 0:
                    coords.append((i, j))
        return coords

    def _pick_random_start(self) -> Union[None, Tuple[int, int]]:
        count = 0
        while True:
            cell = random.randrange(0, self.n_x, 2), random.randrange(0, self.n_y, 2)

            if self._maze[cell] == 0:
                count += 1
                # checking if selection already in maze
                self._invalid_random_cells.add(cell)
                if count > (self.n_x * 10):
                    return None
                continue
            break
        return cell

    def _list_valid_neighbors(self, current_step: Tuple[int, int]) -> List[Tuple[int, int]]:
        valid_neighbors = []
        i, j = current_step
        if i > 1:
            valid_neighbors.append((i - 2, j))
        if i < self.n_x - 2:
            valid_neighbors.append((i + 2, j))
        if j > 1:
            valid_neighbors.append((i, j - 2))
        if j < self.n_y - 2:
            valid_neighbors.append((i, j + 2))

        return valid_neighbors

    @staticmethod
    def _pick_random_neighbor(neighbors: List[Tuple[int, int]]) -> Tuple[int, int]:
        return random.choice(neighbors)

    @staticmethod
    def _get_middle_step(current_step: Tuple[int, int], next_step: Tuple[int, int]) -> Tuple[int, int]:
        avg_i = (current_step[0] + next_step[0]) // 2
        avg_j = (current_step[1] + next_step[1]) // 2
        return avg_i, avg_j

    @staticmethod
    def _remove_loop(current_step: Tuple[int, int], current_walk: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        if current_walk.count(current_step) <= 1:
            return current_walk
        first_occurance = current_walk.index(current_step)
        return current_walk[: first_occurance + 1]

    def _check_in_maze(self, current_step: Tuple[int, int]) -> bool:
        return bool(self._maze[current_step] == 0)

    def _add_walk_to_maze(self, current_walk: List[Tuple[int, int]]):
        for step in current_walk:
            self._maze[step] = 0

    @staticmethod
    def _prepare_final(maze: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
        maze_temp = np.ones([maze.shape[0] + 1, maze.shape[1] + 1], dtype=int)
        maze_temp[1:-1, 1:-1] = maze[:-1, :-1]
        return maze_temp


class MazeSection:
    def __init__(self, cells: Set[Tuple[int, int]]):
        self.cells = cells

    @property
    def center(self) -> Tuple[int, int]:
        x, y = np.average(list(self.cells), axis=0)
        return int(x), int(y)

    def absorb(self, other_section: "MazeSection") -> None:
        """Add cells of other maze section to self's cells."""
        self.cells.update(other_section.cells)

    def check_overlap(self, other_section: "MazeSection") -> bool:
        """Check if there is overlap between self and other maze section."""
        overlapping = self.cells.intersection(other_section.cells)
        return bool(overlapping)

    def connect(self, other_section: "MazeSection") -> Set[Tuple[int, int]]:
        """Create bridge of cells from self to other maze section."""
        bridge = self.get_shortest_bridge(other_section)
        self.cells.update(bridge)
        # other_section.cells.update(bridge)
        return bridge

    def get_distance_to_cell(self, cell: Tuple[int, int]) -> float:
        """Get euclidean distance from center of self to specific cell."""
        center = self.center
        distance_i = center[0] - cell[0]
        distance_j = center[1] - cell[1]
        return float((distance_i**2 + distance_j**2) ** 0.5)

    def find_closest_section(self, other_section_list: List["MazeSection"]) -> "MazeSection":
        """From a list of other _sections, find the section that is closest."""
        min_distance = -1.0
        closest_section = self
        for j, other in enumerate(other_section_list):
            distance = self.get_distance_to_center(other)
            if min_distance == -1:
                min_distance = distance
                closest_section = other
                continue
            if distance < min_distance:
                min_distance = distance
                closest_section = other
        return closest_section

    def get_distance_to_center(self, other_section: "MazeSection") -> float:
        """Get euclidean distance to other center."""
        center = self.center
        other_center = other_section.center
        distance_i = center[0] - other_center[0]
        distance_j = center[1] - other_center[1]
        return float((distance_i**2 + distance_j**2) ** 0.5)

    def get_shortest_bridge(self, other_section: "MazeSection") -> Set[Tuple[int, int]]:
        """Get a set of fewest cells that would connect self to `other_section`."""
        min_distance_i = -1.0
        closest_cell_i = (-1, -1)
        for i, cell_i in enumerate(self.cells):
            distance = other_section.get_distance_to_cell(cell_i)
            if min_distance_i == -1:
                min_distance_i = distance
                closest_cell_i = cell_i
                continue
            if distance < min_distance_i:
                min_distance_i = distance
                closest_cell_i = cell_i

        min_distance_j = -1.0
        closest_cell_j = (-1, -1)
        for j, cell_j in enumerate(other_section.cells):
            distance = self.get_distance_to_cell(cell_j)
            if min_distance_j == -1:
                min_distance_j = distance
                closest_cell_j = cell_j
                continue
            if distance < min_distance_j:
                min_distance_j = distance
                closest_cell_j = cell_j

        bridge = {closest_cell_i, closest_cell_j}
        start_i = min(closest_cell_i[0], closest_cell_j[0])
        end_i = max(closest_cell_i[0], closest_cell_j[0])
        start_j = min(closest_cell_i[1], closest_cell_j[1])
        end_j = max(closest_cell_i[1], closest_cell_j[1])
        for step_i in range(start_i, end_i + 1):
            bridge.add((step_i, start_j))
        for step_j in range(start_j, end_j + 1):
            bridge.add((end_i, step_j))

        return bridge

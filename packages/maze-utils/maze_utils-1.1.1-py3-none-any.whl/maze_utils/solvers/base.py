import abc
from operator import attrgetter
from typing import Generator, Tuple, Union, Set, List

import numpy as np
import numpy.typing as npt

from maze_utils.custom_logging import get_logger


class BaseMazeSolver(abc.ABC):
    """Abstract base for maze solver."""

    def __init__(self, maze: npt.NDArray[np.int_]) -> None:
        self._logger = get_logger(class_=self)
        self.maze = maze
        self.__solution = None
        self.__steps = []

    @property
    def solution(self) -> npt.NDArray[np.int_]:
        if self.__solution is None:
            self._generate_solution()
        return self.__solution

    @property
    def steps(self) -> list[npt.NDArray[np.int_]]:
        if not self.__steps:
            self._generate_solution()
        return self.__steps

    def _generate_solution(self) -> None:
        solution = None
        for solution in self._solve(self.maze):
            self.__steps.append(solution)
        self.__solution = solution

    @abc.abstractmethod
    def _solve(self, maze: npt.NDArray[np.int_]) -> Generator[npt.NDArray[np.int_], None, npt.NDArray[np.int_]]:
        ...

    @staticmethod
    def _optimize_open_nodes(open_nodes: Set["SolverNode"]) -> Set["SolverNode"]:
        optimal_nodes = open_nodes.copy()
        overlap_ij: List[Tuple["SolverNode", "SolverNode"]] = []
        for i, node_i in enumerate(open_nodes):
            for j, node_j in enumerate(open_nodes):
                if node_i == node_j:
                    continue
                if node_i.cell == node_j.cell:
                    overlap_ij.append((node_i, node_j))

        for node_i, node_j in overlap_ij:
            worse_node = max((node_i, node_j), key=attrgetter("g"))
            if worse_node in optimal_nodes:
                optimal_nodes.remove(worse_node)
        return optimal_nodes

    @staticmethod
    def _get_start_cell(maze: npt.NDArray[np.int_]) -> Tuple[int, int]:
        enter = np.where(maze == 2)
        return int(enter[0]), int(enter[1] + 1)

    @staticmethod
    def _get_end_cell(maze: npt.NDArray[np.int_]) -> Tuple[int, int]:
        exit_ = np.where(maze == 3)
        return int(exit_[0]), int(exit_[1] - 1)

    @staticmethod
    def _get_valid_neighbors(
        maze: npt.NDArray[np.int_], current_node: "SolverNode", closed_nodes: Set["SolverNode"]
    ) -> Set["SolverNode"]:
        neighbors = set()
        i, j = current_node.cell
        closed_cells = [node.cell for node in closed_nodes]
        end_cell = current_node.end_cell
        if (maze[i + 1, j] == 0) and (not (i + 1, j) in closed_cells):
            neighbors.add(SolverNode(current_node, (i + 1, j), end_cell))
        if (maze[i - 1, j] == 0) and (not (i - 1, j) in closed_cells):
            neighbors.add(SolverNode(current_node, (i - 1, j), end_cell))
        if (maze[i, j + 1] == 0) and (not (i, j + 1) in closed_cells):
            neighbors.add(SolverNode(current_node, (i, j + 1), end_cell))
        if (maze[i, j - 1] == 0) and (not (i, j - 1) in closed_cells):
            neighbors.add(SolverNode(current_node, (i, j - 1), end_cell))
        return neighbors

    @staticmethod
    def _check_for_end(closed_nodes: Set["SolverNode"], end_cell: Tuple[int, int]) -> Union[None, "SolverNode"]:
        for node in closed_nodes:
            if node.cell == end_cell:
                return node
        return None


class SolverNode:
    def __init__(self, parent: Union["SolverNode", None], cell: Tuple[int, int], end_cell: Tuple[int, int]) -> None:
        self.parent = parent
        self.cell = cell
        self.end_cell = end_cell

    @property
    def g(self) -> int:
        if self.parent:
            return self.parent.g + 1
        else:
            return 0

    @property
    def h(self) -> int:
        i_diff = self.end_cell[0] - self.cell[0]
        j_diff = self.end_cell[1] - self.cell[1]
        return i_diff**2 + j_diff**2

    @property
    def f(self) -> int:
        return self.g + self.h

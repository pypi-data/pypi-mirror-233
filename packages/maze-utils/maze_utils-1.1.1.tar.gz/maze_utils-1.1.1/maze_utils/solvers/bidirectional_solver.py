from typing import Generator

import numpy as np
from numpy import typing as npt

from .base import BaseMazeSolver, SolverNode


class BidirectionalDijkstraSolver(BaseMazeSolver):
    def _solve(self, maze: npt.NDArray[np.int_]) -> Generator[npt.NDArray[np.int_], None, npt.NDArray[np.int_]]:
        solution = np.copy(maze)
        start_cell = self._get_start_cell(maze)
        end_cell = self._get_end_cell(maze)

        # Forward search info
        current_f_node = SolverNode(None, start_cell, end_cell)
        open_f_nodes = {current_f_node}
        closed_f_nodes = set()

        # Backward search info
        current_b_node = SolverNode(None, end_cell, start_cell)
        open_b_nodes = {current_b_node}
        closed_b_nodes = set()

        while open_f_nodes or open_b_nodes:
            # go through dijkstra algorithm for forward search
            current_f_node = open_f_nodes.pop()
            closed_f_nodes.add(current_f_node)
            solution[current_f_node.cell] = 5
            available_f_neighbors = self._get_valid_neighbors(maze, current_f_node, closed_f_nodes)
            for f_neighbor in available_f_neighbors:
                open_f_nodes.add(f_neighbor)
            open_f_nodes = self._optimize_open_nodes(open_f_nodes)
            end_f_node = self._check_for_end(closed_f_nodes, current_b_node.cell)
            if end_f_node:
                # Only need to check one cell each time since
                # there is only one new cell added to either path in each iteration
                current_f_node = end_f_node
                break
            yield solution

            # repeat for backward search
            current_b_node = open_b_nodes.pop()
            closed_b_nodes.add(current_b_node)
            solution[current_b_node.cell] = 5
            available_b_neighbors = self._get_valid_neighbors(maze, current_b_node, closed_b_nodes)
            for b_neighbor in available_b_neighbors:
                open_b_nodes.add(b_neighbor)
            open_b_nodes = self._optimize_open_nodes(open_b_nodes)

            end_b_node = self._check_for_end(closed_b_nodes, current_f_node.cell)
            if end_b_node:
                # Only need to check one cell each time since
                # there is only one new cell added to either path in each iteration
                current_b_node = end_b_node
                break
            yield solution

        while current_f_node:
            solution[current_f_node.cell] = 6
            yield solution
            if not current_f_node.parent:
                break
            current_f_node = current_f_node.parent

        while current_b_node:
            solution[current_b_node.cell] = 6
            yield solution
            if not current_b_node.parent:
                break
            current_b_node = current_b_node.parent
        return solution

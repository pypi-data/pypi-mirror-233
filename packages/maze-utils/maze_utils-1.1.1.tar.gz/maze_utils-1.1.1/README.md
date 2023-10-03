# maze-utils

## Installation

```shell
pip install maze-utils
```

## Usage

### Maze Generator
```python
from maze_utils import mazes

generator = mazes.KruskalMaze(n_x=20, n_y=20)

# Either step by step
for step in generator.steps:
    print(step)

# Or final
print(generator.maze)

```


### Maze Solver
```python
from maze_utils import mazes, solvers

# first get maze as numpy array
maze_generator = mazes.KruskalMaze(n_x=20, n_y=20)
maze = maze_generator.maze

# Then generate solution
solver_generator = solvers.AStarSolver(maze)

# step by step
for step in solver_generator.steps:
    print(step)

# or final
print(solver_generator.solution)

```

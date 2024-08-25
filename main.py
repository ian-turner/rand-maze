import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Animation:
    def __init__(self, num_points: int):
        # setting up plot
        fig, ax = plt.subplots()
        ax.set_xlim(-.1, 1.1)
        ax.set_ylim(-.1, 1.1)
        ax.set_title('Random Maze')
        ax.set_aspect('equal')
        ax.axis('off')

        # drawing maze
        num_points = 20
        xs = np.linspace(0, 1, num_points)
        grid = np.meshgrid(xs, xs)
        vertices = np.stack([grid[0].reshape(num_points**2), grid[1].reshape(num_points**2)])

        ax.scatter(*vertices, color='black', s=5)

        self.xs = xs
        self.fig = fig
        self.ax = ax
        self.num_points = num_points
        self.vertices = vertices
        self.edges = []
        self.visited = np.zeros((num_points, num_points), dtype=int)
        self.stack = [(0, 0)]

    def update(self, frame: int):
        if len(self.stack) == 0:
            return []

        current = self.stack.pop()
        i, j = current
        self.visited[i][j] = 1
        neighbors = []
        if i > 0:
            neighbors.append((i-1, j))
        if i < self.num_points-1:
            neighbors.append((i+1, j))
        if j > 0:
            neighbors.append((i, j-1))
        if j < self.num_points-1:
            neighbors.append((i, j+1))
        
        unvisited = []
        for (_i, _j) in neighbors:
            if self.visited[_i][_j] == 0:
                unvisited.append((_i, _j))
        
        if len(unvisited) == 0:
            return []

        _next = unvisited[np.random.randint(low=0, high=len(unvisited))]
        self.edges.append((_next, current))
        self.stack.append(current)
        self.stack.append(_next)

        ax = self.ax
        xs = self.xs
        _i, _j = _next
        line, = ax.plot([xs[i], xs[_i]], [xs[j], xs[_j]], color='black')

        return [line]


def main():
    A = Animation(20)
    anim = FuncAnimation(fig=A.fig, func=A.update, frames=1000, interval=30)
    anim.save('maze.gif')


if __name__ == '__main__':
    main()

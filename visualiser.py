import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mcoll
import matplotlib.colors as mcolors
import json as js


class PointsCollection:
    def __init__(self, points=[], color=None, marker=None):
        self.points = np.array(points)
        self.color = color
        self.marker = marker


class LinesCollection:
    def __init__(self, lines=[], color=None):
        self.color = color
        self.lines = lines

    def add(self, line):
        self.lines.append(line)

    def get_collection(self):
        if self.color:
            return mcoll.LineCollection(self.lines, [mcolors.to_rgba(self.color)] * len(lines))
        else:
            return mcoll.LineCollection(self.lines)


class Plot:
    def __init__(self, points=[], lines=[], json=None):
        if json is None:
            self.points = points
            self.lines = lines
        else:
            self.points = [PointsCollection(pointsCol) for pointsCol in js.loads(json)["points"]]
            self.lines = [LinesCollection(linesCol) for linesCol in js.loads(json)["lines"]]

    def draw(self):
        ax = plt.axes()
        for collection in self.points:
            if collection.points.size > 0:
                ax.scatter(*zip(*collection.points), c=collection.color, marker=collection.marker)
        for collection in self.lines:
            ax.add_collection(collection.get_collection())
        ax.autoscale()
        plt.draw()
        plt.show()

    def toJSON(self):
        return js.dumps({"points": [pointCol.points.tolist() for pointCol in self.points],
                         "lines": [linesCol.lines for linesCol in self.lines]})


if __name__ == '__main__':
    plot = Plot([PointsCollection([(1, 2), (3, 1.5), (2, -1)]),
                 PointsCollection([(5, -2), (2, 2), (-2, -1)], color='green', marker="^")],
                [LinesCollection([[(-1, 2), (-2, 3)]])])
    plot.draw()

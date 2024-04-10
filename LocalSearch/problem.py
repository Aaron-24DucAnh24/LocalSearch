import numpy as np
import cv2
import matplotlib.pyplot as plt
from copy import deepcopy

class ImageTraversal:
    ACTIONS = np.array(["L", "R", "U", "D", "LU", "LD", "RU", "RD"])

    def __init__(self, image_uri) -> None:
        self.X, self.Y, self.space = self.load_image(image_uri)
        self.X = self.X.size
        self.Y = self.Y.size
        self.space = self.space.T

    def next(self, position):
        """
        Return list of children
        """
        for _, new_pos in self.actions(position):
            yield new_pos

    def objective_value(self, x, y):
        try:
            return self.space[x, y] 
        except:
            return None

    def actions(self, position):
        """
        @return list of available actions
        """
        for action in ImageTraversal.ACTIONS:
            next_pos = self.next_pos(position, action)
            if ImageTraversal.Position.validate(next_pos, xmax=self.X, ymax=self.Y):
                yield action, next_pos

    def next_pos(self, position, action):
        new_position = ImageTraversal.Position(
            position.x, 
            position.y, 
            position.z,
            position)
        if "L" in action: new_position.x -= 1
        if "R" in action: new_position.x += 1
        if "U" in action: new_position.y += 1
        if "D" in action: new_position.y -= 1
        new_position.z = self.objective_value(new_position.x, new_position.y)
        return new_position if new_position.z is not None else None

    def load_image(self, filename):
        # remove colors => z ranges from 0 to 255
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        # remove colors => z ranges from 0 to 
        img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        # create state space landscape
        img = cv2.GaussianBlur(img, (5, 5), 0)
        h, w = img.shape
        X = np.arange(w)
        Y = np.arange(h)
        Z = img
        return X, Y, Z

    def draw_path(self, path):
        X = np.arange(self.Y)
        Y = np.arange(self.X)
        Z = self.space
        X, Y = np.meshgrid(X, Y)
        fig = plt.figure(figsize=(8, 6))
        ax = plt.axes(projection='3d')
        # draw state space (surface)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
        # draw a polyline on the surface
        x_range = [x[1] for x in path]
        y_range = [x[0] for x in path]
        z_range = [x[2] for x in path]
        ax.plot(x_range, y_range, z_range, 'r-', zorder=3, linewidth=0.5)
        plt.show()

    def show(self):
        X = np.arange(self.Y)
        Y = np.arange(self.X)
        Z = self.space
        X, Y = np.meshgrid(X, Y)
        fig = plt.figure(figsize=(8, 6))
        ax = plt.axes(projection='3d')
        # draw state space (surface)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
        plt.show()

    class Position:
        """
        Utility class to work with the problem state
        """

        def __init__(self, x, y, z, parent = None):
            self.x = x
            self.y = y
            self.z = z
            self.parent = parent
            if x < 0 or y < 0: raise Exception(f"{x if x < 0 else y} must be non-negative")
            if not (0 <= z <= 255): raise Exception(str(z) + " must between 0 and 255 (inclusive)")

        def __lt__(self, other):
            return self.z > other.z

        @staticmethod
        def to_tuple3(position):
            return position.x, position.y, position.z

        @staticmethod
        def validate(position, xmin=0, xmax=0, ymin=0, ymax=0, zmin=0, zmax=255) -> bool:
            if position is None: return False
            if xmin <= position.x < xmax: return True
            if ymin <= position.y < ymax: return True
            if zmin <= position.z < zmax: return True
            return False

        def __str__(self):
            return f"({self.x} {self.y} {self.z})"
        
        def get_path(self):
            path = [self.to_tuple3(self)]
            curr = self.parent
            while curr is not None:
                path.append(curr.to_tuple3(curr))
                curr = curr.parent
            return path[::-1]
            

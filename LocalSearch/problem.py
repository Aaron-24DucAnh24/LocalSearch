import numpy as np
import cv2
import matplotlib.pyplot as plt

class ImageTraversal:
    ACTIONS = np.array(["L", "R", "U", "D", "LU", "LD", "RU", "RD"])
    def __init__(self, image_uri) -> None:
        self.space = self.load_image(image_uri)
        self.H, self.W = self.space.shape
            
    def next(self, position):
        """
        Return list of children
        """
        for _, new_pos in self.actions(position):
            yield new_pos
    
    def objective_value(self, x, y):
        # print(f'The space as position {x} and {y}')
        # print(f'is: {self.space[x,y]}')
        print(f'space: {self.space.shape}')
        return self.space[x, y]
    
    def actions(self, position):
        """
        @return list of available actions
        """
        for action in ImageTraversal.ACTIONS:
            next_pos = self.next_pos(position, action)
            if ImageTraversal.Position.validate(next_pos):
                yield action, next_pos

    def next_pos(self, position, action):
        if "L" in action: position.x -= 1
        if "R" in action: position.x += 1
        if "U" in action: position.y += 1
        if "D" in action: position.y -= 1
        return position
    
    def load_image(self, filename):
        # remove colors => z ranges from 0 to 255
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE) 
        # remove colors => z ranges from 0 to 
        img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25) 
        # create state space landscape
        img = cv2.GaussianBlur(img, (5, 5), 0) 
        return img 
    
    def visualize(position):
        X, Y, Z = position
        X, Y = np.meshgrid(X, Y)
        fig = plt.figure(figsize=(8,6))
        ax = plt.axes(projection='3d')
        # draw state space (surface)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
        # draw a polyline on the surface
        ax.plot(range(0, 50), range(0, 50), Z[range(0, 50), range(0, 50)], 'r-', zorder=3, linewidth=0.5)
        plt.show()
    
    class Position:
        """
        Utility class to work with the problem state
        """
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z
            if x < 0 or y < 0: raise Exception(f"{x if x < 0 else y} must be non-negative") 
            if not (0 <= z <= 255): raise Exception(str(z) + " must between 0 and 255 (inclusive)")
        
        def __lt__(self, other):
            return self.z > other.z
        
        @staticmethod
        def to_tuple3(position):
            return (position.x, position.y, position.z)
        
        @staticmethod
        def validate(position) -> bool:
            if position.x < 0: return False
            if position.y < 0: return False
            if position.z > 255 or position.z < 0: return False

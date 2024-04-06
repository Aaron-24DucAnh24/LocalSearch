import numpy as np
import matplotlib.pyplot as plt
import cv2

def load_state_space(filename):
    """
    @return:
    - X: 1-d array of values from 0 to width(image) (after scaled)
    - Y: 1-d array of values from 0 to height(image) (after scaled)
    - Z: brightness of n(th) point = (X[n], Y[n])
    """
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
    print(X)
    print(Y)
    print(Z)
    return X, Y, Z
    
def visualize(position):
    X, Y, Z = position
    X, Y = np.meshgrid(X, Y)
    fig = plt.figure(figsize=(8,6))
    ax = plt.axes(projection='3d')
    # draw state space (surface)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    # draw a polyline on the surface
    ax.plot([range(0, 50)], range(0, 50), Z[range(0, 50), range(0, 50)], 'r-', zorder=3, linewidth=0.5)
    plt.show()
    
if __name__ == "__main__":
    position = load_state_space('monalisa.jpg')
    visualize(position)
    
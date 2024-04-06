from search import RandomRestartHillClimbing
from problem import ImageTraversal
    
if __name__ == "__main__":
    inp = input("Alg: RandomRestartHillClimbing. Please input number of trial: ")
    s = RandomRestartHillClimbing(int(inp))
    p = ImageTraversal('camera.jpg')
    path = s.search(p)
    print(f"path found: {path}")
    p.draw_path(path)
from search import RandomRestartHillClimbing
from problem import ImageTraversal
    
if __name__ == "__main__":
    s = RandomRestartHillClimbing(5)
    p = ImageTraversal('monalisa.jpg')
    path = s.search(p)
    print(f"path found: {path}")
    p.visualize(path)
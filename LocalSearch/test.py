from search import RandomRestartHillClimbing
from problem import ImageTraversal
    
if __name__ == "__main__":
    s = RandomRestartHillClimbing(1)
    p = ImageTraversal('monalisa.jpg')
    path = s.search(p)
    print(path)

    
    
from search import RandomRestartHillClimbing
from problem import ImageTraversal
    
if __name__ == "__main__":
    inp = input("Alg: RandomRestartHillClimbing. Please input number of trial: ")
    search_algo = RandomRestartHillClimbing(int(inp))
    search_problem = ImageTraversal('monalisa.jpg')
    result_path = search_algo.search(search_problem)
    search_problem.show()
    search_problem.draw_path(result_path)
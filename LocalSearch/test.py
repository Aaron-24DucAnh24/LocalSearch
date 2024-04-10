from search import RandomRestartHillClimbing, SimulatedAnnealing
from problem import ImageTraversal
    
def schedule(t):
    return 1 / (t*t)

if __name__ == "__main__":
    inp = input("Alg: RandomRestartHillClimbing. Please input number of trial: ")
    search_algo = RandomRestartHillClimbing(int(inp))
    search_problem = ImageTraversal('test1_global_max.jpg')
    # result_path = search_algo.search(search_problem)
    # search_problem.show()
    # search_problem.draw_path(result_path)

    search_algo1 = SimulatedAnnealing(schedule)
    result_path1 = search_algo1.search(search_problem)
    print(result_path1)
    search_problem.show()
    search_problem.draw_path(result_path1)
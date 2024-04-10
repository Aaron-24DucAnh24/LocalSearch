from search import LocalBeamSearch
from problem import ImageTraversal
    
if __name__ == "__main__":
    inp = input("Alg: Local beam search. Please input number of beam width: ")
    search_algo = LocalBeamSearch(int(inp))
    search_problem = ImageTraversal('monalisa.jpg')
    result_path = search_algo.search(search_problem)
    search_problem.show()
    search_problem.draw_path(result_path)
from search import RandomRestartHillClimbing, SimulatedAnnealing, LocalBeamSearch, LocalSearchStrategy
from problem import ImageTraversal


def test_random_restart_hillclimbing():
    trials = int(input("Enter number of trial: "))
    return RandomRestartHillClimbing(trials)


def test_local_beam_search():
    beam_width = input("Enter beam width (default: 1): ")
    if len(beam_width) == 0:
        return LocalBeamSearch()
    return LocalBeamSearch(int(beam_width))


def test_simulated_annelling():
    return SimulatedAnnealing(schedule=lambda t: 1 / t * t)


if __name__ == "__main__":
    searcher : LocalSearchStrategy | None = None
    uri: str | None = None
    while True:
        uri = input("Enter the image URI")
        algorithm: int = int(input("""
        Enter the algorithm to use:
        1. Restart Hill Climbing
        2. Local Beam search
        3. Simulated Anneling
        """))
        if algorithm == 1:
            searcher = test_random_restart_hillclimbing()
        if algorithm == 2:
            searcher = test_local_beam_search()
        if algorithm == 3:
            searcher = test_simulated_annelling()
        if algorithm not in [1, 2, 3] or uri is None or searcher is None:
            print("Required paramters omitted!!!!")
            continue
        break
    problem: ImageTraversal = ImageTraversal(uri)
    path = searcher.search(problem=problem)
    print(path)
    problem.show()
    problem.draw_path(path)

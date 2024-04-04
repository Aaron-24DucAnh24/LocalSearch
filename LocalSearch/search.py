from problem import ImageTraversal
from abc import ABC, abstractmethod
import numpy as np
import heapq
from functools import reduce

class LocalSearchStrategy(ABC):
    @abstractmethod
    def search(self, problem: ImageTraversal) -> list[ImageTraversal.Position]: pass
    
    
class RandomRestartHillClimbing(LocalSearchStrategy):
    def __init__(self, num_trial: int):
        self.num_trial = num_trial
        
    def search(self, problem: ImageTraversal) -> list[ImageTraversal.Position]:
        return self.random_restart_hill_climbing(problem, self.num_trial)
    
    @staticmethod   
    def random_restart_hill_climbing(problem, num_trial):
        results = []
        for initial_state in RandomRestartHillClimbing.generate_random_state(problem, num_trial):
            path = RandomRestartHillClimbing.__hill_climbing(problem, initial_state)
            results.append(path)
        return reduce(lambda best, candidate: candidate if candidate[:-1][3] > best[:-1][3] else best, results)
    
    def __hill_climbing(problem, init):
        path = [init]
        while True:
            curr = path[-1]
            print(f'this is problem: {problem}')
            print(f'this is curr: {curr}')
            candidate = max(problem.next(curr), key=lambda position: position.z)
            if candidate.z > curr.z:
                path.append(candidate)
            else: break
        return list(map(lambda position: ImageTraversal.Position.to_tuple3(position), path))
    
    def generate_random_state(problem, num_trial):
        for _ in range(0, num_trial):
            y = np.random.randint(problem.W)
            x = np.random.randint(problem.H)
            yield ImageTraversal.Position(x, y, problem.objective_value(x, y))
        
   
class SimulatedAnnealing(LocalSearchStrategy):
    def __init__(self, schedule):
        self.schedule = schedule
    
    def search(self, problem: ImageTraversal) -> list[ImageTraversal.Position]:
        return self.simulated_annealing_search(problem, self.schedule)
    
    @staticmethod
    def simulated_annealing_search(problem, schedule): pass
    
class LocalBeamSearch(LocalSearchStrategy):
    def __init__(self, k = 1):
        self.beam_width = k
    
    def search(self, problem: ImageTraversal) -> list[ImageTraversal.Position]:
        return self.local_beam_search(problem, self.beam_width)
    
    @staticmethod
    def local_beam_search(problem, schedule): pass 
            
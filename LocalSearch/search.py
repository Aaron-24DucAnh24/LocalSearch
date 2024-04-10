import logging

from problem import ImageTraversal
from abc import ABC, abstractmethod
import numpy as np
from functools import reduce
import random
import math

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
            results.append(RandomRestartHillClimbing.__hill_climbing(problem, initial_state))
        return reduce(lambda best, candidate: candidate if candidate[-1][2] > best[-1][2] else best, results)

    @staticmethod
    def __hill_climbing(problem: ImageTraversal, init):
        path = [init]
        while True:
            curr = path[-1]
            candidate = max(problem.next(curr), key=lambda position: position.z)
            if candidate.z > curr.z:
                path.append(candidate)
            else:
                break
        return list(map(lambda position: ImageTraversal.Position.to_tuple3(position), path))

    @staticmethod
    def generate_random_state(problem: ImageTraversal, num_trial=1):
        for _ in range(0, num_trial):
            x = random.randint(0, problem.X - 1)
            y = random.randint(0, problem.Y - 1)
            result = ImageTraversal.Position(x, y, problem.objective_value(x, y))
            yield result


class SimulatedAnnealing(LocalSearchStrategy):
    def __init__(self, schedule):
        self.schedule = schedule

    def search(self, problem: ImageTraversal) -> list[ImageTraversal.Position]:
        return self.simulated_annealing_search(problem, self.schedule)

    @staticmethod
    def simulated_annealing_search(problem, schedule):
        init_x = np.random.randint(problem.X)
        init_y = np.random.randint(problem.Y)
        path = [ImageTraversal.Position(init_x, init_y, problem.objective_value(init_x, init_y))]
        t = 1

        while (1):
            cur = path[-1]
            T = schedule(t)
            if SimulatedAnnealing.terminate(T):
                return list(map(lambda position: ImageTraversal.Position.to_tuple3(position), path))

            succs = list(problem.next(cur))
            if succs != None:
                succ = random.choice(succs)
                deltaE = int(succ.z) - int(cur.z)
                if deltaE > 0 or SimulatedAnnealing.random(math.exp(deltaE/T)):
                    path.append(succ)

            t = t + 1

    @staticmethod
    def random(percent: float) -> bool:
        upper = 1
        while (percent < 1):
            percent = percent * 10
            upper = upper * 10

        number = random.randint(1,upper)
        middle = upper-percent
        if 1 <= number <= middle:
            return False
        return True
    
    @staticmethod
    def terminate(T: float) -> bool:
        if T < 0.01:
            return True
        return False


class LocalBeamSearch(LocalSearchStrategy):
    def __init__(self, k=1):
        self.beam_width = k

    def search(self, problem: ImageTraversal) -> list[ImageTraversal.Position]:
        return self.local_beam_search(problem, self.beam_width)

    @staticmethod
    def local_beam_search(problem, schedule): pass

import logging

from problem import ImageTraversal
from abc import ABC, abstractmethod
import numpy as np
from functools import reduce
import random

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
    def simulated_annealing_search(problem, schedule): pass


class LocalBeamSearch(LocalSearchStrategy):
    def __init__(self, k=1):
        self.beam_width = k

    def search(self, problem: ImageTraversal) -> list[ImageTraversal.Position]:
        return self.local_beam_search(problem, self.beam_width)

    @staticmethod
    def local_beam_search(problem: ImageTraversal, beam_width: int):
        x = random.randint(0, problem.X - 1)
        y = random.randint(0, problem.Y - 1)
        initial_state = ImageTraversal.Position(x, y, problem.objective_value(x, y))
        currents = [initial_state]

        while True:
            for curr in currents:
                best_successor = max(problem.next(curr), key=lambda position: position.z)
                if best_successor.z <= curr.z:
                    return curr.get_path()

            successsors: list[ImageTraversal.Position] = sum([list(problem.next(current)) for current in currents], [])
            successsors.sort(key=lambda p: p.z)
            candidates:  list[ImageTraversal.Position] = successsors[-beam_width:]
            currents = candidates

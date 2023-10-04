from dataclasses import dataclass
from typing import List


@dataclass
class GeneticIter:
    iteration : int
    score : float
    cols : List[str]
    iter_scores : List[float]

    def __str__(self):
        return f"Iteration: {self.iteration} | score {self.score} | cols {self.cols}"

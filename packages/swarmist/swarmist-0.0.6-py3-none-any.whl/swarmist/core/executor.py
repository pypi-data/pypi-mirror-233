from __future__ import annotations
from typing import Optional, List, Callable, Union
from pymonad.either import Right, Left, Either
import sys
import numpy as np
from swarmist.core.dictionary import (
    Parameters,
    SearchContext,
    Fit,
    Pos,
    SearchResults,
    AutoInteger,
    StrategyContext,
)
from swarmist.core.errors import SearchEnded
from swarmist.core.evaluator import Evaluator, Evaluation
from swarmist.core.population import Population


class SearchExecutor:
    def __init__(
        self,
        evaluator: Evaluator,
        parameters: Parameters,
        max_gen: Optional[int],
        min_fit: Optional[float],
        max_evals: Optional[int],
        population_size: Optional[int],
    ):
        self.evaluator = evaluator
        self.parameters = parameters
        self.min_fit = min_fit
        self.max_evals = max_evals
        self.population_size = self._get_population_size(population_size)
        self.max_gen = sys.maxsize if not max_gen else max_gen
        self.expected_max_gen = self._get_expected_max_gen()
        self.curr_fit: Fit = np.inf
        self.curr_pos: Pos = None
        self.curr_gen: int = 0
        self.curr_eval: int = 0
        self._results: List[Evaluation] = [Evaluation()]
        self._ended = False

    def context(self) -> SearchContext:
        return SearchContext(
            evaluate=self.evaluate,
            parameters=self.parameters,
            ndims=self.evaluator.ndims,
            bounds=self.evaluator.bounds,
            curr_gen=self.curr_gen,
            max_gen=self.expected_max_gen,
            curr_fit=self.curr_fit,
            min_fit=self.min_fit,
            curr_eval=self.curr_eval,
            max_evals=self.max_evals,
            population_size=self.population_size,
        )

    def evaluate(self, pos: Pos) -> Evaluation:
        self._assert_max_evals()
        self._assert_min_fit()
        evaluation = self.evaluator.evaluate(pos, self.context())
        self.curr_eval += 1
        self._log_result(evaluation)
        return evaluation

    def evolve(self, population: Population) -> Either[Exception, SearchResults]:
        population_results: List[List[Evaluation]] = []
        try:
            while self._next():
                population.update(self.context())
                population_results.append(
                    [Evaluation(i.pos, i.fit) for i in population._agents]
                )
        except Exception as e:
            if not isinstance(e, SearchEnded):
                return Left(e)
            self._log_result(Evaluation(self.curr_pos, self.curr_fit))
        return Right(SearchResults(best=self._results, population=population_results))

    def _log_result(self, evaluation: Evaluation):
        if evaluation.fit <= self.curr_fit:
            self.curr_fit = evaluation.fit
            self.curr_pos = evaluation.pos
            self._results[self.curr_gen] = evaluation

    def _next(self) -> bool:
        if not self._ended and self.curr_gen < self.max_gen:
            self.curr_gen += 1
            self._results.append(Evaluation(self.curr_pos, self.curr_fit))
            return True
        return False

    def _get_expected_max_gen(self) -> int:
        return (
            min(int(self.max_evals / self.population_size), self.max_gen)
            if self.max_evals and self.population_size
            else self.max_gen
        )

    def _get_population_size(
        self,
        size: Union[int, AutoInteger, Callable[[SearchContext], int]],
    ) -> int:
        if isinstance(size, AutoInteger):
            raise "Population cannot be initialized with auto integer"
        return int(size(StrategyContext(self.parameters))) if callable(size) else size

    def _assert_max_evals(self):
        if self.max_evals and self.curr_eval >= self.max_evals:
            raise SearchEnded("Maximum number of evaluations reached")

    def _assert_min_fit(self):
        if self.min_fit and self.curr_fit <= self.min_fit:
            raise SearchEnded("Fitness goal reached")

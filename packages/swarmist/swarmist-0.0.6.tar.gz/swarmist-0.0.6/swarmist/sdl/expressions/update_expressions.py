from lark import v_args
from typing import Optional, cast
from dataclasses import dataclass
from collections import OrderedDict
from swarmist.core.dictionary import Condition
from swarmist.recombination import RecombinationMethods, RecombinationMethod
from swarmist import all, filter, order, limit, roulette, random, with_probability
from .expressions import Expressions


@dataclass(frozen=True)
class UpdateTail:
    recombination: RecombinationMethod
    update_pos: OrderedDict
    when: Optional[Condition]


@v_args(inline=True)
class UpdateExpressions(Expressions):
    def replace_all_pos(self, update_pos, when=None):
        return UpdateTail(RecombinationMethods().replace_all(), update_pos, when=when)

    def recombine_pos(self, recombination, update_pos, when=None):
        return UpdateTail(recombination=recombination, update_pos=update_pos, when=when)

    def all_selection(self, size=None, order_by=None):
        return self._append_order_by_and_size(all(), order_by, size)

    def reset_pos(self, pos_generator):
        return UpdateTail(
            RecombinationMethods().replace_all(),
            OrderedDict({"pos": pos_generator}),
            when=None,
        )

    def filter_selection(self, size=None, where=None, order_by=None):
        return self._append_order_by_and_size(filter(where), order_by, size)

    def _append_order_by_and_size(self, selection, order_by, size):
        if order_by:
            selection = order_by(selection())
        if size:
            selection = limit(selection(), size)
        return selection

    def roulette_selection(self, size=None):
        return roulette(size=size)

    def random_selection(self, size=None):
        return random(size=size)

    def probabilistic_selection(self, probability, size=None):
        return with_probability(p=probability, size=size)

    def selection_size(self, size=None):
        return size

    def order_by(self, field, asc_desc=False):
        return lambda selection: order(selection, field, reverse=asc_desc)

    def reverse_order(self):
        return True

    def binomial_recombination(self, probability):
        return RecombinationMethods().binomial(cr_probability=lambda ctx: probability(ctx))

    def exponential_recombination(self, probability):
        return RecombinationMethods().exponential(cr_probability=lambda ctx: probability(ctx))

    def with_probability_recombination(self, probability):
        return RecombinationMethods().k_with_probability(probability=lambda ctx: probability(ctx))

    def random_recombination(self, size):
        k = size if callable(size) else lambda _: size
        return RecombinationMethods().k_random(k=k)

    def update_pos(self, *args):
        return OrderedDict({arg[0]: arg[1] for arg in args})

    def set_pos_var(self, value):
        return ("pos", value)

    def set_update_var(self, key, value):
        return (key, value)

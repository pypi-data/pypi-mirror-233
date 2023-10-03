import math
import numpy as np
import functools as ft
from lark import v_args
from .expressions import Expressions, fetch_value


@v_args(inline=True)
class MathExpressions(Expressions):
    def __init__(self):
        super().__init__()

    def and_(self, x, y):
        return lambda ctx=None: fetch_value(x, ctx) and fetch_value(y, ctx)

    def if_then(self, x, y, z):
        return (
            lambda ctx=None: fetch_value(y, ctx)
            if fetch_value(x, ctx)
            else fetch_value(z, ctx)
        )

    def or_(self, x, y):
        return lambda ctx=None: fetch_value(x, ctx) or fetch_value(y, ctx)

    def lt(self, x, y):
        return lambda ctx=None: np.all(
            np.less(fetch_value(x, ctx), fetch_value(y, ctx))
        )

    def le(self, x, y):
        return lambda ctx=None: np.all(
            np.less_equal(fetch_value(x, ctx), fetch_value(y, ctx))
        )

    def gt(self, x, y):
        return lambda ctx=None: np.all(
            np.greater(fetch_value(x, ctx), fetch_value(y, ctx))
        )

    def ge(self, x, y):
        return lambda ctx=None: np.all(
            np.greater_equal(fetch_value(x, ctx), fetch_value(y, ctx))
        )

    def eq(self, x, y):
        return lambda ctx=None: np.all(
            np.equal(fetch_value(x, ctx), fetch_value(y, ctx))
        )

    def ne(self, x, y):
        return lambda ctx=None: np.all(
            np.not_equal(fetch_value(x, ctx), fetch_value(y, ctx))
        )

    def add(self, x, y):
        return lambda ctx=None: np.add(fetch_value(x, ctx), fetch_value(y, ctx))

    def sub(self, x, y):
        return lambda ctx=None: np.subtract(fetch_value(x, ctx), fetch_value(y, ctx))

    def mul(self, x, y):
        return lambda ctx=None: np.multiply(fetch_value(x, ctx), fetch_value(y, ctx))

    def div(self, x, y):
        return lambda ctx=None: np.divide(fetch_value(x, ctx), fetch_value(y, ctx))

    def floordiv(self, x, y):
        return lambda ctx=None: np.floor_divide(
            fetch_value(x, ctx), fetch_value(y, ctx)
        )

    def neg(self, x):
        return lambda ctx=None: np.negative(fetch_value(x, ctx))

    def pow(self, x, y):
        return lambda ctx=None: np.power(fetch_value(x, ctx), fetch_value(y, ctx))

    def mod(self, x, y):
        return lambda ctx=None: np.mod(fetch_value(x, ctx), fetch_value(y, ctx))

    def sin(self, x):
        return lambda ctx=None: np.sin(fetch_value(x, ctx))

    def cos(self, x):
        return lambda ctx=None: np.cos(fetch_value(x, ctx))

    def tan(self, x):
        return lambda ctx=None: np.tan(fetch_value(x, ctx))

    def arcsin(self, x):
        return lambda ctx=None: np.asin(fetch_value(x, ctx))

    def arccos(self, x):
        return lambda ctx=None: np.acos(fetch_value(x, ctx))

    def arctan(self, x):
        return lambda ctx=None: np.atan(fetch_value(x, ctx))

    def sqrt(self, x):
        return lambda ctx=None: np.sqrt(fetch_value(x, ctx))

    def log(self, x):
        return lambda ctx=None: np.log(fetch_value(x, ctx))

    def exp(self, x):
        return lambda ctx=None: np.exp(fetch_value(x, ctx))

    def abs(self, x):
        return lambda ctx=None: np.abs(fetch_value(x, ctx))

    def norm(self, x):
        return lambda ctx=None: np.linalg.norm(fetch_value(x, ctx))

    def sum(self, x):
        def callback(ctx=None):
            val = fetch_value(x, ctx)
            if hasattr(val, "sum"):
                return val.sum()
            elif hasattr(val, "__len__"):
                return sum(val)
            else:
                return val

        return callback

    def count(self, x):
        def callback(ctx=None):
            val = fetch_value(x, ctx)
            if hasattr(val, "size"):
                return val.size()
            elif hasattr(val, "__len__"):
                return len(val)
            else:
                return val

        return callback

    def min(self, x):
        def callback(ctx=None):
            val = fetch_value(x, ctx)
            if hasattr(val, "min"):
                return val.min()
            elif hasattr(val, "__len__"):
                return min(val)
            else:
                return val

        return callback

    def max(self, x):
        def callback(ctx=None):
            val = fetch_value(x, ctx)
            if hasattr(val, "max"):
                return val.max()
            elif hasattr(val, "__len__"):
                return max(val)
            else:
                return val

        return callback

    def avg(self, x, weights=None):
        def callback(ctx=None):
            vals = fetch_value(x, ctx)
            w = None if weights is None else fetch_value(weights, ctx)
            if hasattr(vals, "avg"):
                return vals.avg(weights=w)
            if not hasattr(vals, "__len__"):
                return vals
            return np.average(vals,  axis=0, weights=w)
        return callback

    def repeat(self, expr, times_expr):
        def callback(ctx=None):
            n = int(times_expr(ctx))
            return [expr(ctx) for _ in range(n)]

        return callback

    def distance(self, left, right):
        def callback(ctx=None):
            x = fetch_value(left, ctx)
            y = fetch_value(right, ctx)
            if hasattr(x, "distance"):
                return x.distance(y)
            #elif hasattr(x, "__len__"):
            #    return [xi - y for xi in x]
            else:
                return x - y

        return callback

    # def reduce(self, acc, x, initial=None):
    #     def callback(ctx=None):
    #         val = fetch_value(x, ctx)
    #         if hasattr(val, "reduce"):
    #             return val.reduce(acc, initial)
    #         elif hasattr(val, "__len__"):
    #             return ft.reduce(acc, val, initial)
    #         else:
    #             return val

    #     return callback

    def pi(self):
        return lambda _=None: math.pi

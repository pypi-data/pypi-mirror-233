"""
forbiddenfp - Some builtin/itertools functions that can be chained after objects, in favor of more functional programming.

https://github.com/yx-z/forbiddenfp
"""
import collections
import functools
import itertools
import operator
from numbers import Number
from typing import Callable, List, NoReturn, Optional, Dict, TypeVar, Iterable, Sequence, Tuple, Union, Set, Type, \
    ContextManager

from forbiddenfruit import curse
from typing_extensions import ParamSpec

_P = ParamSpec("_P")
_R = TypeVar("_R")
_F = Callable[[_P], _R]
_Pred = Callable[[_P], bool]
_P2 = ParamSpec("_P2")
_R2 = TypeVar("_R2")
_ExceptionType = Type[Exception]
_ExceptionOrExceptionFunc = Union[_ExceptionType, Callable[[_P], _ExceptionType]]


def chain_as(name: str, cls: Type = object) -> Callable[[_F], _F]:
    def decorator(func: _F) -> _F:
        curse(cls, name, func)
        return func

    return decorator


def chain_for(cls: Type) -> Callable[[_F], _F]:
    def decorator(func: _F) -> _F:
        return chain_as(func.__name__, cls)(func)

    return decorator


def chainable(func: _F) -> _F:
    return chain_as(func.__name__)(func)


def as_func(val: _P) -> Callable[..., _P]:
    return lambda *args, **kwargs: val


def greater_than(val: _P) -> _Pred:
    return lambda a: a > val


chain_as("greater_than")(lambda self, val: greater_than(val)(self))


def less_than(val: _P) -> _Pred:
    return lambda a: a < val


chain_as("less_than")(lambda self, val: less_than(val)(self))


def greater_than_or_equals(val: _P) -> _Pred:
    return lambda a: a >= val


chain_as("greater_than_or_equals")(lambda self, val: greater_than_or_equals(val)(self))


def less_than_or_equals(val: _P) -> _Pred:
    return lambda a: a >= val


chain_as("less_than_or_equals")(lambda self, val: less_than_or_equals(val)(self))


def identity(val: _P) -> _P:
    return val


@chainable
def negate(val: _P) -> _R:
    return not val


@chainable
def negate_func(func: _Pred) -> _Pred:
    return lambda *args, **kwargs: not func(*args, **kwargs)


def equals(val: _P) -> _Pred:
    return lambda a: a == val


chain_as("equals")(lambda self, val: equals(val)(self))


def not_equals(val: _P) -> Callable[[Iterable[_P]], bool]:
    return lambda a: val != a


chain_as("not_equals")(lambda self, val: not_equals(val)(self))


def contains(val: _P) -> Callable[[Iterable[_P]], bool]:
    return lambda a: val in a


chain_as("contains")(lambda self, val: contains(val)(self))


def not_contains(val: _P) -> Callable[[Iterable[_P]], bool]:
    return lambda a: val not in a


chain_as("not_contains")(lambda self, val: not_contains(val)(self))

truthful = chain_as("truthful")(bool)
falseful = chain_as("falseful")(negate_func(bool))


def in_iter(it: Iterable[_P]) -> Callable[[_P], bool]:
    return lambda a: a in it


chain_as("in_iter")(lambda self, val: in_iter(val)(self))


def not_in(it: Iterable[_P]) -> Callable[[_P], bool]:
    return lambda a: a not in it


chain_as("not_in")(lambda self, val: not_in(val)(self))


@chainable
def asserting(self: _P, pred: _Pred) -> _P:
    assert pred(self)
    return self


@chainable
def is_none(val: _P) -> bool:
    return val is None


@chainable
def is_not_none(val: _P) -> bool:
    return val is not None


def add(val: _P) -> _F:
    return lambda a: a + val


chain_as("add")(lambda self, val: add(val)(self))


def subtract(val: _P) -> _F:
    return lambda a: a - val


chain_as("subtract")(lambda self, val: subtract(val)(self))


def multiply(val: _P) -> _F:
    return lambda a: a * val


chain_as("multiply")(lambda self, val: multiply(val)(self))


def divide(val: _P) -> _F:
    return lambda a: a / val


chain_as("divide")(lambda self, val: divide(val)(self))


@chainable
def and_val(self: _P, other: _P2) -> _R:
    return self and other


@chainable
def and_func(self: _Pred, other: _Pred) -> _Pred:
    return lambda *args, **kwargs: self(*args, **kwargs) and other(*args, **kwargs)


@chainable
def or_val(self: _P, other: _P2) -> _R:
    return self or other


@chainable
def or_func(self: _Pred, other: _Pred) -> _Pred:
    return lambda *args, **kwargs: self(*args, **kwargs) or other(*args, **kwargs)


@chainable
def map_val(self: _P, vals: Optional[Dict[_P, _R]] = None, default: Optional[_R] = None, **kwargs: _R) -> Optional[_R]:
    return {**(vals or {}), **kwargs}.get(self, default)


@chainable
def map_pred(self: _P, pred_to_val: Dict[_Pred, _R], default: Optional[_R] = None) -> Optional[_R]:
    for pred, val in pred_to_val.items():
        if pred(self):
            return val
    return default


@chainable
def match_val(self: _P,
              val_to_action: Optional[Dict[_P, _F]] = None,
              default: Callable[[_P], Optional[_R]] = as_func(None), **kwargs: _F) -> Optional[_R]:
    return {**(val_to_action or {}), **kwargs}.get(self, default)(self)


@chainable
def match_pred(self: _P, pred_to_action: Dict[_Pred, _R], default: _F = as_func(None)) -> Optional[_R]:
    for pred, action in pred_to_action.items():
        if pred(self):
            return action(self)
    return default(self)


def isinstance_val(t: _P) -> _Pred:
    return lambda a: isinstance(a, t)


chain_as("isinstance")(lambda self, t: isinstance_val(t)(self))


@chainable
def call(self: _F, *args: _P.args, **kwargs: _P.kwargs) -> _R:
    return self(*args, **kwargs)


@chainable
def compose(*funcs: Sequence[Callable[[_P], _R]]) -> Callable[[_P2], _R2]:
    def _compose2(f: Callable[[_R], _R2], g: _F) -> Callable[[_P], _R2]:
        return lambda *args, **kwargs: f(g(*args, **kwargs))

    return functools.reduce(_compose2, funcs)


@chainable
def compose_r(*funcs: Sequence[Callable[[_P], _R]]) -> Callable[[_P2], _R2]:
    return compose(*reversed(funcs))


@chainable
def flatten(self: List, recurse: bool = False) -> List:
    res = []
    for x in self:
        if isinstance(x, list):
            res += flatten(x, recurse=True) if recurse else x
        else:
            res.append(x)
    return res


@chainable
def partial(self: _F, *args: _P.args, **kwargs: _P.kwargs) -> _F:
    return functools.partial(self, *args, **kwargs)


@chainable
def apply(self: _P, func: _F) -> _P:
    func(self)
    return self


@chain_as("print")
def apply_print(self: _P, print_func: _F = print) -> _P:
    print_func(self)
    return self


@chainable
def print_list(self: Iterable[_P], print_func: _F = print) -> List[_P]:
    ls = list(self)
    print_func(ls)
    return ls


@chainable
def pair_val(self: _P, val: _P2) -> Tuple[_P, _P2]:
    return self, val


@chainable
def pair_func(self: _P, func: _F) -> Tuple[_P, _R]:
    return self, func(self)


@chainable
def pairwise(self: Iterable[_P]) -> Iterable[Tuple[_P, _P]]:
    return itertools.pairwise(self)


@chainable
def also(self: _P, _: _R) -> _P:
    # side effect is evaluated before passing in to this function
    return self


@chainable
def then(self: _P, func: _F) -> _R:
    return func(self)


@chainable
def then_use(self: _P, val: _R) -> _R:
    return val


@chain_as("setattr")
def set_attr(self: _P, **kwargs: _P.kwargs) -> _P:
    for k, v in kwargs.items():
        setattr(self, k, v)
    return self


@chainable
def setitem(self: _P, key: _P2, val: _R) -> _P:
    self[key] = val
    return self


@chainable
def apply_unpack(self: _P, func: _F) -> _R:
    func(*self)
    return self


@chainable
def then_unpack(self: _P, func: _F) -> _R:
    return func(*self)


@chainable
def empty(self: Iterable[_P]) -> bool:
    return all(False for _ in self)


@chainable
def tee(self: Iterable[_P], n: int = 2) -> Tuple[_P, ...]:
    return itertools.tee(self, n)


@chain_as("min")
def min_iter(self: Iterable[_P], key: _F = identity) -> _P:
    return min(self, key=key)


@chain_as("max")
def max_iter(self: Iterable[_P], key: _F = identity) -> _P:
    return max(self, key=key)


@chain_as("range")
def range_up_to(self: int, start: Optional[int] = None, step: Optional[int] = None) -> Iterable[int]:
    if start is None and step is None:
        return range(self)
    if step is None:
        return range(start, self)
    return range(start, self, step)


@chain_as("all")
def all_iter(self: Iterable[_P], predicate: _Pred = truthful) -> bool:
    return all(predicate(x) for x in self)


@chain_as("any")
def any_iter(self: Iterable[_P], predicate: _Pred = truthful) -> bool:
    return any(predicate(x) for x in self)


@chain_as("map")
def map_iter(self: Iterable[_P], func: _F, *other: Iterable[_P2]) -> Iterable[_R]:
    return map(func, self, *other)


@chainable
def map_dict(self: Dict[_P, _P2], key_func: _F = identity, val_func: Callable[[_P2], _R2] = identity) -> Dict[
    _R, _R2]:
    return {key_func(k): val_func(v) for k, v in self.items()}


@chain_as("filter")
def filter_iter(self: Iterable[_P], predicate: _Pred = truthful) -> Iterable[_P]:
    return filter(predicate, self)


@chainable
def filter_key(self: Dict[_P, _P2], predicate: Callable[[_P], bool]) -> Iterable[Tuple[_P, _P2]]:
    return filter(lambda t: predicate(t[0]), self.items())


@chainable
def filter_val(self: Dict[_P, _P2], predicate: Callable[[_P2], bool]) -> Iterable[Tuple[_P, _P2]]:
    return filter(lambda t: predicate(t[1]), self.items())


@chainable
def last(self: Sequence[_P], predicate: _Pred = as_func(True)) -> Optional[_P]:
    return next(filter(predicate, reversed(self)), None)


@chain_as("next")
def next_iter(self: Iterable[_P], predicate: _Pred = as_func(True)) -> Optional[_P]:
    return next(filter(predicate, self), None)


@chain_as("sum")
def sum_iter(self: Iterable[_P], of: Callable[[_P], Number] = identity, predicate: _Pred = truthful) -> int:
    return sum(map(of, filter(predicate, self)))


@chain_as("len")
def len_iter(self: Iterable[_P], predicate: _Pred = truthful) -> int:
    return sum(map(lambda _: 1, filter(predicate, self)))


@chain_as("reversed")
def reversed_iter(self: Sequence[_P]) -> Sequence[_P]:
    return reversed(self)


@chain_as("sorted")
def sorted_iter(self: Iterable[_P], key: _F = identity, reverse: bool = False) -> List[_P]:
    return sorted(self, key=key, reverse=reverse)


@chainable
def reduce(self: Iterable[_P], func: Callable[[_P, _P], _R], initial: Optional[_R] = None) -> _R:
    return functools.reduce(func, self, initial) if initial is not None else functools.reduce(func, self)


@chainable
def reduce_r(self: Iterable[_P], func: Callable[[_P, _P], _R], initial: Optional[_R] = None) -> _R:
    rev = reversed(self)
    return functools.reduce(func, rev, initial) if initial is not None else functools.reduce(func, rev)


@chainable
def separate(self: Iterable[_P], predicate: _Pred = truthful) -> Tuple[List[_P], List[_P]]:
    true_part = []
    false_part = []
    for x in self:
        (true_part if predicate(x) else false_part).append(x)
    return true_part, false_part


@chainable
def counter(self: Iterable[_P]) -> Dict[_P, int]:
    return collections.Counter(self)


@chainable
def groupby(self: Iterable[_P], key: _F) -> Dict[_R, List[_P]]:
    return itertools.groupby(self, key=key)


@chainable
def chain(*self: Iterable[Iterable[_P]]) -> Iterable[_P]:
    return itertools.chain(*self)


@chain_as("zip")
def zip_iter(*self: Iterable[_P]) -> Iterable[Tuple[_P, ...]]:
    return zip(*self)


@chain_as("enumerate")
def enumerate_iter(self: Iterable[_P]) -> Iterable[Tuple[int, _P]]:
    return enumerate(self)


@chain_as("tuple")
def tuple_iter(self: Iterable[_P]) -> Tuple[_P, ...]:
    return tuple(self)


@chain_as("list")
def list_iter(self: Iterable[_P]) -> List[_P]:
    return list(self)


@chain_as("set")
def set_iter(self: Iterable[_P]) -> Set[_P]:
    return set(self)


@chain_as("dict")
def dict_iter(self: Iterable[Tuple[_P, _P2]]) -> Dict[_P, _P2]:
    return dict(self)


@chainable
def join(self: Iterable[_P], sep: str = "", to_str: Callable[[_P], str] = str) -> str:
    return sep.join(map(to_str, self))


@chainable
def starmap(self: Iterable[Iterable[_P]], func: Callable[[_P.args], _R]) -> Iterable[_R]:
    return itertools.starmap(func, self)


@chainable
def each_also(self: Sequence[Sequence[_P]], func: Callable[[Iterable[_P]], _R]) -> Sequence[Sequence[_P]]:
    for x in self:
        func(x)
    return self


@chainable
def each_also_unpacked(self: Sequence[Sequence[_P]], func: Callable[[_P.args], _R]) -> Sequence[Sequence[_P]]:
    for x in self:
        func(*x)
    return self


@chainable
def each(self: Iterable[Iterable[_P]], func: Callable[[Iterable[_P]], _R]) -> None:
    for x in self:
        func(x)


@chainable
def each_unpacked(self: Iterable[Iterable[_P]], func: Callable[[_P.args], _R]) -> None:
    for x in self:
        func(*x)


@chainable
def accumulate(self: Iterable[Iterable[_P]], func: Callable[[_R, _P], _R] = operator.add,
               initial: Optional[_R] = None) -> Iterable[_R]:
    return (itertools.accumulate(self, func, initial=initial) if initial is not None
            else itertools.accumulate(self, func))


@chainable
def pairwise(self: Iterable[_P]) -> Iterable[Tuple[_P, _P]]:
    return itertools.pairwise(self)


@chainable
def product(self: Iterable[_P], repeat: int = 1) -> Iterable[Tuple[_P, ...]]:
    return itertools.product(*self, repeat=repeat)


@chainable
def repeat(self: _P, times: Optional[int] = None) -> Iterable[_P]:
    return itertools.repeat(self, times)


@chainable
def inifinite(self: _P) -> Iterable[_P]:
    return itertools.repeat(self, None)


@chainable
def cycle(self: _P) -> Iterable[_P]:
    return itertools.cycle(self)


@chainable
def takewhile(self: Iterable[_P], predicate: _Pred = truthful) -> Iterable[_P]:
    return itertools.takewhile(predicate, self)


@chainable
def islice_up_to(self: Iterable[_P], stop: int, predicate: _Pred = as_func(True)) -> Iterable[_P]:
    return itertools.islice(filter(predicate, self), stop)


@chainable
def islice(
        self: Iterable[_P], start: int, stop: Optional[int], step: int = 1, predicate: _Pred = as_func(True)
) -> Iterable[_P]:
    return itertools.islice(filter(predicate, self), start, stop, step)


@chainable
def dropwhile(self: Iterable[_P], predicate: _Pred = truthful) -> Iterable[_P]:
    return itertools.dropwhile(predicate, self)


@chain_as("float")
def float_obj(self: _P) -> float:
    return float(self)


@chain_as("int")
def int_obj(self: _P) -> int:
    return int(self)


@chain_as("str")
def str_obj(self: _P) -> str:
    return str(self)


@chain_as("repr")
def repr_obj(self: _P) -> str:
    return repr(self)


@chain_as("format")
def format_obj(self: _P, format_str: str) -> str:
    return format(self, format_str)


@chainable
def if_branches(self: _P, true_func: _F, false_func: _F, predicate: _Pred = truthful) -> _R:
    return true_func(self) if predicate(self) else false_func(self)


@chainable
def if_true(self: _P, func: _F, predicate: _Pred = truthful) -> Optional[_R]:
    return func(self) if predicate(self) else None


@chainable
def if_false(self: _P, func: _F, predicate: _Pred = truthful) -> Optional[_R]:
    return func(self) if not predicate(self) else None


@chainable
def or_else(self: _P, val: _R, predicate: _Pred = truthful) -> _R:
    return self if predicate(self) else val


@chainable
def or_eval(self: _P, func: _F, predicate: _Pred = truthful) -> _R:
    return self if predicate(self) else func(self)


@chainable
def or_raise(self: _P, val_or_func: _ExceptionOrExceptionFunc, predicate: _Pred = truthful) -> _P:
    if predicate(self):
        return self
    if callable(val_or_func):
        raise val_or_func(self)
    raise val_or_func


@chainable
def raise_as(self: _P, val_or_func: _ExceptionOrExceptionFunc) -> NoReturn:
    if callable(val_or_func):
        raise val_or_func(self)
    raise val_or_func


@chainable
def then_suppressed(
        self: _P, func: _F, exception_type: _ExceptionType = Exception, on_except: Optional[_R] = None
) -> Optional[_R]:
    try:
        return func(self)
    except exception_type:
        return on_except


@chainable
def apply_suppressed(self: _P, func: _F, exception_type: _ExceptionType = Exception) -> _P:
    try:
        func(self)
    except exception_type:
        pass
    finally:
        return self


@chainable
def then_catch(self: _P, func: _F, exception_type: _ExceptionType = Exception,
               exception_handler: Callable[[_P, _ExceptionType], _R2] = as_func(None)) -> Union[_R, _R2]:
    try:
        return func(self)
    except exception_type as e:
        return exception_handler(self, e)


@chainable
def apply_catch(self: _P, func: _F, exception_type: _ExceptionType = Exception,
                exception_handler: Optional[Callable[[_P, _ExceptionType], _R2]] = None) -> _P:
    try:
        func(self)
    except exception_type as e:
        if exception_handler is not None:
            exception_handler(self, e)
    finally:
        return self


@chainable
def apply_while(self: _P, func: Callable[[_P], _P], predicate: _Pred = truthful) -> _P:
    while predicate(self):
        self = func(self)
    return self


@chainable
def yield_while(self: _P, func: Callable[[_P], _P], predicate: _Pred = truthful) -> Iterable[_P]:
    while predicate(self):
        yield self
        self = func(self)


@chainable
def with_context(self: _P, context_func: Callable[[_P], ContextManager],
                 then: Union[Callable[[_P, _R], _R2], Callable[[_P], _R2]]) -> _R2:
    with context_func(self) as r:
        if r is None:
            return then(self)
        return then(self, r)


def take_unpacked(
        func_on_iterable_of_iterable: Callable[[Callable[[Iterable[_P]], _R], Iterable[Iterable[_P]]], _R2]
) -> Callable[[Callable[[_P.args], _R], Iterable[Iterable[_P]]], _R2]:
    """
    e.g.
    filter(lambda tup: tup[0] > tup[1], [(1, 2), (3, 2)]
    can be transformed so that it takes a predicate with two arguments (for clarity):
    take_unpacked(filter)(lambda x, y: x > y, [(1, 2), (3, 2)])
    """

    @functools.wraps(func_on_iterable_of_iterable)
    def decorated(func: Callable[[_P.args], _R], iterable_of_iterable: Iterable[Iterable[_P]]) -> _R2:
        return func_on_iterable_of_iterable(lambda args: func(*args), iterable_of_iterable)

    return decorated

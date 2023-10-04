from contextlib import AbstractContextManager, contextmanager
from inspect import isgeneratorfunction
from typing import (
    Any,
    Callable,
    ContextManager,
    Generator,
    Generic,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)

INITIAL_T = TypeVar("INITIAL_T")
FINAL_T = TypeVar("FINAL_T")

NEW_FINAL_T = TypeVar("NEW_FINAL_T")


T = TypeVar("T")
J = TypeVar("J")
PREDICATE = Callable[[T], bool]


TRANSFORMER = Callable[[T], J]
GENERATOR_TRANSFORMER = Callable[[T], Generator[J, Any, Any]]
# CONTEXT_MANAGER_TRANSFORMER = Callable[[T], AbstractContextManager[J]]


INPUT_TRANSFORMER = Union[
    TRANSFORMER[INITIAL_T, FINAL_T],
    GENERATOR_TRANSFORMER[INITIAL_T, FINAL_T],
    # CONTEXT_MANAGER_TRANSFORMER[T, J],
]
# Callable[[T], Union[J, AbstractContextManager[J]]]


class Pipe(Generic[INITIAL_T, FINAL_T]):
    def __init__(self, func: INPUT_TRANSFORMER[INITIAL_T, FINAL_T]) -> None:
        self.func = func

    def __rshift__(
        self, other: TRANSFORMER[FINAL_T, NEW_FINAL_T]
    ) -> "Pipe[INITIAL_T, NEW_FINAL_T]":
        return self.pipe(other)

    def __call__(self, value: INITIAL_T) -> FINAL_T:
        if isgeneratorfunction(self.func):
            casted_func = cast(GENERATOR_TRANSFORMER[INITIAL_T, FINAL_T], self.func)
            cxt_mgr = contextmanager(casted_func)
            with cxt_mgr(value) as result:
                return result

        else:
            result_or_context = self.func(value)
            if isinstance(result_or_context, AbstractContextManager):
                casted_result_or_context = cast(
                    ContextManager[FINAL_T], result_or_context
                )
                with casted_result_or_context as v:
                    return v

            return cast(FINAL_T, result_or_context)

    def pipe(
        self, other: INPUT_TRANSFORMER[FINAL_T, NEW_FINAL_T]
    ) -> "Pipe[INITIAL_T, NEW_FINAL_T]":
        def _pipe(value: INITIAL_T) -> NEW_FINAL_T:
            result = other(self(value))
            if isinstance(result, AbstractContextManager):
                casted_result = cast(ContextManager[NEW_FINAL_T], result)
                with casted_result as v:
                    return v
            return cast(NEW_FINAL_T, result)

        return Pipe(_pipe)


def pattern_match(
    cases: Tuple[Tuple[PREDICATE[T], TRANSFORMER[T, J]], ...],
    default: Optional[TRANSFORMER[T, J]] = None,
) -> Pipe[T, J]:
    @Pipe
    def _pattern_match(value: T) -> J:
        for case, transform in cases:
            if case(value):
                return transform(value)

        if default is not None:
            return default(value)
        raise ValueError("No case matched")

    return _pattern_match

from typing import Callable, Type, TypeVar

from vedro import Scenario

__all__ = ("screenshot_asserts",)


T = TypeVar("T", bound=Type[Scenario])


class screenshot_asserts:
    def __init__(self, *, skip_if: Callable[[], bool] | None = None) -> None:
        self._skip_if = skip_if

    def __call__(self, scn: T) -> T:
        assert issubclass(scn, Scenario)
        setattr(scn, "__vedro__screenshot_asserts__", True)
        skip = self._skip_if() if self._skip_if else False
        setattr(scn, "__vedro__screenshot_asserts_skip__", skip)
        return scn

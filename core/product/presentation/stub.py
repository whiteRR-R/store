from typing import Callable, Any

class Stub:
    def __init__(self, dependency: Callable[..., Any]) -> None:
        self._dependency = dependency

    def __call__(self) -> None:
        print(self._dependency)
        raise NotImplementedError(f"You forgot to register `{self._dependency}` implementation.")

    def __hash__(self) -> int:
        return hash(self._dependency)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Stub):
            return self._dependency == __value._dependency
        else:
            return self._dependency == __value

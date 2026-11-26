from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    """Abstract base class shared by every processor of the Nexus."""

    def __init__(self) -> None:
        self._storage: list[tuple[int, str]] = []
        self._processed: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Tell whether this processor can ingest the given data."""

    @abstractmethod
    def ingest(self, data: Any) -> None:
        """Process the given data (raises ValueError if it is invalid)."""

    def output(self) -> tuple[int, str]:
        """Extract the oldest stored item with its processing rank."""
        if not self._storage:
            raise IndexError(
                f"{type(self).__name__}: no data available to output"
            )
        return self._storage.pop(0)

    def _store(self, item: str) -> None:
        """Keep one item, tagged with its rank in this processor."""
        self._storage.append((self._processed, item))
        self._processed += 1

    @property
    def processed(self) -> int:
        """Total number of items ingested so far."""
        return self._processed

    @property
    def remaining(self) -> int:
        """Number of items still waiting to be output."""
        return len(self._storage)


class NumericProcessor(DataProcessor):
    """Ingests int, float and lists of both (mixed lists allowed)."""

    @staticmethod
    def _is_number(value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(self._is_number(item) for item in data)
        return self._is_number(data)

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError(f"NumericProcessor cannot ingest: {data!r}")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(str(item))


class TextProcessor(DataProcessor):
    """Ingests str and lists of str."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return isinstance(data, str)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError(f"TextProcessor cannot ingest: {data!r}")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(item)


class LogProcessor(DataProcessor):
    """Ingests dicts of str -> str and lists of such dicts."""

    @staticmethod
    def _is_log(value: Any) -> bool:
        return isinstance(value, dict) and all(
            isinstance(k, str) and isinstance(v, str)
            for k, v in value.items()
        )

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(self._is_log(item) for item in data)
        return self._is_log(data)

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError(f"LogProcessor cannot ingest: {data!r}")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(", ".join(f"{k}: {v}" for k, v in item.items()))


def main() -> None:
    print("=== Code Nexus - Data Processor ===")
    processors: list[DataProcessor] = [
        NumericProcessor(), TextProcessor(), LogProcessor()
    ]
    numeric, text, log = processors

    print("\nTesting validate:")
    samples: list[Any] = [
        42, 3.14, [1, 2.5, 3], "hello", ["a", "b"],
        {"level": "INFO", "msg": "ok"}, [{"level": "WARN", "msg": "hot"}],
        [1, "x"], {"level": 1}, None,
    ]
    for proc in processors:
        print(f"{type(proc).__name__}:")
        for sample in samples:
            print(f"  validate({sample!r}) -> {proc.validate(sample)}")

    print("\nTesting ingest without validation (invalid data):")
    try:
        numeric.ingest("not a number")
    except ValueError as error:
        print(f"  Exception raised as expected: {error}")

    print("\nIngesting data:")
    numeric.ingest(42)
    numeric.ingest([1, 2.5, 3])
    text.ingest("hello")
    text.ingest(["nexus", "stream"])
    log.ingest({"level": "INFO", "msg": "system online"})
    log.ingest([{"level": "WARN", "msg": "heat"}, {"level": "ERROR"}])

    print("\nExtracting data with output:")
    for proc in processors:
        print(f"{type(proc).__name__}:")
        while proc.remaining:
            rank, value = proc.output()
            print(f"  rank {rank}: {value}")
        try:
            proc.output()
        except IndexError as error:
            print(f"  Empty processor: {error}")


if __name__ == "__main__":
    main()

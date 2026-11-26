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


class DataStream:
    """Routes every element of a stream to a processor able to handle it."""

    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            for proc in self._processors:
                if not proc.validate(element):
                    continue
                try:
                    proc.ingest(element)
                except ValueError as error:
                    print(f"DataStream error - ingestion failed: {error}")
                break
            else:
                print(
                    "DataStream error - Can't process element in stream: "
                    f"{element!r}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor registered.")
            return
        for proc in self._processors:
            print(
                f"{type(proc).__name__}: total {proc.processed} items "
                f"processed, remaining {proc.remaining} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Polymorphic Data Stream ===")
    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()

    stream = DataStream()
    stream.register_processor(numeric)
    stream.register_processor(text)
    stream.register_processor(log)

    batch: list[Any] = [
        "Hello Nexus", 42, [1, 2.5, 3], ["alpha", "beta"],
        {"level": "INFO", "msg": "stream online"},
        [{"level": "WARN", "msg": "overheat"}],
        3.14, [1, "mixed"], None, {"level": 1}, "end of stream",
    ]
    print(f"\nProcessing stream of {len(batch)} elements...")
    stream.process_stream(batch)

    print()
    stream.print_processors_stats()

    print("\nConsuming 2 elements from each processor:")
    for proc in (numeric, text, log):
        for _ in range(2):
            if proc.remaining:
                rank, value = proc.output()
                print(f"{type(proc).__name__} -> rank {rank}: {value}")

    print()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()

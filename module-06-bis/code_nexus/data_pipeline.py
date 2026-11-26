from abc import ABC, abstractmethod
from typing import Any, Protocol


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


class ExportPlugin(Protocol):
    """Structural contract: anything with this method is a valid plugin."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    """Prints the data as CSV (rank,data)."""

    @staticmethod
    def _cell(value: str) -> str:
        if any(c in value for c in ',"\n\r'):
            return '"' + value.replace('"', '""') + '"'
        return value

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        print("rank,data")
        for rank, value in data:
            print(f"{rank},{self._cell(value)}")


class JSONExportPlugin:
    """Prints the data as a JSON array of {"rank", "data"} objects."""

    @staticmethod
    def _escape(value: str) -> str:
        out = []
        for char in value:
            if char == '"':
                out.append('\\"')
            elif char == "\\":
                out.append("\\\\")
            elif char == "\n":
                out.append("\\n")
            elif char == "\r":
                out.append("\\r")
            elif char == "\t":
                out.append("\\t")
            elif ord(char) < 0x20:
                out.append(f"\\u{ord(char):04x}")
            else:
                out.append(char)
        return "".join(out)

    def process_output(self, data: list[tuple[int, str]]) -> None:
        items = [
            f'{{"rank": {rank}, "data": "{self._escape(value)}"}}'
            for rank, value in data
        ]
        print("JSON Output:")
        print("[" + ", ".join(items) + "]")


class DataStream:
    """Routes stream elements to processors and exports their output."""

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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        """Consume up to nb items per processor and export them."""
        for proc in self._processors:
            batch: list[tuple[int, str]] = []
            while len(batch) < nb and proc.remaining > 0:
                batch.append(proc.output())
            if not batch:
                continue
            print(f"Exporting {len(batch)} item(s) from "
                  f"{type(proc).__name__}")
            try:
                plugin.process_output(batch)
            except Exception as error:
                print(f"DataStream error - export failed: {error}")


class ConsolePlugin:
    """Not related to ExportPlugin by inheritance: duck typing only."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("Console Output:")
        for rank, value in data:
            print(f"  #{rank} {value}")


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    stream = DataStream()
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    batch: list[Any] = [
        "Hello, \"Nexus\"", 42, [1, 2.5, 3], ["alpha", "line\nbreak"],
        {"level": "INFO", "msg": "pipeline online"},
        [{"level": "WARN", "msg": "overheat"}],
        3.14, [1, "mixed"], None, "end of stream",
    ]
    print(f"\nProcessing stream of {len(batch)} elements...")
    stream.process_stream(batch)
    print()
    stream.print_processors_stats()

    print("\n--- Pipeline: 2 items per processor -> CSV ---")
    stream.output_pipeline(2, CSVExportPlugin())

    print("\n--- Pipeline: 2 items per processor -> JSON ---")
    stream.output_pipeline(2, JSONExportPlugin())

    print("\n--- Pipeline: 5 items per processor -> duck-typed plugin ---")
    stream.output_pipeline(5, ConsolePlugin())

    print()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()

from pathlib import Path
import threading
import time
from typing import Any, Callable, Iterable

import toolong.watcher
import toolong.log_file


class CsvWatcher:
    def __init__(
        self,
        path: Path | str,
        line_callback: Callable | None = None,
        fieldnames: Iterable[str] | None = None,
    ):
        self._path = Path(path).expanduser().resolve()
        self._line_callback = line_callback or self.default_line_callback
        self._watcher = toolong.watcher.get_watcher()
        self._log_file = toolong.log_file.LogFile(
            path=self._path.__fspath__()
        )
        self._log_file.open(exit_event=threading.Event())
        
        self._file_index = 0
        """Current read index of file"""

        self._lines = 0
        """Total number of lines (includeing blank/unparsable)"""

        self._parsed_lines = 0
        """Total number of lines that are not blank AND are parsable"""

        self.fieldnames = list(fieldnames or self._get_fieldnames())

        # Have to iterate over this result for side effecrts, but don't need to do anything else
        for _ in self._log_file.scan_line_breaks():
            pass

        self._watcher.add(
            log_file=self._log_file,
            callback=self._process_file_callback,
            error_callback=None
        )

    def _get_fieldnames(self) -> list[str]:
        # TODO
        return []

    def default_line_callback(self):
        pass

    def _process_single_line(self, raw: bytes) -> dict[str, Any] | None:
        self._lines += 1
        line = raw.decode(encoding="utf8").strip("\r\n")
        if not line:
            return
        self._parsed_lines += 1
        print(f"{line=} [{self._lines}] [{self._parsed_lines=}]")
        pass

    def _process_file_callback(self, index: int, line_break_indexes: list[int]) -> None:
        print(f"_process_file_callback {index=}, {line_break_indexes=}, {self._file_index=}")
        if line_break_indexes:
            for line_break_index in line_break_indexes:
                chunk = self._log_file.get_raw(self._file_index, line_break_index)
                self._file_index = line_break_index
                self._process_single_line(chunk)
        chunk = self._log_file.get_raw(self._file_index, index)
        # print(f"{chunk=}")
        self._file_index = index
        self._process_single_line(chunk)


if __name__ == "__main__":
    watcher = CsvWatcher(Path("./unix.csv"))
    watcher._watcher.start()
    pass

import threading

import toolong.watcher
import toolong.log_file

watcher = toolong.watcher.get_watcher()

print(watcher)
print(type(watcher))

# file_path = "./sample.log"
# with open(file_path, "rb") as raw_file:
log_file = toolong.log_file.LogFile("./sample.log")

log_file.open(exit_event=threading.Event())

print(log_file)
print(type(log_file))

previous_index: int = 0
previous_index: int = log_file.size
print(f"Initial size={previous_index}")

def callback(index, *args, **kwargs) -> None:
    global previous_index
    print(f"callback: {previous_index=} {index=} {args=} {kwargs=}")
    line_bytes = log_file.get_raw(previous_index, index)
    line = line_bytes.decode(encoding="utf8")
    stripped_line = line.strip("\r\n")
    print(f"{line_bytes=}")
    print(f"{line=!r}")
    print(f"{stripped_line=!r}")
    previous_index = index

def error_callback(*args, **kwargs) -> None:
    print(f"error_callback: {args=} {kwargs=}")

log_file

watcher.add(
    log_file=log_file,
    callback=callback,
    error_callback=error_callback,
)
print(f"Starting watcher")
watcher.start()
print(f"After Starting watcher")


# import csv

# csv.DictReader()
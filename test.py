from dataclasses import dataclass


@dataclass
class Task:
    name: str
    action: str
    content: dict[str, str]
    start_date: str
    start_time: str
    repeat_every: dict[str, int]
    next_run_time: str | None

task = Task("test", "test", {"test": "test"}, "test", "test", {"test": 1}, "test")
task.aaaaaaaaaaaaaaaaaa()
print(task.__dict__)

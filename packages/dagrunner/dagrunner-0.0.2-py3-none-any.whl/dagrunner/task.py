"""Task class"""
from typing import Callable
from time import perf_counter

from libs.constants import SUCCESS, FAILED


class Task:
    """Task class"""
    def __init__(self, name: str, executable: Callable) -> None:
        self.name = name
        self.executable = executable

    def __repr__(self):
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __gt__(self, other):
        if isinstance(other, Task):
            other.dependencies = set()
            other.dependencies.add(Task)
        elif isinstance(other, list):
            for task in other:
                task.dependencies.add(self)
        return other

    def run_task(self, dag, execution_times, errors, semaphore):
        """Run task"""
        semaphore.acquire()
        start = perf_counter()
        try:
            self.executable()
            result = SUCCESS
        except Exception as exc:
            errors[self.name] = repr(exc)
            result = FAILED
        end = perf_counter()
        execution_times[self.name] = round(end - start, 3)
        semaphore.release()

        dag.task_complete_signal(self.name, result)

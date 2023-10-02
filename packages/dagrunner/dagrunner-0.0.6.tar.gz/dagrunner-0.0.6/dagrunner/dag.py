"""DAG class"""
from multiprocessing import Process, Semaphore
from time import perf_counter

from networkx import DiGraph

from dagrunner.task import Task
from dagrunner.utils.logger import Logger
from dagrunner.libs.constants import TRIGGERED_TASKS, COMPLETED_TASKS, ABORTED_TASKS, FAILED_TASKS, SUCCESS, FAILED

logger = Logger()


class Dag:
    """DAG class"""
    def __init__(self, name, sequence) -> None:
        self.name: str = name
        self.sequence = sequence
        self.semaphore: Semaphore = None
        self.eligible_tasks: list[Task] = []
        self.execution_times: dict = {}
        self.errors: dict = {}
        self.exec_data: dict = {}
        self.tasks_dict: dict =  {}
        self.graph: DiGraph = None

    def __get_tasks_with_no_dependencies(self) -> list[Task]:
        """Get tasks not dependent on any other task"""
        return [task for task in self.graph.nodes() if not any(self.graph.predecessors(task))]

    def __get_dependants_of_task(self, task: Task) -> list[Task]:
        """Get next dependants of task"""
        return list(self.graph.successors(task))

    def __mark_task_as_triggered(self, task) -> None:
        """Mark experiment as triggered"""
        self.exec_data[TRIGGERED_TASKS] |= {task}
        logger.debug(f"* `{task}` triggered successfully")

    def __are_all_dependencies_complete(self, task) -> dict:
        """Check if all dependencies of task are complete"""
        return self.tasks_dict[task].dependencies.issubset(self.exec_data[COMPLETED_TASKS])

    def __get_all_dependants_of_task_recursively(self, task) -> set:
        """Get all dependants of task including dependants of dependants"""
        successors = []
        for node in self.graph.successors(task):
            successors.append(node)
            successors.extend(list(self.graph.successors(node)))
        self.exec_data[ABORTED_TASKS] |= set(successors)
        return set(successors)

    def __mark_task_as_succeeded_or_failed(self, task, result) -> None:
        """Mark task as succeeded or failed based on result"""
        if result == SUCCESS:
            self.exec_data[COMPLETED_TASKS] |= {task}
        elif result == FAILED:
            self.exec_data[FAILED_TASKS] |= {task}
        logger.debug(f"* `{task}` finished execution successful")

    def task_complete_signal(self, task, result):
        """Run procedure to be completed after completion of task"""
        self.__mark_task_as_succeeded_or_failed(task, result)
        if result == SUCCESS:
            logger.success(f"* `{task}` executed successfully")
            dependants = self.__get_dependants_of_task(task)
            for dependant in dependants:
                if self.__are_all_dependencies_complete(task):
                    logger.debug(f"* {dependant} starting execution as dependencies are complete")
                    self.eligible_tasks.append(dependant)
        elif result == FAILED:
            logger.error(f"* `{task}` execution failed")
            all_dependants = self.__get_all_dependants_of_task_recursively(task)
            if all_dependants:
                logger.error(f"* `Aborting dependents of `{task}` -> {all_dependants}")

        self.execute_tasks()

    def execute_tasks(self):
        """Function to be called multiple times"""
        eligible_tasks = []
        for task in self.eligible_tasks:
            if task in self.exec_data[TRIGGERED_TASKS]:
                continue

            if self.__are_all_dependencies_complete(task):
                self.__mark_task_as_triggered(task)
                eligible_tasks.append(task)

        # Create a list of processes having Process objects and start processes
        processes = []
        for task in eligible_tasks:
            self.eligible_tasks.remove(task)
            process = Process(
                target=self.tasks_dict[task].run_task,
                args=(
                    self,
                    self.execution_times,
                    self.errors,
                    self.semaphore
                )
            )
            process.start()
            processes.append(process)

        for process in processes:
            process.join()

    def initiate(self):
        """Initiate DAG execution starting with tasks with no dependencies"""
        logger.debug("Dag execution started ...")
        start = perf_counter()

        # Get initial list of runnable experiments not having any dependency
        self.eligible_tasks = self.__get_tasks_with_no_dependencies()
        self.execute_tasks()

        end = perf_counter()
        self.execution_times["total"] = round(end - start, 3)

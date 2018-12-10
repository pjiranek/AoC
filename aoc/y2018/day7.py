from aoc import utils
from collections import defaultdict
from abc import ABCMeta, abstractmethod
import re


class StepSource:

    def __init__(self, file_name):
        pattern = r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.'
        expr = re.compile(pattern)

        graph = defaultdict(lambda: {'succ': set(), 'prec': set()})
        for line in utils.read_input(file_name):
            match = expr.match(line)
            node_source, node_target = match.groups()
            graph[node_source]['succ'].add(node_target)
            graph[node_target]['prec'].add(node_source)

        self._graph = graph

        self._order = []
        self._processed = set()
        self._todo = set(node
                         for node in graph
                         if len(graph[node]['prec']) == 0)

    def get_next(self):
        if len(self._todo) > 0:
            step = min(self._todo)
            self._todo.remove(step)
            return step
        else:
            return None

    def finish(self, step):
        self._processed.add(step)
        self._todo.update(node
                          for node in self._graph[step]['succ']
                          if self._graph[node]['prec'] <= self._processed
                          if node not in self._processed)

        self._order.append(step)

    @property
    def done(self):
        return len(self._processed) == len(self._graph)

    @property
    def order(self):
        return ''.join(self._order)


class StepDoer(metaclass = ABCMeta):

    @property
    @abstractmethod
    def has_worker(self):
        pass

    @abstractmethod
    def do(self, task):
        pass

    @abstractmethod
    def get_finished(self):
        pass

    @property
    @abstractmethod
    def time(self):
        pass


class IdealDoer(StepDoer):

    def __init__(self):
        self._step = None

    @property
    def has_worker(self):
        return self._step is None

    def do(self, task):
        assert self._step is None
        self._step = task

    def get_finished(self):
        finished = (self._step, )
        self._step = None
        return finished

    @property
    def time(self):
        return 0


class CrappyDoer(StepDoer):

    def __init__(self, num_workers, step_cost):
        self._num_workers = num_workers
        self._step_cost = step_cost
        self._step_times = {}
        self._time = 0

    @property
    def has_worker(self):
        return len(self._step_times) < self._num_workers

    def do(self, task):
        self._step_times[task] = self._step_cost(task)

    def get_finished(self):
        min_time = min(self._step_times.values())
        self._time += min_time
        finished = [step for step, time in self._step_times.items() if time == min_time]
        self._step_times = {step: time - min_time for step, time in self._step_times.items() if time != min_time}
        return finished

    @property
    def time(self):
        return self._time


def do_all_steps(source, doer):
    while not source.done:
        while doer.has_worker:
            task = source.get_next()
            if task is None:
                break
            doer.do(task)
        finished = doer.get_finished()
        for task in finished:
            source.finish(task)


def main():
    source = StepSource('input7.txt')
    doer = IdealDoer()
    do_all_steps(source, doer)
    print(source.order)

    source = StepSource('input7.txt')
    doer = CrappyDoer(num_workers = 5, step_cost = lambda step: 60 + ord(step) - 64)
    do_all_steps(source, doer)
    print(doer.time)


if __name__ == '__main__':
    main()

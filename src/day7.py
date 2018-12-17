from typing import Dict, List


class Node:
    def __init__(self, name):
        self.name = name
        self.successors = []
        self.predecessors = []

    def add_successor(self, node_name):
        self.successors.append(node_name)

    def add_predecessor(self, node_name):
        self.predecessors.append(node_name)

    def has_predecessors(self):
        return len(self.predecessors) != 0

    def has_successors(self):
        return len(self.successors) != 0


class Workers:
    def __init__(self, n_workers: int, delay: int):
        self.n_workers = n_workers
        self.delay = delay
        self.work_queue = {}
        self.elapsed_time = 0

    def is_full(self):
        return len(self.work_queue.keys()) >= self.n_workers

    def add_work(self, nodes: List[str]):
        added = []
        for node in sorted(nodes):
            if self.is_full():
                break
            self.work_queue[node] = ord(node) - ord('A') + 1 + self.delay
            added.append(node)
        return added

    def get_next_finished_tasks(self):
        min_value = min(self.work_queue.values())
        min_keys = [key for key in self.work_queue.keys() if self.work_queue[key] == min_value]
        for key in min_keys:
            del self.work_queue[key]
        for key in self.work_queue.keys():
            self.work_queue[key] -= min_value
        self.elapsed_time += min_value
        return min_keys


def add_to_graph(graph, node):
    if node not in graph:
        graph[node] = Node(node)


def find_root(graph: Dict, node):
    if len(graph[node].predecessors) == 0:
        return node
    else:
        for pred in graph[node].predecessors:
            return find_root(graph, pred)


def can_be_scheduled(graph: Dict[str, Node], node: str, sequence: str):
    for pred in graph[node].predecessors:
        if pred not in sequence:
            return False
    return True


def traverse_with_workers(graph: Dict[str, Node], nodes: List[str], n_workers: int, delay_p_task: int) -> str:
    ready_queue = []
    wait_queue = []
    ready_queue.extend(sorted(nodes))
    workers = Workers(n_workers, delay_p_task)
    sequence = ""
    while True:
        added_nodes = workers.add_work(ready_queue)
        for r_node in added_nodes:
            ready_queue.remove(r_node)
        done_tasks = workers.get_next_finished_tasks()
        sequence += ''.join(done_tasks)
        for task in done_tasks:
            for suc in sorted(graph[task].successors):
                if suc in sequence:
                    continue
                elif can_be_scheduled(graph, suc, sequence) and suc not in sequence:
                    ready_queue.append(suc)
                elif suc not in wait_queue:
                    wait_queue.append(suc)
        if len(sequence) == len(graph):
            break
        from_wait_to_ready = []
        for node in wait_queue:
            if can_be_scheduled(graph, node, sequence):
                from_wait_to_ready.append(node)
                ready_queue.append(node)
        for node in from_wait_to_ready:
            wait_queue.remove(node)
        #print(sequence)
    print(workers.elapsed_time)
    return sequence


def traverse(graph: Dict[str, Node], nodes: List[str]) -> str:
    ready_queue = []
    wait_queue = []
    ready_queue.extend(sorted(nodes))
    cur_node = ready_queue.pop(0)
    sequence = ""
    while True:
        if cur_node not in sequence:
            sequence += graph[cur_node].name
        for suc in sorted(graph[cur_node].successors):
            if suc in sequence:
                continue
            elif can_be_scheduled(graph, suc, sequence) and suc not in sequence:
                ready_queue.append(suc)
            elif suc not in wait_queue:
                wait_queue.append(suc)

        if len(ready_queue) != 0:
            ready_queue.sort()
            cur_node = ready_queue.pop(0)
            if cur_node in wait_queue:
                wait_queue.remove(cur_node)
        elif len(wait_queue) != 0:
            for w_node in sorted(wait_queue):
                if can_be_scheduled(graph, w_node, sequence):
                    cur_node = w_node
            if cur_node == w_node:
                wait_queue.remove(cur_node)
            else:
                pass
        elif len(sequence) == len(graph.keys()):
            break
        else:
            # all empty finish
            break
    return sequence


def parse_input(in_file) -> Dict[str, Node]:
    input_lines = open(in_file).readlines()
    graph = {}
    for line in input_lines:
        tokenz = line.split()
        pred, suc = tokenz[1], tokenz[-3]
        add_to_graph(graph, pred)
        add_to_graph(graph, suc)
        graph[pred].add_successor(suc)
        graph[suc].add_predecessor(pred)
    return graph


graph = parse_input('../input/input_7.txt')

root = find_root(graph, list(graph.keys())[-1])
roots = []
for key, value in graph.items():
    if not value.has_predecessors():
        roots.append(key)
print('root', roots)
print(traverse(graph, roots))
print(traverse_with_workers(graph,roots,5,60))
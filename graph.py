import queue
from copy import deepcopy

class Node:
    def __init__(self, value: int):
        self.linked_nodes = set()
        self.stored_value = value


class Graph:
    def __init__(self):
        self.nodes = set()

    def add_node(self, node: Node):
        self.nodes.add(node)

    def add_pair(self, node_1: Node, node_2: Node):
        if node_1 not in self.nodes:
            self.add_node(node_1)
        if node_2 not in self.nodes:
            self.add_node(node_2)
        if node_1 not in node_2.linked_nodes:
            node_2.linked_nodes.add(node_1)
        if node_2 not in node_1.linked_nodes:
            node_1.linked_nodes.add(node_2)

    def wsm(self, value: int | Node, start_node: Node):
        visited_nodes = set()
        # if start_node.stored_value == search_node.stored_value:
        #     return start_node
        # else:
        inner_queue = queue.Queue()
        inner_queue.put(start_node)
        visited_nodes.add(start_node)
        while not inner_queue.empty():
            elem = inner_queue.get()
            print(elem.stored_value)
            if type(value) == int:
                if elem.stored_value == value:
                    return elem
                else:
                    for enc_node in elem.linked_nodes:
                        if enc_node not in visited_nodes:
                            inner_queue.put(enc_node)
                            visited_nodes.add(enc_node)
            else:
                if elem.stored_value == value.stored_value:
                    return elem
                else:
                    for enc_node in elem.linked_nodes:
                        if enc_node not in visited_nodes:
                            inner_queue.put(enc_node)
                            visited_nodes.add(enc_node)
        return None

    def dsm(self, value: int | Node, start_node: Node):
        visited_nodes = set()
        # if start_node.stored_value == search_node.stored_value:
        #     return start_node
        # else:
        inner_queue = queue.LifoQueue()
        inner_queue.put(start_node)
        visited_nodes.add(start_node)
        while not inner_queue.empty():
            elem = inner_queue.get()
            print(elem.stored_value)
            if type(value) == int:
                if elem.stored_value == value:
                    return elem
                else:
                    for enc_node in elem.linked_nodes:
                        if enc_node not in visited_nodes:
                            inner_queue.put(enc_node)
                            visited_nodes.add(enc_node)
            else:
                if elem.stored_value == value.stored_value:
                    return elem
                else:
                    for enc_node in elem.linked_nodes:
                        if enc_node not in visited_nodes:
                            inner_queue.put(enc_node)
                            visited_nodes.add(enc_node)
        return None

    def delete_node(self, value: int | Node):
        result = self.wsm(value, next(iter(self.nodes)))
        if not result:
            print('Value not found. Nothing to delete.')
        else:
            self.nodes.discard(result)
            for node in result.linked_nodes:
                node.linked_nodes.discard(result)

    def replace(self, node_to_replace: Node, value: int | Node):
        result = self.wsm(node_to_replace, next(iter(self.nodes)))
        if not result:
            print('Value not found. Nothing to replace.')
        else:
            if type(value) == int:
                result.stored_value = value
            else:
                value.linked_nodes = deepcopy(result.linked_nodes)
                self.nodes.discard(result)
                self.nodes.add(value)
                for node in result.linked_nodes:
                    node.linked_nodes.discard(result)
                    node.linked_nodes.add(value)



random_graph = Graph()
node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)
node5 = Node(5)
node6 = Node(6)
node7 = Node(7)
random_graph.add_pair(node1, node2)
random_graph.add_pair(node1, node3)
random_graph.add_pair(node2, node4)
random_graph.add_pair(node2, node5)
random_graph.add_pair(node3, node6)
random_graph.add_pair(node3, node7)
res = random_graph.wsm(6, node1)
print(res)
print()
res = random_graph.dsm(6, node1)
print(res)
print()
random_graph.delete_node(9)
res = random_graph.wsm(7, node1)
print(res)
print()
# print(res.stored_value)


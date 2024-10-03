import queue

class Node:
    def __init__(self, value: int):
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.stored_value = value


class BinarySearchTree:
    def __init__(self, root_node: Node):
        self.root_node = root_node

    def add_node(self, node_to_add: Node, parent: Node):
        if node_to_add.stored_value < parent.stored_value:
            if not parent.left_child:
                node_to_add.parent = parent
                parent.left_child = node_to_add
            else:
                self.add_node(node_to_add, parent.left_child)
        else:
            if not parent.right_child:
                node_to_add.parent = parent
                parent.right_child = node_to_add
            else:
                self.add_node(node_to_add, parent.right_child)

    def wsm(self):
        print('STARTING WSM')
        visited_nodes = set()
        inner_queue = queue.Queue()
        inner_queue.put(self.root_node)
        while not inner_queue.empty():
            elem = inner_queue.get()
            if elem is None:
                continue
            if elem not in visited_nodes:
                print(elem.stored_value)
                inner_queue.put(elem.left_child)
                inner_queue.put(elem.right_child)
        print('END WSM')

    def depth_preorder_print(self, node: Node):
        if node is None:
            return
        print(node.stored_value)
        self.depth_preorder_print(node.left_child)
        self.depth_preorder_print(node.right_child)

    def depth_inorder_print(self, node: Node):
        if node is None:
            return
        self.depth_inorder_print(node.left_child)
        print(node.stored_value)
        self.depth_inorder_print(node.right_child)

    def depth_postorder_print(self, node: Node):
        if node is None:
            return
        self.depth_inorder_print(node.left_child)
        self.depth_inorder_print(node.right_child)
        print(node.stored_value)

    def find_node(self, node_to_find: Node, pos_node: Node):
        if pos_node is None:
            return
        if pos_node.stored_value == node_to_find.stored_value:
            return pos_node
        else:
            if node_to_find.stored_value > pos_node.stored_value:
                return self.find_node(node_to_find, pos_node.right_child)
            else:
                return self.find_node(node_to_find, pos_node.left_child)

    def find_next(self, node: Node):
        if node.left_child is None:
            return node
        else:
            return self.find_next(node.left_child)

    def delete_node(self, node_to_delete: Node):
        node = self.find_node(node_to_delete, self.root_node)
        if node.left_child is None and node.right_child is None:
            if node.parent:
                if node.parent.left_child == node:
                    node.parent.left_child = None
                else:
                    node.parent.right_child = None
            else:
                self.root_node = None
        elif node.left_child and node.right_child is None:
            if node.parent:
                node.left_child.parent = node.parent
                if node.parent.left_child == node:
                    node.parent.left_child = node.left_child
                else:
                    node.parent.right_child = node.left_child
            else:
                node.left_child.parent = None
                self.root_node = node.left_child

        elif node.right_child and node.left_child is None:
            if node.parent:
                node.right_child.parent = node.parent
                if node.parent.left_child == node:
                    node.parent.left_child = node.right_child
                else:
                    node.parent.right_child = node.right_child
            else:
                node.right_child.parent = None
                self.root_node = node.right_child
        else:
            successor = self.find_next(node.right_child)
            if successor.right_child:
                if successor is successor.parent.left_child:
                    successor.parent.left_child = successor.right_child
                else:
                    successor.parent.right_child = successor.right_child
                successor.right_child.parent = successor.parent
            else:
                if successor is successor.parent.left_child:
                    successor.parent.left_child = None
                else:
                    successor.parent.right_child = None
            if node.left_child != successor:
                successor.left_child = node.left_child
            if node.right_child != successor:
                successor.right_child = node.right_child
            if node.parent:
                if node.parent.right_child == node:
                    node.parent.right_child = successor
                else:
                    node.parent.left_child = successor
                successor.parent = node.parent
            else:
                self.root_node = successor
                successor.parent = None

    def print_tree(self, val="stored_value", left="left_child", right="right_child"):
        def display(root, val=val, left=left, right=right):
            if getattr(root, right) is None and getattr(root, left) is None:
                line = '%s' % getattr(root, val)
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            if getattr(root, right) is None:
                lines, n, p, x = display(getattr(root, left))
                s = '%s' % getattr(root, val)
                u = len(s)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
                second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
                shifted_lines = [line + u * ' ' for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

            if getattr(root, left) is None:
                lines, n, p, x = display(getattr(root, right))
                s = '%s' % getattr(root, val)
                u = len(s)
                first_line = s + x * '_' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

            left, n, p, x = display(getattr(root, left))
            right, m, q, y = display(getattr(root, right))
            s = '%s' % getattr(root, val)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
            second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)
            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
            return lines, n + m + u, max(p, q) + 2, n + u // 2

        lines, *_ = display(self.root_node, val, left, right)
        for line in lines:
            print(line)


if __name__ == '__main__':
    i_am_root = Node(8)
    bst = BinarySearchTree(i_am_root)
    node2 = Node(3)
    node3 = Node(4)
    node4 = Node(2)
    node5 = Node(25)
    node6 = Node(19)
    node7 = Node(28)
    node8 = Node(18)
    node9 = Node(29)
    node10 = Node(5)
    node11 = Node(26)
    node12 = Node(27)
    bst.add_node(node2, bst.root_node)
    bst.add_node(node3, bst.root_node)
    bst.add_node(node4, bst.root_node)
    bst.add_node(node5, bst.root_node)
    bst.add_node(node6, bst.root_node)
    bst.add_node(node7, bst.root_node)
    bst.add_node(node8, bst.root_node)
    bst.add_node(node9, bst.root_node)
    bst.add_node(node10, bst.root_node)
    bst.add_node(node11, bst.root_node)
    bst.add_node(node12, bst.root_node)
    print()
    print('FINISHED ADDING')
    bst.print_tree()
    print()
    bst.wsm()
    print()
    print('STARTING DEPTH PREORDER PRINT')
    print()
    bst.depth_preorder_print(bst.root_node)
    print()

    print('STARTING DEPTH INORDER PRINT')
    print()
    bst.depth_inorder_print(bst.root_node)
    print()

    print('STARTING DEPTH POSTORDER PRINT')
    print()
    bst.depth_inorder_print(bst.root_node)
    print()

    print('STARTING FIND 5')
    print()
    find_node = Node(5)
    res5 = bst.find_node(find_node, bst.root_node)
    print(res5)
    print()

    print('STARTING FIND 10')
    print()
    find_node = Node(10)
    res10 = bst.find_node(find_node, bst.root_node)
    print(res10)
    print()

    print('STARTING FIND 7')
    print()
    find_node = Node(7)
    res7 = bst.find_node(find_node, bst.root_node)
    print(res7)

    print()

    print('STARTING DELETE 25')
    print()
    bst.delete_node(Node(25))
    print()
    bst.print_tree()



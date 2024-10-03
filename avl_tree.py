from binary_search_tree import BinarySearchTree

class Node:
    def __init__(self, value):
        self.stored_value = value
        self.left_child = None
        self.right_child = None
        self.height = 1


class AVLTree(BinarySearchTree):

    def __init__(self, root_node: Node):
        super(AVLTree, self).__init__(root_node)

    @staticmethod
    def height(node: Node):
        if node:
            return node.height
        else:
            return 0

    def get_node_balance(self, node: Node):
        return self.height(node.left_child) - self.height(node.right_child)

    def fix_height(self, node: Node):
        hight_right = self.height(node.right_child)
        hight_left = self.height(node.left_child)
        if hight_right > hight_left:
            biggest_height = hight_right
        else:
            biggest_height = hight_left
        node.height = biggest_height + 1

    def rotate_right(self, node: Node):
        temp = node.left_child
        node.left_child = temp.right_child
        temp.right_child = node
        self.fix_height(node)
        self.fix_height(temp)
        return temp

    def rotate_left(self, node: Node):
        temp = node.right_child
        node.right_child = temp.left_child
        temp.left_child = node
        self.fix_height(node)
        self.fix_height(temp)
        return temp

    def balance_tree(self, node: Node):
        self.fix_height(node)
        if self.get_node_balance(node) == 2:
            if self.get_node_balance(node.left_child) < 0:
                node.left_child = self.rotate_left(node.left_child)
            return self.rotate_right(node)
        elif self.get_node_balance(node) == -2:
            if self.get_node_balance(node.right_child) > 0:
                node.right_child = self.rotate_right(node.right_child)
            return self.rotate_left(node)
        else:
            return node

    def add_node(self, node_to_add: Node, parent_node: Node):
        if node_to_add.stored_value < parent_node.stored_value:
            if parent_node.left_child is None:
                parent_node.left_child = node_to_add
            else:
                parent_node.left_child = self.add_node(node_to_add, parent_node.left_child)
        else:
            if parent_node.right_child is None:
                parent_node.right_child = node_to_add
            else:
                parent_node.right_child = self.add_node(node_to_add, parent_node.right_child)
        return self.balance_tree(parent_node)

    def remove_min(self, node: Node):
        if node.left_child is None:
            return node.right_child
        node.left_child = self.remove_min(node.left_child)
        return self.balance_tree(node)

    def delete_node(self, node_to_delete: Node, parent_node: Node = None):
        if parent_node is None:
            return
        if node_to_delete.stored_value > parent_node.stored_value:
            parent_node.right_child = self.delete_node(node_to_delete, parent_node.right_child)
        elif node_to_delete.stored_value < parent_node.stored_value:
            parent_node.left_child = self.delete_node(node_to_delete, parent_node.left_child)
        else:
            temp_left = parent_node.left_child
            temp_right = parent_node.right_child
            if not temp_right:
                return temp_left
            next_node = self.find_next(parent_node.right_child)
            next_node.right_child = self.remove_min(parent_node.right_child)
            next_node.left_child = temp_left
            return self.balance_tree(next_node)
        return self.balance_tree(parent_node)


if __name__ == '__main__':
    root_node_1 = Node(10)
    node1 = Node(4)
    node2 = Node(17)
    node3 = Node(13)
    node4 = Node(19)
    node5 = Node(11)
    node6 = Node(14)
    tree = AVLTree(root_node_1)
    print()
    print(f'Adding node {node1.stored_value}')
    tree.root_node = tree.add_node(node1, tree.root_node)
    tree.print_tree()
    print()
    print(f'Adding node {node2.stored_value}')
    tree.root_node = tree.add_node(node2, tree.root_node)
    tree.print_tree()
    print()
    print(f'Adding node {node3.stored_value}')
    tree.root_node = tree.add_node(node3, tree.root_node)
    tree.print_tree()
    print()
    print(f'Adding node {node4.stored_value}')
    tree.root_node = tree.add_node(node4, tree.root_node)
    tree.print_tree()
    print()
    print(f'Adding node {node5.stored_value}')
    tree.root_node = tree.add_node(node5, tree.root_node)
    tree.print_tree()
    print()
    print(f'Adding node {node6.stored_value}')
    tree.root_node = tree.add_node(node6, tree.root_node)
    tree.print_tree()
    print(f'deleting node {root_node_1.stored_value}')
    tree.root_node = tree.delete_node(root_node_1, tree.root_node)
    print('finish deleting node')
    tree.print_tree()
    print()
    print(f'deleting node {node5.stored_value}')
    tree.root_node = tree.delete_node(node5, tree.root_node)
    print('finish deleting node')
    tree.print_tree()
    print()
    print(f'deleting node {node1.stored_value}')
    tree.root_node = tree.delete_node(node1, tree.root_node)
    print('finish deleting node')
    tree.print_tree()
    print()

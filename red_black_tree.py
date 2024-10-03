from binary_search_tree import BinarySearchTree

class Node:
    def __init__(self, value):
        self.parent = None
        self.stored_value = value
        self.left_child = None
        self.right_child = None
        self.red = True


class RedBlackTree(BinarySearchTree):

    def __init__(self, root_node: Node):
        super(RedBlackTree, self).__init__(root_node)
        self.root_node.red = False

    def flip_colors(self, node: Node):
        if node.left_child and node.right_child:
            if node.left_child.red and node.right_child.red:
                node.left_child.red = False
                node.right_child.red = False
                node.red = True

    def rotate_right_on_insert(self, node: Node):
        temp = node.left_child
        temp.red = node.red
        node.red = True
        if temp.right_child and node:
            temp.right_child.parent = node
        node.left_child = temp.right_child
        if temp and node:
            node.parent = temp
        temp.right_child = node
        return temp

    def rotate_left_on_insert(self, node: Node):
        temp = node.right_child
        temp.red = node.red
        node.red = True
        if temp.left_child and node:
            temp.left_child.parent = node
        node.right_child = temp.left_child
        if temp and node:
            node.parent = temp
        temp.left_child = node
        return temp

    def rotate_right_on_delete(self, node: Node):
        temp = node.left_child
        if temp.right_child and node:
            temp.right_child.parent = node
        node.left_child = temp.right_child
        if temp and node:
            node.parent = temp
        temp.right_child = node
        return temp

    def rotate_left_on_delete(self, node: Node):
        temp = node.right_child
        if temp.left_child and node:
            temp.left_child.parent = node
        node.right_child = temp.left_child
        if temp and node:
            node.parent = temp
        temp.left_child = node
        return temp

    def fix_insert_balance(self, node: Node):
        right_child_is_black = False
        left_child_is_black = False
        if node.right_child is None:
            right_child_is_black = True
        elif not node.right_child.red:
            right_child_is_black = True
        if node.left_child is None:
            left_child_is_black = True
        elif not node.left_child.red:
            left_child_is_black = True
        if not left_child_is_black:
            if node.left_child.right_child:
                if node.left_child.right_child.red:
                    if right_child_is_black:
                        node.left_child = self.rotate_left_on_insert(node.left_child)
                        node.left_child.parent = node
                    else:
                        self.flip_colors(node)
            if node.left_child.left_child:
                if node.left_child.left_child.red:
                    if right_child_is_black:
                        temp_parent = node.parent
                        node = self.rotate_right_on_insert(node)
                        node.parent = temp_parent
                    else:
                        self.flip_colors(node)
        if not right_child_is_black:
            if node.right_child.left_child:
                if node.right_child.left_child.red:
                    if left_child_is_black:
                        node.left_child = self.rotate_right_on_insert(node.right_child)
                        node.left_child.parent = node
                    else:
                        self.flip_colors(node)
            if node.right_child.right_child:
                if node.right_child.right_child.red:
                    if left_child_is_black:
                        temp_parent = node.parent
                        node = self.rotate_left_on_insert(node)
                        node.parent = temp_parent
                    else:
                        self.flip_colors(node)
        # self.flip_colors(node)
        return node

    def add_node(self, node_to_add: Node, parent_node: Node):
        if parent_node is None:
            return
        if node_to_add.stored_value < parent_node.stored_value:
            if parent_node.left_child is None:
                node_to_add.parent = parent_node
                parent_node.left_child = node_to_add
            else:
                parent_node.left_child = self.add_node(node_to_add, parent_node.left_child)
        elif node_to_add.stored_value > parent_node.stored_value:
            if parent_node.right_child is None:
                node_to_add.parent = parent_node
                parent_node.right_child = node_to_add
            else:
                parent_node.right_child = self.add_node(node_to_add, parent_node.right_child)
        balanced_node = self.fix_insert_balance(parent_node)
        if parent_node == self.root_node:
            balanced_node.red = False
        return balanced_node

    @staticmethod
    def count_child(node: Node):
        counter = 0
        if node.right_child:
            counter += 1
        if node.left_child:
            counter += 1
        return counter

    def get_brother(self, node: Node):
        if node is node.parent.right_child:
            return node.parent.left_child
        else:
            return node.parent.right_child

    def remove_min(self, node: Node):
        if node.left_child is None:
            return node.right_child
        node.left_child = self.remove_min(node.left_child)
        return node

    def remove_node_with_no_child(self, node: Node):
        if not node.red:
            self.fix_delete_balance(node)
        if node.parent:
            if node is node.parent.right_child:
                node.parent.right_child = None
            else:
                node.parent.left_child = None
        else:
            self.root_node = None

    def remove_node_with_one_child(self, node: Node):
        if node.left_child:
            node.left_child.red = node.red
            node.left_child.parent = node.parent
            if node.parent:
                if node is node.parent.right_child:
                    node.parent.right_child = node.left_child

                else:
                    node.parent.left_child = node.left_child
            else:
                if node is node.parent.right_child:
                    node.left_child.parent = None
                    self.root_node = node.left_child
                else:
                    node.left_child.parent = None
                    self.root_node = node.left_child
        else:
            node.right_child.red = node.red
            node.right_child.parent = node.parent
            if node.parent:
                if node is node.parent.right_child:
                    node.parent.right_child = node.right_child

                else:
                    node.parent.left_child = node.right_child
            else:
                if node is node.parent.right_child:
                    node.left_child.parent = None
                    self.root_node = node.right_child
                else:
                    node.left_child.parent = None
                    self.root_node = node.right_child

    def delete_node(self, node_to_delete: Node):
        real_node = self.find_node(node_to_delete, self.root_node)
        child_count = self.count_child(real_node)
        if child_count == 0:
            self.remove_node_with_no_child(real_node)
        elif child_count == 1:
            self.remove_node_with_one_child(real_node)
        else:
            next_node = self.find_next(real_node.right_child)
            next_child_count = self.count_child(next_node)
            if real_node.parent:
                if real_node is real_node.parent.right_child:
                    real_node.parent.right_child = next_node
                else:
                    real_node.parent.left_child = next_node
            else:
                self.root_node = next_node
            if next_child_count == 0:
                self.remove_node_with_no_child(next_node)
            else:
                self.remove_node_with_one_child(next_node)
            next_node.right_child = real_node.right_child
            next_node.left_child = real_node.left_child
            if not real_node.parent:
                next_node.parent = None
            else:
                next_node.parent = real_node.parent
            next_node.red = real_node.red
        self.root_node.red = False

    def fix_delete_balance(self, node: Node):
        if not node.parent or node.red:
            return
        brother = self.get_brother(node)
        if brother == brother.parent.right_child:
            if brother.red:
                brother.red = False
                node.parent.red = True
                if node.parent.parent:
                    parent_right = node.parent is node.parent.parent.right_child
                    old_grandad = node.parent.parent
                    new_subtree = self.rotate_left_on_delete(node.parent)
                    if parent_right:
                        old_grandad.right_child = new_subtree
                        new_subtree.parent = old_grandad
                    else:
                        old_grandad.left_child = new_subtree
                        new_subtree.parent = old_grandad
                else:
                    self.root_node = self.rotate_left_on_delete(node.parent)
                    self.root_node.parent = None
                brother = self.get_brother(node)
            if not brother.red:
                if brother.left_child:
                    brother_left_child_red = brother.left_child.red
                else:
                    brother_left_child_red = False
                if brother.right_child:
                    brother_right_child_red = brother.right_child.red
                else:
                    brother_right_child_red = False
                if not brother_left_child_red and not brother_right_child_red:
                    parent_old_red = node.parent.red
                    brother.red = True
                    node.parent.red = False
                    if not parent_old_red:
                        self.fix_delete_balance(node.parent)
                else:
                    if brother_left_child_red and not brother_right_child_red:
                        brother.left_child.red = False
                        brother.red = True
                        brother = self.rotate_right_on_delete(brother)
                        node.parent.right_child = brother
                        brother.parent = node.parent
                    if brother_right_child_red:
                        brother.red = node.parent.red
                        node.parent.red = False
                        brother.right_child.red = False
                        parent_right = node.parent is node.parent.parent.right_child
                        if node.parent.parent:
                            old_grandad = node.parent.parent
                            new_subtree = self.rotate_left_on_delete(node.parent)
                            if parent_right:
                                old_grandad.right_child = new_subtree
                                new_subtree.parent = old_grandad
                            else:
                                old_grandad.left_child = new_subtree
                                new_subtree.parent = old_grandad
                        else:
                            self.root_node = self.rotate_left_on_delete(node.parent)
                            self.root_node.parent = None
        else:
            if brother.red:
                brother.red = False
                node.parent.red = True
                if node.parent.parent:
                    parent_right = node.parent is node.parent.parent.right_child
                    old_grandad = node.parent.parent
                    new_subtree = self.rotate_right_on_delete(node.parent)
                    if parent_right:
                        old_grandad.right_child = new_subtree
                        new_subtree.parent = old_grandad
                    else:
                        old_grandad.left_child = new_subtree
                        new_subtree.parent = old_grandad
                else:
                    self.root_node = self.rotate_right_on_delete(node.parent)
                    self.root_node.parent = None
                brother = self.get_brother(node)
            if not brother.red:
                if brother.right_child:
                    brother_right_child_red = brother.right_child.red
                else:
                    brother_right_child_red = False
                if brother.left_child:
                    brother_left_child_red = brother.left_child.red
                else:
                    brother_left_child_red = False
                if not brother_right_child_red and not brother_left_child_red:
                    parent_old_red = node.parent.red
                    brother.red = True
                    node.parent.red = False
                    if not parent_old_red:
                        self.fix_delete_balance(node.parent)
                else:
                    if brother_right_child_red and not brother_left_child_red:
                        brother.right_child.red = False
                        brother.red = True
                        brother = self.rotate_left_on_delete(brother)
                        node.parent.left_child = brother
                        brother.parent = node.parent
                    if brother_left_child_red:
                        brother.red = node.parent.red
                        node.parent.red = False
                        brother.left_child.red = False
                        parent_right = node.parent is node.parent.parent.right_child
                        if node.parent.parent:
                            old_grandad = node.parent.parent
                            new_subtree = self.rotate_left_on_delete(node.parent)
                            if parent_right:
                                old_grandad.right_child = new_subtree
                                new_subtree.parent = old_grandad
                            else:
                                old_grandad.left_child = new_subtree
                                new_subtree.parent = old_grandad
                        else:
                            self.root_node = self.rotate_left_on_delete(node.parent)
                            self.root_node.parent = None

    def print_tree(self, val="stored_value", left="left_child", right="right_child"):
        def display(root, val=val, left=left, right=right):
            if getattr(root, right) is None and getattr(root, left) is None:
                line = '%s' % getattr(root, val)
                color = 'r' if getattr(root, 'red') else 'b'
                line = line + color
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            if getattr(root, right) is None:
                lines, n, p, x = display(getattr(root, left))
                s = '%s' % getattr(root, val)
                color = 'r' if getattr(root, 'red') else 'b'
                s = s + color
                u = len(s)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
                second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
                shifted_lines = [line + u * ' ' for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

            if getattr(root, left) is None:
                lines, n, p, x = display(getattr(root, right))
                s = '%s' % getattr(root, val)
                color = 'r' if getattr(root, 'red') else 'b'
                s = s + color
                u = len(s)
                first_line = s + x * '_' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

            left, n, p, x = display(getattr(root, left))
            right, m, q, y = display(getattr(root, right))
            s = '%s' % getattr(root, val)
            color = 'r' if getattr(root, 'red') else 'b'
            s = s + color
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
    root_node_1 = Node(1)
    node1 = Node(2)
    node2 = Node(3)
    node3 = Node(4)
    node4 = Node(5)
    node5 = Node(6)
    node6 = Node(7)
    node7 = Node(8)
    tree = RedBlackTree(root_node_1)
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
    print()
    print(f'Adding node {node5.stored_value}')
    tree.root_node = tree.add_node(node5, tree.root_node)
    tree.print_tree()
    print()
    print(f'Adding node {node7.stored_value}')
    tree.root_node = tree.add_node(node7, tree.root_node)
    tree.print_tree()
    print()
    print()
    print(f'Deleting node 1')
    tree.delete_node(Node(1))
    tree.print_tree()
    print()
    print(f'Deleting node 2')
    tree.delete_node(Node(2))
    tree.print_tree()
    print()
    print(f'Deleting node 3')
    tree.delete_node(Node(3))
    tree.print_tree()
    print()


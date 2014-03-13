# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.avl
    ~~~~~~~~~~~~~~~~~~

    This module implements the AVL tree data structure.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

import bst


class Node(bst.Node):
    """A node in an AVL tree.

    An AVL tree is a BST and a node is an AVL tree is similar to a BST node.
    In order to keep track of the height of a node, an AVL tree node contains
    an additional height attribute.
    The height of a node is the length of the longest path from the node to a
    leaf node.

    :param key: value store in the node
    """

    def __init__(self, key):
        super(Node, self).__init__(key)
        self._height = 0

    @property
    def height(self):
        return self._height

    @property
    def left_height(self):
        """Returns the height of the left child."""
        return self.left.height if self.left else -1

    @property
    def right_height(self):
        """Returns the height of the right child."""
        return self.right.height if self.right else -1

    def is_heavy(self):
        """Returns true if the difference of height between the left and right
        children is greater than 1.
        """
        return abs(self.left_height - self.right_height) > 1

    def is_left_heavy(self, diff=1):
        """Returns true if left child's height minus right child's height is
        greater than ``diff``.
        """
        return self.left_height - self.right_height > diff

    def is_right_heavy(self, diff=1):
        """Returns true if right child's height minus left child's height is
        greater than ``diff``.
        """
        return self.right_height - self.left_height > diff

    def update(self):
        """Updates the weight and height of the node."""
        self.weight = self.count + self.left_weight + self.right_weight
        self._height = 1 + max(self.left_height, self.right_height)


class AVLTree(bst.BinarySearchTree):
    """An AVL tree which is a binary search tree."""

    @staticmethod
    def create_node(key):
        return Node(key)

    def is_balanced(self, node=None):
        """Returns true if the tree is balanced.

        Starting from the root, it recursively checks if every node and its
        children are non-heavy nodes.
        """

        if not node:
            node = self.root

        is_balanced = not node.is_heavy()

        # If parent is balanced, check left child
        if is_balanced and node.left:
            is_balanced = self.is_balanced(node.left)

        # If parent and left child are balanced, check right child
        if is_balanced and node.right:
            is_balanced = self.is_balanced(node.right)

        return is_balanced

    def _balance(self, node):
        parent = node.parent
        if node.is_left_heavy():
            # If left child is right heavy, first make it left heavy.
            if node.left.is_right_heavy(diff=0):
                self._rotate_left(node.left, node.left.right)
            self._rotate_right(node, node.left)
        elif node.is_right_heavy():
            # If right child is left heavy, first make it right heavy.
            if node.right.is_left_heavy(diff=0):
                self._rotate_right(node.right, node.right.left)
            self._rotate_left(node, node.right)

        if parent:
            self._balance(parent)

    def _rotate_left(self, node, heavy_child):
        """Rotate to make the node the left child of its ``heavy_child``."""

        parent = node.parent

        node.right = heavy_child.left
        node.update()

        heavy_child.parent = parent
        heavy_child.left = node
        heavy_child.update()

        if parent:
            parent.add_child(heavy_child)
        else:
            self.root = heavy_child

    def _rotate_right(self, node, heavy_child):
        """Rotate to make the node the right child of its ``heavy_child.``"""

        parent = node.parent

        node.left = heavy_child.right
        node.update()

        heavy_child.parent = parent
        heavy_child.right = node
        heavy_child.update()

        if parent:
            parent.add_child(heavy_child)
        else:
            self.root = heavy_child

    def _update(self, node):
        while node:
            node.update()

            # Updating the height may make the subtree rooted at ``node``
            # unbalanced. Hence balance.
            self._balance(node)

            node = node.parent
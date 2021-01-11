from hashlib import sha256
from math import log2, floor


def _hash(string):
    if string == "":
        return ""
    else:
        return sha256(str.encode(string)).hexdigest()


class MerkleTree:
    def __init__(self, messages):
        # You instantiate the tree passing to the
        # constructor an array of strings:
        # for example:
        #     mt = MerkleTree(['First message', 'Second message', '...and the third'])
        # The tree is implemented with an array, if you want to see it, call
        #     mt._merkle_tree

        _n_leaves = 1
        self._height = 0
        n_messages = len(messages)
        while _n_leaves < n_messages:
            _n_leaves = _n_leaves * 2
            self._height = self._height + 1
        self._merkle_tree = [""] * int(pow(2, self._height + 1) - 1)
        k = pow(2, self._height) - 1
        for m in messages:
            self._merkle_tree[k] = m
            k = k + 1

    def _get_height_of_node(self, node_index):
        if node_index == 0:
            return self._height
        else:
            return self._height - (floor(log2(node_index + 1)))

    def _parent_index(self, child_index):
        if child_index == 0:
            raise ValueError("This is the root")
        if child_index % 2 == 0:
            return int(child_index / 2) - 1
        else:
            return int(child_index / 2)

    def _parent_value(self, child_index):
        return self._merkle_tree[self._parent_index(child_index)]

    def _has_left_child(self, node_index):
        return 2 * node_index + 1 < len(self._merkle_tree)

    def _get_left_child_index(self, node_index):
        if self._has_left_child(node_index):
            return 2 * node_index + 1
        else:
            raise ValueError("The node has no left child")

    def _get_left_child_value(self, node_index):
        return self._merkle_tree[self._get_left_child_index(node_index)]

    def _has_right_child(self, node_index):
        return 2 * node_index + 2 < len(self._merkle_tree)

    def _get_right_child_index(self, node_index):
        if self._has_right_child(node_index):
            return 2 * node_index + 2
        else:
            raise ValueError("The node has no right child")

    def _get_right_child_value(self, node_index):
        return self._merkle_tree[self._get_right_child_index(node_index)]

    def recursive_evaluation(self, current_node_index=0):
        # Attention:
        # whereas stack evaluation (next function) doesn't
        # change the tree itself, this one does change, so calling
        # this function without reassigning the tree results
        # in getting different values for the root each time
        if self._has_left_child(current_node_index):
            self._merkle_tree[current_node_index] = str(_hash(
                self.recursive_evaluation(self._get_left_child_index(current_node_index))
                + self.recursive_evaluation(self._get_right_child_index(current_node_index))))
            return self._merkle_tree[current_node_index]
        else:
            self._merkle_tree[current_node_index] = str(_hash(self._merkle_tree[current_node_index]))
            return self._merkle_tree[current_node_index]

    def stack_evaluation(self):
        # Attention:
        # this function doesn't change the values of the tree
        # itself, but the previous one does. If you want to
        # compare the results provided by
        # stack_evaluation and recursive_evaluation, it's easier to
        # call stack_evaluation first
        stack = []
        for k in range(int(pow(2, self._height)) - 1, len(self._merkle_tree)):
            node_1 = (str(_hash(self._merkle_tree[k])), self._get_height_of_node(k))
            if len(stack) > 0:
                while node_1[1] == stack[len(stack) - 1][1]:
                    node_2 = stack.pop()
                    node_1 = (str(_hash(node_2[0] + node_1[0] )), node_1[1] + 1)
                    if len(stack) == 0:
                        break
            stack.append(node_1)
        return stack.pop()[0]

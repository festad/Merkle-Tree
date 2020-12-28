import hashlib


def _hash(string):
    if string == "":
        return ""
    else:
        return str(hashlib.sha256(str.encode(string)).hexdigest())


class MerkleTree:

    def __init__(self, messages):
        n_leaves = 1
        height = 0
        n_messages = len(messages)
        while n_leaves < n_messages:
            n_leaves = n_leaves * 2
            height = height + 1
        self._merkle_tree = [""] * (pow(2, height + 1) - 1)
        k = pow(2, height) - 1
        for m in messages:
            self._merkle_tree[k] = m
            k = k + 1

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

    def recursive_evaluation(self, current_node_index):
        if self._has_left_child(current_node_index):
            self._merkle_tree[current_node_index] = _hash(
                self.recursive_evaluation(self._get_left_child_index(current_node_index))
                + self.recursive_evaluation(self._get_right_child_index(current_node_index)))
            print(self._merkle_tree)
            return self._merkle_tree[current_node_index]
        else:
            return _hash(self._merkle_tree[current_node_index])

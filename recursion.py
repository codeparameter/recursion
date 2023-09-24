def itself(*args, **kwargs):
    out = list(args)
    out += [v for v in kwargs.values()]
    return out


class Continue:

    def __init__(self, *args, **kwargs):
        self.out = itself(*args, **kwargs)

    def __iter__(self):
        return iter(self.out)


class Unset:
    pass


def recursive(res=Unset()):
    def itself_set(*args, **kwargs):
        return itself(res, *args, **kwargs)

    def itself_unset(*args, **kwargs):
        return itself(*args, **kwargs)

    def inner(itself_fn):
        def wrapper(fn):
            def calc(*args, **kwargs):
                inp = itself_fn(*args, **kwargs)
                while True:
                    out = fn(*inp)
                    if isinstance(out, Continue):
                        inp = out
                    else:
                        return out

            return calc

        return wrapper

    return inner(itself_unset) if isinstance(res, Unset) else inner(itself_set)


"""
# Use case:

@recursive(1)
def factorial(res, n):
    if n == 1:
        return res
    return Continue(n * res, n - 1)


print(factorial(3))
print(factorial(4))
print(factorial(5))


# Bad use case 1:

@recursive(1)
def bad_use_case(res, a, b, n):
    if n == 1:
        return res
    res *= a * b
    return bad_use_case(res * b, a, n - 1) + bad_use_case(res * a, b, n - 1)


print(bad_use_case(6, 9, 3))
print(bad_use_case(3, 5, 6))


# The reason fo that is that actually this library is not necessary in these situations.
# To know how we can use this library, follow this single step: 
# "Instead of returning the function, use Continue like the factorial example."
# Whenever you use calling the function multiple time just before returning anything,
# you don't need this library(unless there is somewhere else in the function that returns only itself).


# Bad use case 2:

# A merkle tree implementation
import hashlib


def str_to_hash(content) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


class Node:
    def __init__(self, left, right, content: str):
        self.left = left
        self.right = right
        self.content = content
        self.hash = str_to_hash(content) if left is None else str_to_hash(left.hash + right.hash)

    def __str__(self):
        return self.content

    def copy(self):
        return Node(self.left, self.right, self.content)


class MerkleTree:
    def __init__(self, content: [str]):
        nodes = [Node(None, None, i) for i in content]
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1].copy())
        self.root = self.buildTree(nodes)

    def getRoot(self):
        return self.root

    @recursive()
    def buildTree(self, content: [Node]) -> Node:
        if len(content) % 2 == 1:
            content.append(content[-1].copy())
        if len(content) == 2:
            return Node(content[0], content[1], content[0].content + content[1].content)
        half = len(content) // 2
        left = self.buildTree(content[:half])
        right = self.buildTree(content[half:])
        return Node(left, right, left.content + right.content)

    def __str__(self) -> str:
        return self.root.content

    def print(self):
        self.printHelper(self.root)

    def printHelper(self, node: Node):
        print(node)
        if node.left is None:
            return
        self.printHelper(node.left)
        self.printHelper(node.right)



content = input().split(" ")
tree = MerkleTree(content)
tree.print()
print(tree.getRoot().hash)



# Like we discussed, calling the function multiple time just before returning anything means this library is useless.

"""

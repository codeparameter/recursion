from concurrent.futures import ThreadPoolExecutor


class Continue:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class Unset:
    pass


def recursive(res=Unset, parallel=False, join=False):
    def set_res(*args, **kwargs):
        return Continue(res, *args, **kwargs)

    def unset_res(*args, **kwargs):
        return Continue(*args, **kwargs)

    def wrapper(itself_fn):
        def calc(fn):
            def inner_calc(*args, **kwargs):
                inp: Continue = itself_fn(*args, **kwargs)
                while True:
                    out = fn(*inp.args, **inp.kwargs)
                    if isinstance(out, Continue):
                        inp = out
                    else:
                        return out

            return inner_calc

        return calc

    def single_thread(itself_fn):
        return wrapper(itself_fn)

    def multi_thread(itself_fn):
        if join:
            class Result:
                item = None

            with ThreadPoolExecutor() as executor:
                Result.item = executor.submit(wrapper, itself_fn).result()
            return Result.item
        else:
            return ThreadPoolExecutor().submit(wrapper, itself_fn).result()

    itself = unset_res if res == Unset else set_res

    return multi_thread(itself) if parallel else single_thread(itself)


"""
# Use case:

@recursive(res=1)
def factorial(res, n):
    if n == 1:
        return res
    return Continue(n * res, n - 1)


print(factorial(3))
print(factorial(4))
print(factorial(5))


# Use case 1:

@recursive(res=1, parallel=True)
def bad_use_case(res, a, b, n):
    if n == 1:
        return res
    res *= a * b
    return bad_use_case(res * b, a, n - 1) + bad_use_case(res * a, b, n - 1)


print(bad_use_case(6, 9, 3))
print(bad_use_case(3, 5, 6))


# To know how we can use this library, remember these:
# 1. Instead of returning the function, use Continue like the factorial example.
# 2. Whenever you use calling the function multiple time just before returning anything, you maybe be able
#    to set parallel flag True. If parallel would corrupted your calculations, then in these situations
#    you don't need to use this library at all


# Use case 2:

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

    @recursive(parallel=True)
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
"""

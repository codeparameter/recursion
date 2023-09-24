<h1> Python Recursion Package </h1>

<h3> install: <h3>

<pre><code>
pip install recursion
</code></pre>

<h3> doc: <h3>


<h5>Use case:</h5>

<pre><code>
@recursive(1)
def factorial(res, n):
    if n == 1:
        return res
    return Continue(n * res, n - 1)


print(factorial(3))
print(factorial(4))
print(factorial(5))
</code></pre>

<h5>Bad use case 1:</h5>

<pre><code>
@recursive(1)
def bad_use_case(res, a, b, n):
    if n == 1:
        return res
    res *= a * b
    return bad_use_case(res * b, a, n - 1) + bad_use_case(res * a, b, n - 1)


print(bad_use_case(6, 9, 3))
print(bad_use_case(3, 5, 6))
</code></pre>

<p>
The reason fo that is that actually this library is not necessary in these situations.
To know how we can use this library, follow this single step: 
"Instead of returning the function, use Continue like the factorial example."
Whenever you use calling the function multiple time just before returning anything,
you don't need this library(unless there is somewhere else in the function that returns only itself).
</p>

<h5>Bad use case 2:</h5>

<pre><code>
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
        

    def __init__(self, content: [str]):
        nodes = [Node(None, None, i) for i in content]
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1].copy())
        self.root = self.buildTree(nodes)

    def getRoot(self):
        return self.root

    def buildTree(self, content: [Node]) -> Node:
        if len(content) % 2 == 1:
            content.append(content[-1].copy())
        if len(content) == 2:
            return Node(content[0], content[1], content[0].content + content[1].content)
        half = len(content) // 2
        left = self.buildTree(content[:half])
        right = self.buildTree(content[half:])
        return Node(left, right, left.content + right.content)
        


@recursion(None)
def buildTree_rec(res, content: [Node]) -> Node:
    if len(content) % 2 == 1:
        content.append(content[-1].copy())
    if len(content) == 2:
        return Node(content[0], content[1], content[0].content + content[1].content)
    half = len(content) // 2
    left = buildTree_rec(content[:half])
    right = buildTree_rec(content[half:])
    return Node(left, right, left.content + right.content)


def buildTree(content: [str]):
    nodes = [Node(None, None, i) for i in content]
    if len(nodes) % 2 == 1:
        nodes.append(nodes[-1].copy())
    return buildTree_rec(nodes)
</code></pre>

<p>
Like we discussed, calling the function multiple time just before returning anything means this library is useless.
This example is even worse. we even didn't use res at all!
</p>


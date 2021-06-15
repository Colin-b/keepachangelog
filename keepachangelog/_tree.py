from abc import ABC, abstractmethod
from typing import Union, List, Optional, Iterator, TypeVar, Generic, Sequence

T = TypeVar("T", bound="Tree")


class Printable(ABC):
    """Abstract Printable class.

    Printable classes define a `print` function with an
    optional `depth` parameter."""

    @abstractmethod
    def print(self, depth: int = 0) -> str:
        """Prints the object.

        :param depth: May be used to know the relative depth of this
                object.
        """
        pass  # pragma: no cover


class TextNode(List[str], Printable):
    """A text node.

    A Leaf in a Tree. It can contain a `list[str]` to represent
    a multiline string.
    """

    def __init__(self, seq: Sequence[str] = (), parent: "Tree" = None):
        super(TextNode, self).__init__(seq)
        self.__parent = parent

    def print(self, depth: int = 1, *, indent: int = 2, bullet: str = "-") -> str:
        if not self:
            return ""
        if depth < 1:
            raise ValueError("A %s cannot be root!", self.__class__.__name__)
        # let's allow for indent=1 but not encourage
        indent = indent if indent > 0 else 2
        initial = (
            f"{' ' * ((depth - 1 ) * indent)}"
            f"{' ' * (indent - (2 if indent > 1 else 1))}"
            f"{bullet}{' ' if indent > 1 else ''}"
        )
        subsequent = " " * (depth * indent)
        lines = [f"{initial}{self[0]}"] + [f"{subsequent}{el}" for el in self[1:]]
        return "\n".join(lines)


NodeType = Union[T, TextNode]


class Tree(Generic[T], Printable, Sequence):
    """A printable Tree."""

    def __init__(
        self,
        children: Optional[List[NodeType]] = None,
        *,
        parent: T = None,
    ):
        self.__parent = parent
        self.__children: List[NodeType] = [] if children is None else children

    def __iter__(self) -> Iterator:
        for child in self.__children:
            if isinstance(child, Tree):
                yield from child
            elif isinstance(child, TextNode):
                yield "\n".join(child).rstrip()

    def __getitem__(self, index: int) -> NodeType:
        return self.__children[index]

    def __len__(self):
        return len(self.__children)

    def __repr__(self) -> str:
        return f"{self.type()}[{', '.join(repr(c) for c in self.__children)}]"

    def __str__(self) -> str:
        return self.print()

    @property
    def parent(self) -> T:
        return self.__parent

    @property
    def children(self) -> List[NodeType]:
        return self.__children

    @property
    def is_root(self) -> bool:
        return self.__parent is None

    @property
    def last(self) -> NodeType:
        if isinstance(self[-1], Tree):
            return self[-1].last
        elif isinstance(self[-1], TextNode):
            return self[-1]

    @property
    def last_non_textnode(self) -> T:
        if isinstance(self[-1], Tree):
            return self[-1].last_non_textnode
        elif isinstance(self[-1], TextNode):
            return self

    @classmethod
    def treeify(cls, data: list) -> T:
        """Transforms a `list` into a `Tree`.

        >>> Tree.treeify([])
        Root[]

        >>> Tree.treeify([[]])
        Root[Node[]]

        >>> Tree.treeify([[[]]])
        Root[Node[Node[]]]

        >>> Tree.treeify([[], []])
        Root[Node[], Node[]]

        >>> Tree.treeify([["item 1 (L1)\\nitem1 (L2)"], ["item 2", ["item 2.1", "item 2.2"]]])
        Root[Node[['item 1 (L1)', 'item1 (L2)']], Node[['item 2'], Node[['item 2.1'], ['item 2.2']]]]
        """
        root = cls()
        for el in data:
            if isinstance(el, list):
                root.new_child_node(cls.treeify(el))
            elif isinstance(el, str):
                root.new_child_node(TextNode(el.splitlines()))
        return root

    def new_child_node(self, child: NodeType) -> None:
        """Adds a child node to the Tree."""
        self.__children.append(child)
        child.__parent = self

    def type(self) -> str:
        """The "type" of the current part of the Tree.

        :return: Either "Root" or "Node"."""
        return "Root" if self.is_root else "Node"

    def print(self, depth: int = 0) -> str:
        out = []
        for child in self.__children:
            if isinstance(child, Tree):
                out.append(child.print(depth + 1))
            elif isinstance(child, TextNode):
                out.append(child.print(depth))
        return "\n".join(out)


class BulletTree(Tree["BulletTree"]):
    """A printable Tree that accepts some extra formatting options."""

    def __init__(
        self,
        children: Optional[List[NodeType]] = None,
        *,
        parent: "Tree" = None,
        bullet: str = "-",
        indent: int = 2,
    ):
        super(BulletTree, self).__init__(children, parent=parent)
        self.__bullet = bullet
        self.__indent = indent

    @property
    def bullet(self):
        return self.__bullet

    @property
    def indent(self):
        return self.__indent

    def print(self, depth: int = 0, *, bullet: Optional[str] = None) -> str:
        bullet = self.__bullet if bullet is None else bullet
        out = []
        for child in self.children:
            if isinstance(child, Tree):
                out.append(child.print(depth + 1))
            elif isinstance(child, TextNode):
                out.append(child.print(depth, indent=self.__indent, bullet=bullet))
        return "\n".join(out)

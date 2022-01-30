import textwrap

import pytest
from keepachangelog._tree import Tree, TextNode


class TestTextNode:
    def test_empty(self):
        assert TextNode().print() == ""

    def test_root_bad(self):
        with pytest.raises(ValueError):
            TextNode([""]).print(depth=0)

    def test_single_line_default(self):
        assert TextNode(["line 1"]).print() == "- line 1"

    def test_single_line_bullet(self):
        assert TextNode(["line 1"]).print(bullet="*") == "* line 1"

    def test_single_line_bullet_depth1_indent1(self):
        assert TextNode(["line 1"]).print(indent=1, bullet="*") == "*line 1"

    def test_single_line_bullet_depth1_indent4(self):
        assert TextNode(["line 1"]).print(depth=1, indent=4, bullet="*") == "  * line 1"

    def test_single_line_bullet_depth2_indent4(self):
        assert (
            TextNode(["line 1"]).print(depth=2, indent=4, bullet="*")
            == "      * line 1"
        )

    def test_single_line_bullet_depth2_indent2(self):
        assert TextNode(["line 1"]).print(depth=2, indent=2, bullet="*") == "  * line 1"


class TestTree:
    @pytest.mark.parametrize(
        ["data", "expected_repr", "expected_str"],
        [
            pytest.param([], "Root[]", "", id="empty"),
            pytest.param([[]], "Root[Node[]]", "", id="single_node"),
            pytest.param([[[]]], "Root[Node[Node[]]]", "", id="two_nested_nodes"),
            pytest.param([[], []], "Root[Node[], Node[]]", "\n", id="two_nodes"),
            pytest.param(
                [["item 1 (L1)\nitem 1 (L2)"], ["item 2", ["item 2.1", "item 2.2"]]],
                "Root[Node[['item 1 (L1)', 'item 1 (L2)']], Node[['item 2'], Node[['item 2.1'], ['item 2.2']]]]",
                textwrap.dedent(
                    """\
                 - item 1 (L1)
                   item 1 (L2)
                 - item 2
                   - item 2.1
                   - item 2.2"""
                ),
                id="complex",
            ),
        ],
    )
    def test_repr(self, data: list, expected_repr, expected_str: str):
        assert repr(Tree.treeify(data)) == expected_repr
        assert str(Tree.treeify(data)) == expected_str

    def test_repr_root(self):
        assert (
            repr(Tree.treeify(["item 1 (L1)\nitem 1 (L2)"]))
            == "Root[['item 1 (L1)', 'item 1 (L2)']]"
        )

    def test_repr_non_root(self):
        assert (
            repr(
                Tree.treeify(
                    [["item 1 (L1)\nitem 1 (L2)"], ["item 2", ["item 2.1", "item 2.2"]]]
                )[0]
            )
            == "Node[['item 1 (L1)', 'item 1 (L2)']]"
        )

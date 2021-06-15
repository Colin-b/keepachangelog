import textwrap

import pytest

from keepachangelog._changelog_dataclasses import Category


class TestCategory:
    def test_no_bullet_bad(self):
        lines = textwrap.dedent(
            """
            note 1
            note 2
            """
        ).splitlines()
        category = Category()
        with pytest.raises(ValueError):
            for line in lines:
                category.streamline(line)

    def test_complex(self):
        lines = textwrap.dedent(
            """
            * note 1 l1
              note 1 l2
    
              note 1 l4
              - note 1.1 l1
              - note 1.2 l1
                note 1.2 l2
            - note 2
            * note 3
            """
        ).splitlines()
        category = Category()
        for line in lines:
            category.streamline(line)
        assert category

        # Should look like:
        #
        # Root[
        #     Node[TextNode[""]]
        #     Node[
        #         TextNode["note 1 l1", "note 1 l2", "", "note 1 l4"],
        #         Node[TextNode["note 1.1 l1"]],
        #         Node[TextNode["note 1.2 l1", "note 1.2 l2"]],
        #     ],
        #     Node[TextNode["note 2"]],
        #     Node[TextNode["note 3"]],
        # ]

        assert category.root[0].bullet == "*"
        assert category.root[0][0] == ["note 1 l1", "note 1 l2", "", "note 1 l4"]
        assert category.root[0][1].bullet == "-"
        assert category.root[0][1][0] == ["note 1.1 l1"]
        assert category.root[0][2].bullet == "-"
        assert category.root[0][2][0] == ["note 1.2 l1", "note 1.2 l2"]
        assert category.root[1].bullet == "-"
        assert category.root[1][0] == ["note 2"]
        assert category.root[2].bullet == "*"
        assert category.root[2][0] == ["note 3"]

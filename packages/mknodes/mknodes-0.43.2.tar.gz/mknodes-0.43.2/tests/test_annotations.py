from __future__ import annotations

import mknodes


EXPECTED = """## Header

1.  abcde
    fghi
2.  abcde
    fghi
3.  abcde
    fghi
4.  abcde
    fghi
5.  abcde
    fghi
6.  abcde
    fghi
7.  abcde
    fghi
8.  abcde
    fghi
9.  abcde
    fghi
10. abcde
    fghi
"""

EXPECTED_SORTED = """1.  1
2.  2
"""


def test_empty():
    annotation = mknodes.MkAnnotations()
    assert not str(annotation)


def test_if_annotations_get_sorted():
    node = mknodes.MkAnnotations()
    node[2] = "2"
    node[1] = "1"
    assert str(node) == EXPECTED_SORTED


def test_markdown():
    annotation = mknodes.MkAnnotations(["abcde\nfghi"] * 10, header="Header")
    assert str(annotation) == EXPECTED


def test_constructors():
    annotation_1 = mknodes.MkAnnotations(["abc", "def"])
    anns = {1: "abc", 2: "def"}
    annotation_2 = mknodes.MkAnnotations(anns)
    assert str(annotation_1) == str(annotation_2)


def test_mapping_interface():
    ann = mknodes.MkAnnotations()
    ann[1] = "test"
    assert str(ann[1]) == "1.  test\n"


def test_code_annotations_inside_admonition():
    expected = """!!! info
    <div class="annotate" markdown>
    ``` python
    test # (1)
    ```
    </div>

    1.  Some annotation

"""
    code = mknodes.MkCode("test # (1)", language="python")
    code.annotations[1] = "Some annotation"
    admonition = mknodes.MkAdmonition(code)
    assert str(admonition) == expected

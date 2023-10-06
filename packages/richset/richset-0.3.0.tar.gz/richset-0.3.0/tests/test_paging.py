from dataclasses import dataclass

from richset import RichSet


@dataclass(frozen=True)
class Something:
    id: int
    name: str


def test_richset_page() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
            Something(4, "four"),
            Something(5, "five"),
        ]
    )
    assert rs.page(0, 2).to_list() == [
        Something(1, "one"),
        Something(2, "two"),
    ]
    assert rs.page(1, 2).to_list() == [
        Something(2, "two"),
        Something(3, "three"),
    ]
    assert rs.page(2, 2).to_list() == [
        Something(3, "three"),
        Something(4, "four"),
    ]
    assert rs.page(3, 2).to_list() == [
        Something(4, "four"),
        Something(5, "five"),
    ]
    assert rs.page(4, 2).to_list() == [
        Something(5, "five"),
    ]


def test_richset_split_into_pages() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
            Something(4, "four"),
            Something(5, "five"),
        ]
    )
    assert rs.split_into_pages(2) == [
        RichSet.from_list(
            [
                Something(1, "one"),
                Something(2, "two"),
            ]
        ),
        RichSet.from_list(
            [
                Something(3, "three"),
                Something(4, "four"),
            ]
        ),
        RichSet.from_list(
            [
                Something(5, "five"),
            ]
        ),
    ]
    assert rs.split_into_pages(3) == [
        RichSet.from_list(
            [
                Something(1, "one"),
                Something(2, "two"),
                Something(3, "three"),
            ]
        ),
        RichSet.from_list(
            [
                Something(4, "four"),
                Something(5, "five"),
            ]
        ),
    ]
    assert rs.split_into_pages(4) == [
        RichSet.from_list(
            [
                Something(1, "one"),
                Something(2, "two"),
                Something(3, "three"),
                Something(4, "four"),
            ]
        ),
        RichSet.from_list(
            [
                Something(5, "five"),
            ]
        ),
    ]
    assert rs.split_into_pages(5) == [
        RichSet.from_list(
            [
                Something(1, "one"),
                Something(2, "two"),
                Something(3, "three"),
                Something(4, "four"),
                Something(5, "five"),
            ]
        ),
    ]
    assert rs.split_into_pages(6) == [
        RichSet.from_list(
            [
                Something(1, "one"),
                Something(2, "two"),
                Something(3, "three"),
                Something(4, "four"),
                Something(5, "five"),
            ]
        ),
    ]

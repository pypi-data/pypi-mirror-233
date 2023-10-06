from __future__ import annotations

import functools
from bs4.element import _PageElementT, _Strainable, SoupStrainer, NavigableString, ResultSet
from abc import ABCMeta, abstractmethod

from _typeshed import Incomplete, ReadableBuffer
from collections.abc import Callable, Iterable, Iterator
from re import Pattern
from typing import Any, Generic, TypeVar, overload, Self, List
from typing_extensions import Self, TypeAlias

from bs4 import BeautifulSoup
from bs4.builder import TreeBuilder
from bs4.formatter import Formatter, _EntitySubstitution
from bs4.element import PageElement, Tag

DEFAULT_OUTPUT_ENCODING: str
nonwhitespace_re: Pattern[str]
whitespace_re: Pattern[str]
PYTHON_SPECIFIC_ENCODINGS: set[str]

if False:
# class PageElement:
#     parent: Tag | None
#     previous_element: PageElement | None
#     next_element: PageElement | None
#     next_sibling: PageElement | None
#     previous_sibling: PageElement | None
#     def setup(
#         self,
#         parent: Tag | None = None,
#         previous_element: PageElement | None = None,
#         next_element: PageElement | None = None,
#         previous_sibling: PageElement | None = None,
#         next_sibling: PageElement | None = None,
#     ) -> None: ...
#     def format_string(self, s: str, formatter: Formatter | str | None) -> str: ...
#     def formatter_for_name(self, formatter: Formatter | str | _EntitySubstitution): ...
#     nextSibling: PageElement | None
#     previousSibling: PageElement | None
#     @property
#     def stripped_strings(self) -> Iterator[str]: ...
#     def get_text(self, separator: str = "", strip: bool = False, types: tuple[type[NavigableString], ...] = ...) -> str: ...
#     getText = get_text
#     @property
#     def text(self) -> str: ...
#     def replace_with(self, *args: PageElement | str) -> Self: ...
#     replaceWith = replace_with
#     def unwrap(self) -> Self: ...
#     replace_with_children = unwrap
#     replaceWithChildren = unwrap
#     def wrap(self, wrap_inside: _PageElementT) -> _PageElementT: ...
#     def extract(self, _self_index: int | None = None) -> Self: ...
#     def insert(self, position: int, new_child: PageElement | str) -> None: ...
#     def append(self, tag: PageElement | str) -> None: ...
#     def extend(self, tags: Iterable[PageElement | str]) -> None: ...
#     def insert_before(self, *args: PageElement | str) -> None: ...
#     def insert_after(self, *args: PageElement | str) -> None: ...
#     def find_next(
#         self,
#         name: _Strainable | SoupStrainer | None = None,
#         attrs: dict[str, _Strainable] | _Strainable = {},
#         string: _Strainable | None = None,
#         **kwargs: _Strainable,
#     ) -> Tag | NavigableString | None: ...
#     findNext = find_next
#     def find_all_next(
#         self,
#         name: _Strainable | SoupStrainer | None = None,
#         attrs: dict[str, _Strainable] | _Strainable = {},
#         string: _Strainable | None = None,
#         limit: int | None = None,
#         **kwargs: _Strainable,
#     ) -> ResultSet[PageElement]: ...
#     findAllNext = find_all_next
#     def find_next_sibling(
#         self,
#         name: _Strainable | SoupStrainer | None = None,
#         attrs: dict[str, _Strainable] | _Strainable = {},
#         string: _Strainable | None = None,
#         **kwargs: _Strainable,
#     ) -> Tag | NavigableString | None: ...
#     findNextSibling = find_next_sibling
#     def find_next_siblings(
#         self,
#         name: _Strainable | SoupStrainer | None = None,
#         attrs: dict[str, _Strainable] | _Strainable = {},
#         string: _Strainable | None = None,
#         limit: int | None = None,
#         **kwargs: _Strainable,
#     ) -> ResultSet[PageElement]: ...
#     findNextSiblings = find_next_siblings
#     fetchNextSiblings = find_next_siblings
#     def find_previous(
#         self,
#         name: _Strainable | SoupStrainer | None = None,
#         attrs: dict[str, _Strainable] | _Strainable = {},
#         string: _Strainable | None = None,
#         **kwargs: _Strainable,
#     ) -> Tag | NavigableString | None: ...
#     findPrevious = find_previous
#     def find_all_previous(
#         self,
#         name: _Strainable | SoupStrainer | None = None,
#         attrs: dict[str, _Strainable] | _Strainable = {},
#         string: _Strainable | None = None,
#         limit: int | None = None,
#         **kwargs: _Strainable,
#     ) -> ResultSet[PageElement]: ...
#     findAllPrevious = find_all_previous
#     fetchPrevious = find_all_previous
#     def find_previous_sibling(
#         self,
#         name: _Strainable | SoupStrainer | None = None,
#         attrs: dict[str, _Strainable] | _Strainable = {},
#         string: _Strainable | None = None,
#         **kwargs: _Strainable,
#     ) -> Tag | NavigableString | None: ...
#     findPreviousSibling = find_previous_sibling
#     def find_previous_siblings(
#         self,
#         name: _Strainable | SoupStrainer | None = None,
#         attrs: dict[str, _Strainable] | _Strainable = {},
#         string: _Strainable | None = None,
#         limit: int | None = None,
#         **kwargs: _Strainable,
#     ) -> ResultSet[PageElement]: ...
#     findPreviousSiblings = find_previous_siblings
#     fetchPreviousSiblings = find_previous_siblings
#     def find_parent(
#         self,
#         name: _Strainable | SoupStrainer | None = None,
#         attrs: dict[str, _Strainable] | _Strainable = {},
#         **kwargs: _Strainable,
#     ) -> Tag | None: ...
#     findParent = find_parent
#     def find_parents(
#         self,
#         name: _Strainable | SoupStrainer | None = None,
#         attrs: dict[str, _Strainable] | _Strainable = {},
#         limit: int | None = None,
#         **kwargs: _Strainable,
#     ) -> ResultSet[Tag]: ...
#     findParents = find_parents
#     fetchParents = find_parents
#     @property
#     def next(self) -> Tag | NavigableString | None: ...
#     @property
#     def previous(self) -> Tag | NavigableString | None: ...
#     @property
#     def next_elements(self) -> Iterable[PageElement]: ...
#     @property
#     def next_siblings(self) -> Iterable[PageElement]: ...
#     @property
#     def previous_elements(self) -> Iterable[PageElement]: ...
#     @property
#     def previous_siblings(self) -> Iterable[PageElement]: ...
#     @property
#     def parents(self) -> Iterable[Tag]: ...
#     @property
#     def decomposed(self) -> bool: ...
#     def nextGenerator(self) -> Iterable[PageElement]: ...
#     def nextSiblingGenerator(self) -> Iterable[PageElement]: ...
#     def previousGenerator(self) -> Iterable[PageElement]: ...
#     def previousSiblingGenerator(self) -> Iterable[PageElement]: ...
#     def parentGenerator(self) -> Iterable[Tag]: ...


# class Tag(PageElement):
#     parser_class: type[BeautifulSoup] | None
#     name: str
#     namespace: str | None
#     prefix: str | None
#     sourceline: int | None
#     sourcepos: int | None
#     known_xml: bool | None
#     attrs: dict[str, str]
#     contents: list[PageElement]
#     hidden: bool
#     can_be_empty_element: bool | None
#     cdata_list_attributes: list[str] | None
#     preserve_whitespace_tags: list[str] | None
#     def __init__(
#         self,
#         parser: BeautifulSoup | None = None,
#         builder: TreeBuilder | None = None,
#         name: str | None = None,
#         namespace: str | None = None,
#         prefix: str | None = None,
#         attrs: dict[str, str] | None = None,
#         parent: Tag | None = None,
#         previous: PageElement | None = None,
#         is_xml: bool | None = None,
#         sourceline: int | None = None,
#         sourcepos: int | None = None,
#         can_be_empty_element: bool | None = None,
#         cdata_list_attributes: list[str] | None = None,
#         preserve_whitespace_tags: list[str] | None = None,
#         interesting_string_types: type[NavigableString] | tuple[type[NavigableString], ...] | None = None,
#         namespaces: dict[str, str] | None = None,
#     ) -> None: ...
#     parserClass: type[BeautifulSoup] | None
#     def __copy__(self) -> Self: ...
#     @property
#     def is_empty_element(self) -> bool: ...
#     @property
#     def isSelfClosing(self) -> bool: ...
#     @property
#     def string(self) -> str | None: ...
#     @string.setter
#     def string(self, string: str) -> None: ...
#     DEFAULT_INTERESTING_STRING_TYPES: tuple[type[NavigableString], ...]
#     @property
#     def strings(self) -> Iterable[str]: ...
#     def decompose(self) -> None: ...
#     def clear(self, decompose: bool = False) -> None: ...
#     def smooth(self) -> None: ...
#     def index(self, element: PageElement) -> int: ...
#     def get(self, key: str, default: str | list[str] | None = None) -> str | list[str] | None: ...
#     def get_attribute_list(self, key: str, default: str | list[str] | None = None) -> list[str]: ...
#     def has_attr(self, key: str) -> bool: ...
#     def __hash__(self) -> int: ...
#     def __getitem__(self, key: str) -> str | list[str]: ...
#     def __iter__(self) -> Iterator[PageElement]: ...
#     def __len__(self) -> int: ...
#     def __contains__(self, x: object) -> bool: ...
#     def __bool__(self) -> bool: ...
#     def __setitem__(self, key: str, value: str | list[str]) -> None: ...
#     def __delitem__(self, key: str) -> None: ...
#     def __getattr__(self, tag: str) -> Tag | None: ...
#     def __eq__(self, other: object) -> bool: ...
#     def __ne__(self, other: object) -> bool: ...
#     def __unicode__(self) -> str: ...
#     def encode(
#         self,
#         encoding: str = "utf-8",
#         indent_level: int | None = None,
#         formatter: str | Formatter = "minimal",
#         errors: str = "xmlcharrefreplace",
#     ) -> bytes: ...
#     def decode(
#         self,
#         indent_level: int | None = None,
#         eventual_encoding: str = "utf-8",
#         formatter: str | Formatter = "minimal",
#         iterator: Iterator[PageElement] | None = None,
#     ) -> str: ...
#     @overload
#     def prettify(self, encoding: str, formatter: str | Formatter = "minimal") -> bytes: ...
#     @overload
#     def prettify(self, encoding: None = None, formatter: str | Formatter = "minimal") -> str: ...
#     def decode_contents(
#         self, indent_level: int | None = None, eventual_encoding: str = "utf-8", formatter: str | Formatter = "minimal"
#     ) -> str: ...
#     def encode_contents(
#         self, indent_level: int | None = None, encoding: str = "utf-8", formatter: str | Formatter = "minimal"
#     ) -> bytes: ...
#     def renderContents(self, encoding: str = "utf-8", prettyPrint: bool = False, indentLevel: int = 0) -> bytes: ...
#     def find(
#         self,
#         name: _Strainable | None = None,
#         attrs: dict[str, _Strainable] | _Strainable = {},
#         recursive: bool = True,
#         string: _Strainable | None = None,
#         **kwargs: _Strainable,
#     ) -> Tag | NavigableString | None: ...
#     findChild = find
#     def find_all(
#         self,
#         name: _Strainable | None = None,
#         attrs: dict[str, _Strainable] | _Strainable = {},
#         recursive: bool = True,
#         string: _Strainable | None = None,
#         limit: int | None = None,
#         **kwargs: _Strainable,
#     ) -> ResultSet[Any]: ...
#     __call__ = find_all
#     findAll = find_all
#     findChildren = find_all
#     @property
#     def children(self) -> Iterable[PageElement]: ...
#     @property
#     def descendants(self) -> Iterable[PageElement]: ...
#     def select_one(
#         self, selector: str, namespaces: Incomplete | None = None, *, flags: int = ..., custom: dict[str, str] | None = ...
#     ) -> Tag | None: ...
#     def select(
#         self,
#         selector: str,
#         namespaces: Incomplete | None = None,
#         limit: int | None = None,
#         *,
#         flags: int = ...,
#         custom: dict[str, str] | None = ...,
#     ) -> ResultSet[Tag]: ...
#     def childGenerator(self) -> Iterable[PageElement]: ...
#     def recursiveChildGenerator(self) -> Iterable[PageElement]: ...
#     def has_key(self, key: str) -> bool: ...
    pass

ChainingBroadcastListType = list

# ChainingBroadcastListType = type[ChainingBroadcastList]

T = TypeVar('T')
# U = TypeVar('U')

class AbstractBroadcastList(list[T], metaclass=ABCMeta):
    @abstractmethod
    def _callable_attr_broadcast(self, *args, attr_name: str = '', **kwargs) -> Any:
        ...

    @abstractmethod
    def _attr_broadcast(self, attr_name: str) -> Any:
        ...

    def __getattr__(self, __name: str):
        ...

class NonchainingBroadcastList(AbstractBroadcastList[T]):
    def _callable_attr_broadcast(self, *args, attr_name: str = '', **kwargs) -> None:
        ...

    def _attr_broadcast(self, attr_name: str) -> None:
        ...

class ChainingBroadcastList(AbstractBroadcastList[T]):
    def _callable_attr_broadcast(self, *args, attr_name: str = '', **kwargs) -> ChainingBroadcastList:
        ...

    def _attr_broadcast(self, attr_name: str) -> ChainingBroadcastList:
        ...


class TagBroadcastList(ChainingBroadcastList[Tag]):
    parent: ChainingBroadcastList[Tag | None]
    previous_element: ChainingBroadcastList[PageElement | None]
    next_element: ChainingBroadcastList[PageElement | None]
    next_sibling: ChainingBroadcastList[PageElement | None]
    previous_sibling: ChainingBroadcastList[PageElement | None]
    def setup(
        self,
        parent: Tag | None = None,
        previous_element: PageElement | None = None,
        next_element: PageElement | None = None,
        previous_sibling: PageElement | None = None,
        next_sibling: PageElement | None = None,
    ) -> ChainingBroadcastList[None]: ...
    def format_string(self, s: str, formatter: Formatter | str | None) -> ChainingBroadcastList[str]: ...
    def formatter_for_name(self, formatter: Formatter | str | _EntitySubstitution) -> ChainingBroadcastList[None]: ...
    nextSibling: ChainingBroadcastList[PageElement | None]
    previousSibling: ChainingBroadcastList[PageElement | None]
    @property
    def stripped_strings(self) -> ChainingBroadcastList[Iterator[str]]: ...
    def get_text(self, separator: str = "", strip: bool = False, types: tuple[type[NavigableString], ...] = ...) -> ChainingBroadcastList[str]: ...
    getText = get_text
    @property
    def text(self) -> ChainingBroadcastList[str]: ...
    def replace_with(self, *args: PageElement | str) -> ChainingBroadcastList[Self]: ...
    replaceWith = replace_with
    def unwrap(self) -> ChainingBroadcastList[Self]: ...
    replace_with_children = unwrap
    replaceWithChildren = unwrap
    def wrap(self, wrap_inside: _PageElementT) -> ChainingBroadcastList[_PageElementT]: ...
    def extract(self, _self_index: int | None = None) -> ChainingBroadcastList[Self]: ...
    def Einsert(self, position: int, new_child: PageElement | str) -> ChainingBroadcastList[None]: ...
    def Eappend(self, tag: PageElement | str) -> ChainingBroadcastList[None]: ...
    def Eextend(self, tags: Iterable[PageElement | str]) -> ChainingBroadcastList[None]: ...
    def insert_before(self, *args: PageElement | str) -> ChainingBroadcastList[None]: ...
    def insert_after(self, *args: PageElement | str) -> ChainingBroadcastList[None]: ...
    def find_next(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> ChainingBroadcastList[Tag | NavigableString | None]: ...
    findNext = find_next
    def find_all_next(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> ChainingBroadcastList[ResultSet[PageElement]]: ...
    findAllNext = find_all_next
    def find_next_sibling(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> ChainingBroadcastList[Tag | NavigableString | None]: ...
    findNextSibling = find_next_sibling
    def find_next_siblings(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> ChainingBroadcastList[ResultSet[PageElement]]: ...
    findNextSiblings = find_next_siblings
    fetchNextSiblings = find_next_siblings
    def find_previous(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> ChainingBroadcastList[Tag | NavigableString | None]: ...
    findPrevious = find_previous
    def find_all_previous(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> ChainingBroadcastList[ResultSet[PageElement]]: ...
    findAllPrevious = find_all_previous
    fetchPrevious = find_all_previous
    def find_previous_sibling(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> ChainingBroadcastList[Tag | NavigableString | None]: ...
    findPreviousSibling = find_previous_sibling
    def find_previous_siblings(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> ChainingBroadcastList[ResultSet[PageElement]]: ...
    findPreviousSiblings = find_previous_siblings
    fetchPreviousSiblings = find_previous_siblings
    def find_parent(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        **kwargs: _Strainable,
    ) -> ChainingBroadcastList[Tag | None]: ...
    findParent = find_parent
    def find_parents(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> ChainingBroadcastList[ResultSet[Tag]]: ...
    findParents = find_parents
    fetchParents = find_parents
    @property
    def next(self) -> ChainingBroadcastList[Tag | NavigableString | None]: ...
    @property
    def previous(self) -> ChainingBroadcastList[Tag | NavigableString | None]: ...
    @property
    def next_elements(self) -> ChainingBroadcastList[Iterable[PageElement]]: ...
    @property
    def next_siblings(self) -> ChainingBroadcastList[Iterable[PageElement]]: ...
    @property
    def previous_elements(self) -> ChainingBroadcastList[Iterable[PageElement]]: ...
    @property
    def previous_siblings(self) -> ChainingBroadcastList[Iterable[PageElement]]: ...
    @property
    def parents(self) -> ChainingBroadcastList[Iterable[Tag]]: ...
    @property
    def decomposed(self) -> ChainingBroadcastList[bool]: ...
    def nextGenerator(self) -> ChainingBroadcastList[Iterable[PageElement]]: ...
    def nextSiblingGenerator(self) -> ChainingBroadcastList[Iterable[PageElement]]: ...
    def previousGenerator(self) -> ChainingBroadcastList[Iterable[PageElement]]: ...
    def previousSiblingGenerator(self) -> ChainingBroadcastList[Iterable[PageElement]]: ...
    def parentGenerator(self) -> ChainingBroadcastList[Iterable[Tag]]: ...

    # TAGS

    parser_class: ChainingBroadcastList[type[BeautifulSoup] | None]
    name: ChainingBroadcastList[str]
    namespace: ChainingBroadcastList[str | None]
    prefix: ChainingBroadcastList[str | None]
    sourceline: ChainingBroadcastList[int | None]
    sourcepos: ChainingBroadcastList[int | None]
    known_xml: ChainingBroadcastList[bool | None]
    attrs: ChainingBroadcastList[dict[str, str]]
    contents: ChainingBroadcastList[list[PageElement]]
    hidden: ChainingBroadcastList[bool]
    can_be_empty_element: ChainingBroadcastList[bool | None]
    cdata_list_attributes: ChainingBroadcastList[list[str] | None]
    preserve_whitespace_tags: ChainingBroadcastList[list[str] | None]
    # def __init__(
    #     self,
    #     parser: BeautifulSoup | None = None,
    #     builder: TreeBuilder | None = None,
    #     name: str | None = None,
    #     namespace: str | None = None,
    #     prefix: str | None = None,
    #     attrs: dict[str, str] | None = None,
    #     parent: Tag | None = None,
    #     previous: PageElement | None = None,
    #     is_xml: bool | None = None,
    #     sourceline: int | None = None,
    #     sourcepos: int | None = None,
    #     can_be_empty_element: bool | None = None,
    #     cdata_list_attributes: list[str] | None = None,
    #     preserve_whitespace_tags: list[str] | None = None,
    #     interesting_string_types: type[NavigableString] | tuple[type[NavigableString], ...] | None = None,
    #     namespaces: dict[str, str] | None = None,
    # ) -> ChainingBroadcastList[None]: ...
    parserClass: ChainingBroadcastList[type[BeautifulSoup] | None]
    def __copy__(self) -> ChainingBroadcastList[Self]: ...
    @property
    def is_empty_element(self) -> ChainingBroadcastList[bool]: ...
    @property
    def isSelfClosing(self) -> ChainingBroadcastList[bool]: ...
    @property
    def string(self) -> ChainingBroadcastList[str | None]: ...
    @string.setter
    def string(self, string: str) -> ChainingBroadcastList[None]: ...
    DEFAULT_INTERESTING_STRING_TYPES: ChainingBroadcastList[tuple[type[NavigableString], ...]]
    @property
    def strings(self) -> ChainingBroadcastList[Iterable[str]]: ...
    def decompose(self) -> ChainingBroadcastList[None]: ...
    def Eclear(self, decompose: bool = False) -> ChainingBroadcastList[None]: ...
    def smooth(self) -> ChainingBroadcastList[None]: ...
    def Eindex(self, element: PageElement) -> ChainingBroadcastList[int]: ...
    def get(self, key: str, default: str | list[str] | None = None) -> ChainingBroadcastList[str | list[str] | None]: ...
    def get_attribute_list(self, key: str, default: str | list[str] | None = None) -> ChainingBroadcastList[list[str]]: ...
    def has_attr(self, key: str) -> ChainingBroadcastList[bool]: ...
    def E__hash__(self) -> ChainingBroadcastList[int]: ...
    def E__getitem__(self, key: str) -> ChainingBroadcastList[str | list[str]]: ...
    def E__iter__(self) -> ChainingBroadcastList[Iterator[PageElement]]: ...
    def E__len__(self) -> ChainingBroadcastList[int]: ...
    def E__contains__(self, x: object) -> ChainingBroadcastList[bool]: ...
    def E__bool__(self) -> ChainingBroadcastList[bool]: ...
    def __setitem__(self, key: str, value: str | list[str]) -> ChainingBroadcastList[None]: ...
    def E__delitem__(self, key: str) -> ChainingBroadcastList[None]: ...
    def __getattr__(self, tag: str) -> ChainingBroadcastList[Tag | None]: ...
    def E__eq__(self, other: object) -> ChainingBroadcastList[bool]: ...
    def E__ne__(self, other: object) -> ChainingBroadcastList[bool]: ...
    def __unicode__(self) -> ChainingBroadcastList[str]: ...
    def encode(
        self,
        encoding: str = "utf-8",
        indent_level: int | None = None,
        formatter: str | Formatter = "minimal",
        errors: str = "xmlcharrefreplace",
    ) -> ChainingBroadcastList[bytes]: ...
    def decode(
        self,
        indent_level: int | None = None,
        eventual_encoding: str = "utf-8",
        formatter: str | Formatter = "minimal",
        iterator: Iterator[PageElement] | None = None,
    ) -> ChainingBroadcastList[str]: ...
    @overload
    def prettify(self, encoding: str, formatter: str | Formatter = "minimal") -> ChainingBroadcastList[bytes]: ...
    @overload
    def prettify(self, encoding: None = None, formatter: str | Formatter = "minimal") -> ChainingBroadcastList[str]: ...
    def decode_contents(
        self, indent_level: int | None = None, eventual_encoding: str = "utf-8", formatter: str | Formatter = "minimal"
    ) -> ChainingBroadcastList[str]: ...
    def encode_contents(
        self, indent_level: int | None = None, encoding: str = "utf-8", formatter: str | Formatter = "minimal"
    ) -> ChainingBroadcastList[bytes]: ...
    def renderContents(self, encoding: str = "utf-8", prettyPrint: bool = False, indentLevel: int = 0) -> ChainingBroadcastList[bytes]: ...
    def find(
        self,
        name: _Strainable | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        recursive: bool = True,
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> ChainingBroadcastList[Tag | NavigableString | None]: ...
    findChild = find
    def find_all(
        self,
        name: _Strainable | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        recursive: bool = True,
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> ChainingBroadcastList[ResultSet[Any]]: ...
    __call__ = find_all
    findAll = find_all
    findChildren = find_all
    @property
    def children(self) -> ChainingBroadcastList[Iterable[PageElement]]: ...
    @property
    def descendants(self) -> ChainingBroadcastList[Iterable[PageElement]]: ...
    def select_one(
        self, selector: str, namespaces: Incomplete | None = None, *, flags: int = ..., custom: dict[str, str] | None = ...
    ) -> ChainingBroadcastList[Tag | None]: ...
    def select(
        self,
        selector: str,
        namespaces: Incomplete | None = None,
        limit: int | None = None,
        *,
        flags: int = ...,
        custom: dict[str, str] | None = ...,
    ) -> ChainingBroadcastList[ResultSet[Tag]]: ...
    def childGenerator(self) -> ChainingBroadcastList[Iterable[PageElement]]: ...
    def recursiveChildGenerator(self) -> ChainingBroadcastList[Iterable[PageElement]]: ...
    def has_key(self, key: str) -> ChainingBroadcastList[bool]: ...
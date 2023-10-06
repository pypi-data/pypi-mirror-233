from __future__ import annotations

import functools
from abc import abstractmethod, ABCMeta
from typing import (
    Any,
    TypeVar,
    # Generic,
)

from bs4.element import Tag

T = TypeVar('T')


class AbstractBroadcastList(list[T], metaclass=ABCMeta):
    @abstractmethod
    def _callable_attr_broadcast(self, *args, attr_name: str = '', **kwargs) -> Any:
        ...

    @abstractmethod
    def _attr_broadcast(self, attr_name: str) -> Any:
        ...

    def __getattr__(self, __name: str):
        if __name.startswith('E'):
            __name = __name.removeprefix('E')

        # every element contained in list should share same type.
        if callable(getattr(self[0], __name)):
            return functools.partial(self._callable_attr_broadcast, attr_name=__name)
        else:
            return self._attr_broadcast(__name)


class NonchainingBroadcastList(AbstractBroadcastList[T]):
    def _callable_attr_broadcast(self, *args, attr_name: str = '', **kwargs):
        if not attr_name:
            raise ValueError('attr_name is empty. This function not intended to use outside of class.')
        self[:] = [getattr(i, attr_name)(*args, **kwargs) for i in self]

    def _attr_broadcast(self, attr_name: str):
        self[:] = [getattr(i, attr_name) for i in self]


class ChainingBroadcastList(AbstractBroadcastList[T]):
    def _callable_attr_broadcast(self, *args, attr_name: str = '', **kwargs):
        if not attr_name:
            raise ValueError('attr_name is empty. This function not intended to use outside of class.')
        return ChainingBroadcastList([getattr(i, attr_name)(*args, **kwargs) for i in self])

    def _attr_broadcast(self, attr_name: str):
        return ChainingBroadcastList([getattr(i, attr_name) for i in self])


class TagBroadcastList(ChainingBroadcastList[Tag]):  # This list is made for typing purpose. See 'broadcast_list.pyi'.
    """Chaining Broadcast list especially for Tags, seperated due to typing purpose."""

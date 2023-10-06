from __future__ import annotations

import functools
import logging
from typing import (
    Any,
    Hashable,
    Mapping,
    Iterable,
    Callable
)

from frozendict import frozendict


def ignore_unhashable(func):
    """
    Sorce: https://stackoverflow.com/a/64111268/21997874 (MIT License maybe)
    만약 unhashable을 만나 caching이 중지되었다면, 오류를 내보내지 않게 만드는 함수입니다.
    """
    uncached = func.__wrapped__
    attributes = functools.WRAPPER_ASSIGNMENTS + ('cache_info', 'cache_clear')

    @functools.wraps(func, assigned=attributes)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as error:
            if 'unhashable type' in str(error):
                problematic_args = [arg for arg in args if not isinstance(arg, Hashable)]
                problematic_kwargs = {key: value for key, value in kwargs.items() if not isinstance(value, Hashable)}

                error_description = ('If one of arguments is unhashable, function cannot be cached. '
                                     'Please do not use caching.\n')
                if problematic_args:
                    error_description += 'problematic argument(s): '
                if problematic_args and problematic_kwargs:
                    error_description += '\n'
                if problematic_kwargs:
                    error_description += (
                        ('problematic keyword argument: ' if len(problematic_kwargs) == 1 else 'problematic keyword arguments: ')
                        + ', '.join(f'{item}: {value}' for item, value in problematic_kwargs.items())
                    )

                logging.warning(error_description)
                return uncached(*args, **kwargs)
            raise
    wrapper.__uncached__ = uncached  # type: ignore
    return wrapper


def made_it_hashable(value, alert: bool = True, error: bool = False) -> Any:
    if isinstance(value, Hashable):
        return value
    # 앞에서 Hashable은 이미 나가기 때문에 Iterable이나 Mapping 검사 시 hashable인지는 검사하지 않아도 됨.
    if isinstance(value, Mapping):  # Mapping은 Iterable이기 때문에 Iterable보다 더 먼저 와야 값이 손상되지 않음!
        return frozendict(value)
    if isinstance(value, Iterable):  # Mapping같이 특정한 경우에는 값이 손상될 수 있음.
        return tuple(value)
    if error:
        raise TypeError(f"type of '{value}' {type(value)}, "
                        "which is nether hashable, iterable(like list), nor mapping(like dict).")
    if alert:
        logging.warning(f"type of '{value}' {type(value)}, "
                        "which is nether hashable, iterable(like list), nor mapping(like dict). "
                        "So this thing will not be converted to hashable, that means this function "
                        "cannot be cached if your're using things like lru_cache.")
    return value


def freeze_dict_and_list(alert: bool = True, error: bool = False):
    """
    기본적으로는 가장 흔한 mutable인 mapping와 unhashable한 iterable를 hashable로 변환합니다.
    만악 dict와 list 외의 mutable이 있다면 아무런 변환 없이 넘깁니다.
    이때 alert가 True라면 경고를 내보내고, error가 True이면 exception이 나갑니다.
    """
    def wrapper(func: Callable):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            # 속도를 위해 제너레이터 컴프리헨션 대신 리스트 > 튜플 변환 사용 (약 1.5~2배 가량 빠름)
            new_args = [made_it_hashable(argument, alert, error) for argument in args]
            new_kwargs = {kwname: made_it_hashable(kwvalue)
                          for kwname, kwvalue in kwargs.items()}
            logging.debug((new_args, new_kwargs))
            return func(*new_args, **new_kwargs)
        return inner

    return wrapper

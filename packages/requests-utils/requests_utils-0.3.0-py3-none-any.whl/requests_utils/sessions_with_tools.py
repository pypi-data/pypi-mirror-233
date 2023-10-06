import functools
from functools import lru_cache
import logging
from requests.sessions import Session as RequestsSession
from requests.models import Request
from requests.exceptions import ConnectionError
import asyncio
import time

from .dealing_unhashable_args import freeze_dict_and_list
from .response_proxy import ResponseProxy
from .contants import DEFAULT_HEADERS


class Session(RequestsSession):
    # def __init__(self):
    #     super().__init__()
    #     self._caches = {}

    def request(
        self,
        *args,
        attempts: int | None = None,
        waiting_time_reattept: int | float | None = None,
        raise_for_status: bool = True,
        **kwargs,
    ):
        """Constructs a :class:`Request <Request>`, prepares it and sends it.

        """
        if kwargs.get('headers') == 'default':
            kwargs['headers'] = DEFAULT_HEADERS

        kwargs.setdefault('timeout', 40)

        attempts = attempts or 1

        last_exception = None
        if attempts <= 1 or not isinstance(attempts, int):
            response = ResponseProxy(super().request(*args, **kwargs))
            if raise_for_status:
                response.raise_for_status()
            return response

        for _ in range(attempts):
            try:
                response = ResponseProxy(super().request(*args, **kwargs))
            except ConnectionError as e:
                logging.warning('Retring...')
                last_exception = e
                time.sleep(waiting_time_reattept or 0)
            else:
                if last_exception is not None:
                    logging.warning(f'Sucessfully retried from {response.url}')
                if raise_for_status:
                    response.raise_for_status()
                return response

        url = args[0] if args else kwargs['url']
        raise ConnectionError(f'Trying {attempts} times but failed to get data.\nURL: {url}') from last_exception

    # CACHED REQESTS

    @freeze_dict_and_list()
    @lru_cache
    def cget(self, url, params=None, **kwargs):
        "cached requests.get"
        return self.get(url, params=params, **kwargs)

    @freeze_dict_and_list()
    @lru_cache
    def coptions(self, url, **kwargs):
        "cached requests.options"
        return self.options(url, **kwargs)

    @freeze_dict_and_list()
    @lru_cache
    def chead(self, url, **kwargs):
        "cached requests.head"
        kwargs.setdefault("allow_redirects", False)
        return self.head(url, **kwargs)

    @freeze_dict_and_list()
    @lru_cache
    def cpost(self, url, data=None, json=None, **kwargs):
        "cached requests.post"
        return self.post(url, data=data, json=json, **kwargs)

    @freeze_dict_and_list()
    @lru_cache
    def cput(self, url, data=None, **kwargs):
        "cached requests.put"
        return self.put(url, data=data, **kwargs)

    @freeze_dict_and_list()
    @lru_cache
    def cpatch(self, url, data=None, **kwargs):
        "cached requests.patch"
        return self.patch(url, data=data, **kwargs)

    @freeze_dict_and_list()
    @lru_cache
    def cdelete(self, url, **kwargs):
        "cached requests.delete"
        return self.delete(url, **kwargs)

    # ASYNCRONIZED, CACHED REQESTS

    async def acget(self, url, params=None, run_in_executor: bool = True, **kwargs):
        "asyncronized, cached requests.get"
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.cget(url, **kwargs))
        return self.cget(url, params=params, **kwargs)

    async def acoptions(self, url, run_in_executor: bool = True, **kwargs):
        "asyncronized, cached requests.options"
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.coptions(url, **kwargs))
        return self.coptions(url, **kwargs)

    async def achead(self, url, run_in_executor: bool = True, **kwargs):
        "asyncronized, cached requests.head"
        kwargs.setdefault("allow_redirects", False)
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.chead(url, **kwargs))
        return self.chead(url, **kwargs)

    async def acpost(self, url, data=None, json=None, run_in_executor: bool = True, **kwargs):
        "asyncronized, cached requests.post"
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.cpost(url, data=data, json=json, **kwargs))
        return self.cpost(url, data=data, json=json, **kwargs)

    async def acput(self, url, data=None, run_in_executor: bool = True, **kwargs):
        "asyncronized, cached requests.put"
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.cput(url, data=data, **kwargs))
        return self.cput(url, data=data, **kwargs)

    async def acpatch(self, url, data=None, run_in_executor: bool = True, **kwargs):
        "asyncronized, cached requests.patch"
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.cpatch(url, data=data, **kwargs))
        return self.cpatch(url, data=data, **kwargs)

    async def acdelete(self, url, run_in_executor: bool = True, **kwargs):
        "asyncronized, cached requests.delete"
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.cdelete(url, **kwargs))
        return self.cdelete(url, **kwargs)

    # ASYNCRONIZED REQESTS

    async def aget(self, url, params=None, run_in_executor: bool = True, **kwargs):
        "asyncronized requests.get"
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.get(url, **kwargs))
        return self.get(url, params=params, **kwargs)

    async def aoptions(self, url, run_in_executor: bool = True, **kwargs):
        "asyncronized requests.options"
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.options(url, **kwargs))
        return self.options(url, **kwargs)

    async def ahead(self, url, run_in_executor: bool = True, **kwargs):
        "asyncronized requests.head"
        kwargs.setdefault("allow_redirects", False)
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.head(url, **kwargs))
        return self.head(url, **kwargs)

    async def apost(self, url, data=None, json=None, run_in_executor: bool = True, **kwargs):
        "asyncronized requests.post"
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.post(url, data=data, json=json, **kwargs))
        return self.post(url, data=data, json=json, **kwargs)

    async def aput(self, url, data=None, run_in_executor: bool = True, **kwargs):
        "asyncronized requests.put"
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.put(url, data=data, **kwargs))
        return self.put(url, data=data, **kwargs)

    async def apatch(self, url, data=None, run_in_executor: bool = True, **kwargs):
        "asyncronized requests.patch"
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.patch(url, data=data, **kwargs))
        return self.patch(url, data=data, **kwargs)

    async def adelete(self, url, run_in_executor: bool = True, **kwargs):
        "asyncronized requests.delete"
        if run_in_executor:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.delete(url, **kwargs))
        return self.delete(url, **kwargs)

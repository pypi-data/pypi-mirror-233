"""
requests_plus.requests_api_with_more_tools
~~~~~~~~~~~~

This module implements the Requests API and more tools.

:copyright: (c) 2023 by ilotoki0804.
:license: MIT License, see LICENSE for more details.
"""

from __future__ import annotations

from functools import lru_cache
import asyncio
import logging
# from typing import Literal, Any, TypedDict

from requests import sessions, exceptions

from . import response_proxy
from .dealing_unhashable_args import freeze_dict_and_list
from .contants import DEFAULT_HEADERS

__all__ = (
    'request',
    'get', 'options', 'head', 'post', 'put', 'patch', 'delete',
    'cget', 'coptions', 'chead', 'cpost', 'cput', 'cpatch', 'cdelete',
    'acget', 'acoptions', 'achead', 'acpost', 'acput', 'acpatch', 'acdelete',
    'aget', 'aoptions', 'ahead', 'apost', 'aput', 'apatch', 'adelete',
)


def request(method, url, **kwargs):
    """기본값, 재시도 횟수 등 추가 기능이 들어간 requests_plus 버전의 requests.request 구현입니다.

    ## 추가된 기능
    만약 명시하지 않았다면 기본값이 적용됩니다. timeout의 기본값은 100, headers의 기본값은 간단한 user agent, attempts의 기본값은 1입니다.

    ## 기존 requests 라이브러리에는 없는 parameter
    :param attempts: (optional) request가 ConnectionError를 받았을 때 같은 요청을 몇 번 다시 실행할 것인지를 정합니다.
    :type attempts: positive integer

    ## 기존 requests 라이브러리에 있었던 parameter
    :param method: method for the new :class:`Request` object: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    Usage::

      >>> from requests_utils import requests
      >>> req = requests.request('GET', 'https://httpbin.org/get')
      >>> req
      <Response [200]>
    """

    # By using the 'with' statement we are sure the session is closed, thus we
    # avoid leaving sockets open which can trigger a ResourceWarning in some
    # cases, and look like a memory leak in others.
    def send_request():
        with sessions.Session() as session:
            return session.request(method=method, url=url, **kwargs)

    # kwargs.setdefault('headers', {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    #                               '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'})

    kwargs.setdefault('headers', DEFAULT_HEADERS)

    kwargs.setdefault('timeout', 40)

    if 'attempts' not in kwargs:
        attempts = 1
    else:
        attempts = kwargs['attempts']
        del kwargs['attempts']

    last_exception = None
    if attempts > 1:
        for _ in range(attempts):
            try:
                response = response_proxy.ResponseProxy(send_request())
            except exceptions.ConnectionError as e:
                logging.warning('Retring...')
                last_exception = e
            else:
                if last_exception is not None:
                    logging.warning(f'Sucessfully retried from {url}')
                return response
    else:
        return response_proxy.ResponseProxy(send_request())

    raise ConnectionError(f'Trying {attempts} times but failed to get data.\nURL: {url}') from last_exception


def get(url, params=None, **kwargs):
    r"""Sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("get", url, params=params, **kwargs)


def options(url, **kwargs):
    r"""Sends an OPTIONS request.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("options", url, **kwargs)


def head(url, **kwargs):
    r"""Sends a HEAD request.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes. If
        `allow_redirects` is not provided, it will be set to `False` (as
        opposed to the default :meth:`request` behavior).
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    kwargs.setdefault("allow_redirects", False)
    return request("head", url, **kwargs)


def post(url, data=None, json=None, **kwargs):
    r"""Sends a POST request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("post", url, data=data, json=json, **kwargs)


def put(url, data=None, **kwargs):
    r"""Sends a PUT request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("put", url, data=data, **kwargs)


def patch(url, data=None, **kwargs):
    r"""Sends a PATCH request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("patch", url, data=data, **kwargs)


def delete(url, **kwargs):
    r"""Sends a DELETE request.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("delete", url, **kwargs)


# CACHED REQESTS


@freeze_dict_and_list()
@lru_cache
def cget(url, params=None, **kwargs):
    "cached requests.get"
    return get(url, params=params, **kwargs)


@freeze_dict_and_list()
@lru_cache
def coptions(url, **kwargs):
    "cached requests.options"
    return options(url, **kwargs)


@freeze_dict_and_list()
@lru_cache
def chead(url, **kwargs):
    "cached requests.head"
    kwargs.setdefault("allow_redirects", False)
    return head(url, **kwargs)


@freeze_dict_and_list()
@lru_cache
def cpost(url, data=None, json=None, **kwargs):
    "cached requests.post"
    return post(url, data=data, json=json, **kwargs)


@freeze_dict_and_list()
@lru_cache
def cput(url, data=None, **kwargs):
    "cached requests.put"
    return put(url, data=data, **kwargs)


@freeze_dict_and_list()
@lru_cache
def cpatch(url, data=None, **kwargs):
    "cached requests.patch"
    return patch(url, data=data, **kwargs)


@freeze_dict_and_list()
@lru_cache
def cdelete(url, **kwargs):
    "cached requests.delete"
    return delete(url, **kwargs)


# ASYNCRONIZED, CACHED REQESTS


async def acget(url, params=None, run_in_executor: bool = True, **kwargs):
    "asyncronized, cached requests.get"
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: cget(url, **kwargs))
    return cget(url, params=params, **kwargs)


async def acoptions(url, run_in_executor: bool = True, **kwargs):
    "asyncronized, cached requests.options"
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: coptions(url, **kwargs))
    return coptions(url, **kwargs)


async def achead(url, run_in_executor: bool = True, **kwargs):
    "asyncronized, cached requests.head"
    kwargs.setdefault("allow_redirects", False)
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: chead(url, **kwargs))
    return chead(url, **kwargs)


async def acpost(url, data=None, json=None, run_in_executor: bool = True, **kwargs):
    "asyncronized, cached requests.post"
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: cpost(url, data=data, json=json, **kwargs))
    return cpost(url, data=data, json=json, **kwargs)


async def acput(url, data=None, run_in_executor: bool = True, **kwargs):
    "asyncronized, cached requests.put"
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: cput(url, data=data, **kwargs))
    return cput(url, data=data, **kwargs)


async def acpatch(url, data=None, run_in_executor: bool = True, **kwargs):
    "asyncronized, cached requests.patch"
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: cpatch(url, data=data, **kwargs))
    return cpatch(url, data=data, **kwargs)


async def acdelete(url, run_in_executor: bool = True, **kwargs):
    "asyncronized, cached requests.delete"
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: cdelete(url, **kwargs))
    return cdelete(url, **kwargs)


# ASYNCRONIZED REQESTS


async def aget(url, params=None, run_in_executor: bool = True, **kwargs):
    "asyncronized requests.get"
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: get(url, **kwargs))
    return get(url, params=params, **kwargs)


async def aoptions(url, run_in_executor: bool = True, **kwargs):
    "asyncronized requests.options"
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: options(url, **kwargs))
    return options(url, **kwargs)


async def ahead(url, run_in_executor: bool = True, **kwargs):
    "asyncronized requests.head"
    kwargs.setdefault("allow_redirects", False)
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: head(url, **kwargs))
    return head(url, **kwargs)


async def apost(url, data=None, json=None, run_in_executor: bool = True, **kwargs):
    "asyncronized requests.post"
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: post(url, data=data, json=json, **kwargs))
    return post(url, data=data, json=json, **kwargs)


async def aput(url, data=None, run_in_executor: bool = True, **kwargs):
    "asyncronized requests.put"
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: put(url, data=data, **kwargs))
    return put(url, data=data, **kwargs)


async def apatch(url, data=None, run_in_executor: bool = True, **kwargs):
    "asyncronized requests.patch"
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: patch(url, data=data, **kwargs))
    return patch(url, data=data, **kwargs)


async def adelete(url, run_in_executor: bool = True, **kwargs):
    "asyncronized requests.delete"
    if run_in_executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: delete(url, **kwargs))
    return delete(url, **kwargs)

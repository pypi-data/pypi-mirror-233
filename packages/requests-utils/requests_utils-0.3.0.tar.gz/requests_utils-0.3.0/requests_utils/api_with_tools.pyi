#### IMPORTS FOR TYPE HINT

# from _typeshed import Incomplete
# from collections.abc import Mapping
# from typing_extensions import TypeAlias

# from requests.models import Response
# from .sessions import RequestsCookieJar, _Auth, _Cert, _Data, _Files, _HooksInput, _Params, _TextMapping, _Timeout, _Verify

from __future__ import annotations

# from _typeshed import Incomplete, SupportsItems, SupportsRead, Unused
from _typeshed import Incomplete, SupportsItems, SupportsRead
from collections.abc import Callable, Iterable, Mapping, MutableMapping
from typing import Any
# from typing_extensions import Self, TypeAlias, TypedDict
from typing_extensions import TypeAlias

# from urllib3._collections import RecentlyUsedContainer

# from requests import adapters, auth as _auth, compat, cookies, exceptions, hooks, models, status_codes, utils
from requests import auth as _auth, cookies, models
from requests.models import Response
from requests.structures import CaseInsensitiveDict as CaseInsensitiveDict

from .response_proxy import ResponseProxy

# _BaseAdapter: TypeAlias = adapters.BaseAdapter
# OrderedDict = compat.OrderedDict
# cookiejar_from_dict = cookies.cookiejar_from_dict
# extract_cookies_to_jar = cookies.extract_cookies_to_jar
RequestsCookieJar = cookies.RequestsCookieJar
# merge_cookies = cookies.merge_cookies
# Request = models.Request
PreparedRequest = models.PreparedRequest
# DEFAULT_REDIRECT_LIMIT = models.DEFAULT_REDIRECT_LIMIT
# default_hooks = hooks.default_hooks
# dispatch_hook = hooks.dispatch_hook
# to_key_val_list = utils.to_key_val_list
# default_headers = utils.default_headers  # redefine
# to_native_string = utils.to_native_string
# TooManyRedirects = exceptions.TooManyRedirects
# InvalidSchema = exceptions.InvalidSchema
# ChunkedEncodingError = exceptions.ChunkedEncodingError
# ContentDecodingError = exceptions.ContentDecodingError
# HTTPAdapter = adapters.HTTPAdapter
# requote_uri = utils.requote_uri
# get_environ_proxies = utils.get_environ_proxies
# get_netrc_auth = utils.get_netrc_auth
# should_bypass_proxies = utils.should_bypass_proxies
# get_auth_from_url = utils.get_auth_from_url
# codes = status_codes.codes
# REDIRECT_STATI = models.REDIRECT_STATI
# 
# def merge_setting(request_setting, session_setting, dict_class=...): ...
# def merge_hooks(request_hooks, session_hooks, dict_class=...): ...

# class SessionRedirectMixin:
#     def resolve_redirects(
#         self,
#         resp,
#         req,
#         stream: bool = False,
#         timeout: Incomplete | None = None,
#         verify: bool = True,
#         cert: Incomplete | None = None,
#         proxies: Incomplete | None = None,
#         yield_requests: bool = False,
#         **adapter_kwargs,
#     ): ...
#     def rebuild_auth(self, prepared_request, response): ...
#     def rebuild_proxies(self, prepared_request, proxies): ...
#     def should_strip_auth(self, old_url, new_url): ...
#     def rebuild_method(self, prepared_request: PreparedRequest, response: Response) -> None: ...
#     def get_redirect_target(self, resp: Response) -> str | None: ...

_Data: TypeAlias = (
    # used in requests.models.PreparedRequest.prepare_body
    #
    # case: is_stream
    # see requests.adapters.HTTPAdapter.send
    # will be sent directly to http.HTTPConnection.send(...) (through urllib3)
    Iterable[bytes]
    # case: not is_stream
    # will be modified before being sent to urllib3.HTTPConnectionPool.urlopen(body=...)
    # see requests.models.RequestEncodingMixin._encode_params
    # see requests.models.RequestEncodingMixin._encode_files
    # note that keys&values are converted from Any to str by urllib.parse.urlencode
    | str
    | bytes
    | SupportsRead[str | bytes]
    | list[tuple[Any, Any]]
    | tuple[tuple[Any, Any], ...]
    | Mapping[Any, Any]
)
_Auth: TypeAlias = tuple[str, str] | _auth.AuthBase | Callable[[PreparedRequest], PreparedRequest]
_Cert: TypeAlias = str | tuple[str, str]
# Files is passed to requests.utils.to_key_val_list()
_FileName: TypeAlias = str | None
_FileContent: TypeAlias = SupportsRead[str | bytes] | str | bytes
_FileContentType: TypeAlias = str
_FileCustomHeaders: TypeAlias = Mapping[str, str]
_FileSpecTuple2: TypeAlias = tuple[_FileName, _FileContent]
_FileSpecTuple3: TypeAlias = tuple[_FileName, _FileContent, _FileContentType]
_FileSpecTuple4: TypeAlias = tuple[_FileName, _FileContent, _FileContentType, _FileCustomHeaders]
_FileSpec: TypeAlias = _FileContent | _FileSpecTuple2 | _FileSpecTuple3 | _FileSpecTuple4
_Files: TypeAlias = Mapping[str, _FileSpec] | Iterable[tuple[str, _FileSpec]]
_Hook: TypeAlias = Callable[[Response], Any]
_HooksInput: TypeAlias = Mapping[str, Iterable[_Hook] | _Hook]

_ParamsMappingKeyType: TypeAlias = str | bytes | int | float
_ParamsMappingValueType: TypeAlias = str | bytes | int | float | Iterable[str | bytes | int | float] | None
_Params: TypeAlias = (
    SupportsItems[_ParamsMappingKeyType, _ParamsMappingValueType]
    | tuple[_ParamsMappingKeyType, _ParamsMappingValueType]
    | Iterable[tuple[_ParamsMappingKeyType, _ParamsMappingValueType]]
    | str
    | bytes
)
_TextMapping: TypeAlias = MutableMapping[str, str]
# _HeadersUpdateMapping: TypeAlias = Mapping[str, str | bytes | None]
_Timeout: TypeAlias = float | tuple[float, float] | tuple[float, None]
_Verify: TypeAlias = bool | str

# class _Settings(TypedDict):
#     verify: _Verify | None
#     proxies: _TextMapping
#     stream: bool
#     cert: _Cert | None

_HeadersMapping: TypeAlias = Mapping[str, str | bytes]

DEFAULT_HEADERS: dict[str, str]

def request(
    method: str | bytes,
    url: str | bytes,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
def get(
    url: str | bytes,
    params: _Params | None = None,
    *,
    attempts: int | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
def options(
    url: str | bytes,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
def head(
    url: str | bytes,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
def post(
    url: str | bytes,
    data: _Data | None = None,
    json: Incomplete | None = None,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
) -> ResponseProxy: ...
def put(
    url: str | bytes,
    data: _Data | None = None,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
def patch(
    url: str | bytes,
    data: _Data | None = None,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
def delete(
    url: str | bytes,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...

# CACHED REQESTS

def crequest(
    method: str | bytes,
    url: str | bytes,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...

# CACHED REQUESTS

def cget(
    url: str | bytes,
    params: _Params | None = None,
    *,
    attempts: int | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
def coptions(
    url: str | bytes,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
def chead(
    url: str | bytes,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
def cpost(
    url: str | bytes,
    data: _Data | None = None,
    json: Incomplete | None = None,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
) -> ResponseProxy: ...
def cput(
    url: str | bytes,
    data: _Data | None = None,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
def cpatch(
    url: str | bytes,
    data: _Data | None = None,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
def cdelete(
    url: str | bytes,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...

# ASYNCRONIZED, CACHED REQESTS

async def acrequest(
    method: str | bytes,
    url: str | bytes,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
async def acget(
    url: str | bytes,
    params: _Params | None = None,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
async def acoptions(
    url: str | bytes,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
async def achead(
    url: str | bytes,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
async def acpost(
    url: str | bytes,
    data: _Data | None = None,
    json: Incomplete | None = None,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
) -> ResponseProxy: ...
async def acput(
    url: str | bytes,
    data: _Data | None = None,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
async def acpatch(
    url: str | bytes,
    data: _Data | None = None,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
async def acdelete(
    url: str | bytes,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...

# ASYNCRONIZED REQESTS

async def arequest(
    method: str | bytes,
    url: str | bytes,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
async def aget(
    url: str | bytes,
    params: _Params | None = None,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
async def aoptions(
    url: str | bytes,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
async def ahead(
    url: str | bytes,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
async def apost(
    url: str | bytes,
    data: _Data | None = None,
    json: Incomplete | None = None,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
) -> ResponseProxy: ...
async def aput(
    url: str | bytes,
    data: _Data | None = None,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
async def apatch(
    url: str | bytes,
    data: _Data | None = None,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
async def adelete(
    url: str | bytes,
    run_in_executor: bool = True,
    *,
    attempts: int | None = ...,
    params: _Params | None = ...,
    data: _Data | None = ...,
    headers: _HeadersMapping | None = ...,
    cookies: RequestsCookieJar | _TextMapping | None = ...,
    files: _Files | None = ...,
    auth: _Auth | None = ...,
    timeout: _Timeout | None = ...,
    allow_redirects: bool = ...,
    proxies: _TextMapping | None = ...,
    hooks: _HooksInput | None = ...,
    stream: bool | None = ...,
    verify: _Verify | None = ...,
    cert: _Cert | None = ...,
    json: Incomplete | None = ...,
) -> ResponseProxy: ...
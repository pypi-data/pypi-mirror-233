from __future__ import annotations

# '#': 작동하긴 하지만 공식적으로 지원하지 않는 모듈
# '# #': 작동하지 않는 모듈
from requests import (


    ConnectTimeout,
    ConnectionError,
    # DependencyWarning,
    FileModeWarning,
    HTTPError,
    JSONDecodeError,
    # NullHandler,
    PreparedRequest,
    ReadTimeout,
    Request,
    RequestException,
    # RequestsDependencyWarning,
    Response,
    # # Session,
    Timeout,
    TooManyRedirects,
    URLRequired,
    __author__,
    __author_email__,
    __build__,
    # # __builtins__,
    # # __cached__,
    __cake__,
    __copyright__,
    __description__,
    # # __doc__,
    # # __file__,
    __license__,
    # # __loader__,
    # # __name__,
    # # __package__,
    # # __path__,
    # # __spec__,
    __title__,
    __url__,
    __version__,
    # _check_cryptography,
    # _internal_utils,
    adapters,
    # # api,
    auth,
    certs,
    # chardet_version,
    # charset_normalizer_version,
    check_compatibility,
    codes,
    compat,
    cookies,
    # # delete,
    exceptions,
    # # get,
    # # head,
    hooks,
    # logging,
    models,
    # # options,
    packages,
    # # patch,
    # # post,
    # # put,
    # # request,
    # session,
    sessions,
    # # ssl,
    status_codes,
    structures,
    # urllib3,
    utils,
    # warnings,
)

from .api_with_tools import (
    request,
    get, options, head, post, put, patch, delete,
    cget, coptions, chead, cpost, cput, cpatch, cdelete,
    acget, acoptions, achead, acpost, acput, acpatch, acdelete,
    aget, aoptions, ahead, apost, aput, apatch, adelete,
)
from .sessions_with_tools import Session


class session(Session):
    def __init__(self) -> None:
        import warnings
        warnings.warn('This class is deprecated. Use `Session`(Capitalized) instead.', DeprecationWarning)
        super().__init__()

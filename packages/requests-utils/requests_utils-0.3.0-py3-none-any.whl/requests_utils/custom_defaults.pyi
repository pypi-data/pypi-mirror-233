from . import api_with_tools


class CustomDefaults:
    get = staticmethod(api_with_tools.get)
    options = staticmethod(api_with_tools.options)
    head = staticmethod(api_with_tools.head)
    post = staticmethod(api_with_tools.post)
    put = staticmethod(api_with_tools.put)
    patch = staticmethod(api_with_tools.patch)
    delete = staticmethod(api_with_tools.delete)
    cget = staticmethod(api_with_tools.cget)
    coptions = staticmethod(api_with_tools.coptions)
    chead = staticmethod(api_with_tools.chead)
    cpost = staticmethod(api_with_tools.cpost)
    cput = staticmethod(api_with_tools.cput)
    cpatch = staticmethod(api_with_tools.cpatch)
    cdelete = staticmethod(api_with_tools.cdelete)
    acget = staticmethod(api_with_tools.acget)
    acoptions = staticmethod(api_with_tools.acoptions)
    achead = staticmethod(api_with_tools.achead)
    acpost = staticmethod(api_with_tools.acpost)
    acput = staticmethod(api_with_tools.acput)
    acpatch = staticmethod(api_with_tools.acpatch)
    acdelete = staticmethod(api_with_tools.acdelete)
    aget = staticmethod(api_with_tools.aget)
    aoptions = staticmethod(api_with_tools.aoptions)
    ahead = staticmethod(api_with_tools.ahead)
    apost = staticmethod(api_with_tools.apost)
    aput = staticmethod(api_with_tools.aput)
    apatch = staticmethod(api_with_tools.apatch)
    adelete = staticmethod(api_with_tools.adelete)

    def __init__(
            self,
            *,
            method=...,
            url=...,
            attempts=...,
            params=...,
            data=...,
            headers=...,
            cookies=...,
            files=...,
            auth=...,
            timeout=...,
            allow_redirects=...,
            proxies=...,
            hooks=...,
            stream=...,
            verify=...,
            cert=...,
            json=...,
    ):
        ...

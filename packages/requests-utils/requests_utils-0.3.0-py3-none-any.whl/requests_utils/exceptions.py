from __future__ import annotations


class EmptyResultError(Exception):
    def __init__(self, error_message: str, selector: str | None = None, url=None, status_code: int | None = None) -> None:
        if not url:
            url = "(can't show URL probably because `markup_or_response` parameter was string)"

        error_message = error_message.rstrip()

        error_string = (
            f'{error_message} '
            'This error happens probably because of invalid selector or URL. '
            'Check if both selector and URL are valid. '
            'Set to False `no_empty_result` if empty list is intended. '
            'It may also because of selector is not matched with URL.\n'
            f'selector: {selector}, URL: {url}'
        )

        if str(status_code)[0] in {'4', '5'}:
            error_string = (f'WARNING: status code (HTTP{status_code}) looks odd. '
                            f'check your identity, headers, and URL again.\n{error_string}')

        super().__init__(error_string)


class NoParserError(Exception):
    pass


class NotAResponseError(Exception):
    pass

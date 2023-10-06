def clean_headers(raw_headers: str):
    is_name = True
    name: str = ''
    headers = {}
    for i, line in enumerate(filter(None, raw_headers.splitlines())):
        if not is_name:
            headers[name] = line
            is_name = True
            continue

        if line[-1] != ':':
            raise ValueError(f'Unexpected string: {line} on {i + 1}th line.')

        name = line.removesuffix(':')
        is_name = False

    return headers

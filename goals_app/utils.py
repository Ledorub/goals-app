import re


def split_camel_case(identifier):
    return re.findall(
        r'[A-Z][a-z]+|[0-9A-Z]+(?=[A-Z][a-z])'
        r'|[0-9A-Z]{2,}|[a-z0-9]{2,}|[a-zA-Z0-9]',
        identifier
    )


def camel_case_to_snake_case(identifier):
    words = split_camel_case(identifier)
    words = map(str.lower, words)
    return '_'.join(words)

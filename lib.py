def match_tag(line: str, tag: str) -> bool:
    return line[:len(tag)+1] == f'%{tag}'


def tag_param(line: str) -> str:
    return ''.join(line.split('%')).replace(' ', '').split(':')[1]


def reverse_bool(flag: bool) -> bool:
    if flag:
        return False
    else:
        return True

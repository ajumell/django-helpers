def remove_breaks(string):
    while string.find('\n') >= 0:
        string = string.replace('\n', '')
    return string


def remove_extra_space(string):
    while string.find('  ') >= 0:
        string = string.replace('  ', ' ')
    return string
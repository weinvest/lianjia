
def extract(selector):
    if selector is None:
        return ''

    v = selector.extract_first()
    if v is None:
        return ''
    return v
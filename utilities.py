import re

def clean_str(s: str) -> str:
    return str.lower(re.sub('\s|\.|,|!|\?|:|;|-|"|\'', '', s))

def parse_user_bool(s: str) -> bool:
    s = clean_str(s)
    if any(map(lambda x : x in s, ['declin', 'den', 'false', 'nah', 'nay', 'negative', 'no', 'refus', 'reject', '0'])) or s == 'n':
        return False
    if any(map(lambda x : x in s, ['absolutely', 'affirm', 'confirm', 'def', 'goahead', 'indeed', 'ok', 'positive', 'sure', 'tru', 'ya', 'ye', '1'])) or s == 'y':
        return True
    return parse_user_bool(input('Huh?\n'))
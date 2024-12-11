import re

def clean_str(s: str) -> str:
    return str.lower(re.sub('\s|\.|,|!|\?|:|;|-|"|\'', '', s))

def parse_user_bool(s: str) -> bool:
    s = clean_str(s)
    if any(map(lambda x : x in s, ['declin', 'den', 'false', 'nah', 'nay', 'negative', 'no', 'refus', 'reject', '0'])):
        return False
    if any(map(lambda x : x in s, ['absolutely', 'affirm', 'confirm', 'goahead', 'indeed', 'positive', 'tru', 'ye', '1'])):
        return True
    return parse_user_bool(input('Huh?\n'))
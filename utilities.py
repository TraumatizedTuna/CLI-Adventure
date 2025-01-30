import re

def clean_str(s: str) -> str:
    return str.lower(re.sub('\s|\.|,|!|\?|:|;|-|"|\'', '', s))

def parse_user_bool(s: str,  insist = True, insist_msg = 'Huh?') -> bool:
    s = clean_str(s)
    if any(map(lambda x : x in s, ['declin', 'den', 'false', 'nah', 'nay', 'negative', 'no', 'refus', 'reject', '0'])) or s == 'n':
        return False
    if any(map(lambda x : x in s, ['absolutely', 'affirm', 'confirm', 'def', 'goahead', 'indeed', 'ok', 'positive', 'sure', 'tru', 'ya', 'ye', '1'])) or s == 'y':
        return True
    if insist: return parse_user_bool(input(insist_msg + '\n'), insist, insist_msg)
    else: return False


# Method that figures out what player wants to interact with and calls its interact() function
def choose_action(user_input: str, actions: list):
    action = None
    # Loop to insist on valid input
    while True:
        try:
            action = actions[int(user_input)-1]
            break
        except:
            # Politely ask user to provide valid input
            user_input = input('Try again stupid\n')

    action.interact()
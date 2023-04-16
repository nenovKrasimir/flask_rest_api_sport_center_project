import random
import re


def hide_identity(client_id):
    symbols = ["@!>a/.-m", "$$!!xaaw!x", "-#%^&"]
    hashed_identity = ""
    for hiding_identity in range(len(client_id)):
        hashed_identity += client_id[hiding_identity] + random.choice(symbols)
    return hashed_identity


def see_identity(client_id):
    return "".join(re.findall(r"\d+", client_id))

import re

bad_chars = re.compile(r"[^A-Za-z0-9_. ]+|^\.|\.$|^ | $|^$")
bad_names = re.compile(r"(aux|com[1-9]|con|lpt[1-9]|prn)(\.|$)")


def sanitize_name(s: str) -> str:
    """It transforms string to the conventional path and file names this including
    turning white space into underscore character
    """
    name = bad_chars.sub("_", s)
    if bad_names.match(name):
        name = "_" + name
    return name


def sanitize_author_name(name: str) -> str:
    """It takes author name string which is returned author_catalog function
    and returns valid directory name as a string.
    """
    name = name.rsplit(",", 1)
    name = name[0].split(",")
    if len(name) == 2:
        last_name, first_name = name
        name = f"{first_name[1:]} {last_name}".replace(" ", "_").lower()
    else:
        name = name[0].replace(" ", "_").lower()
    return name

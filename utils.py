import re

flatten = lambda list: [item for sublist in list for item in sublist]


def split_email(email):
    """Splits an email into headers and the abstract"""

    pattern = r"([\S\s]+?Abstract: \n)([\S\s]+)"
    split_email = re.search(pattern, email)

    headers = split_email.group(1)
    abstract = split_email.group(2)

    return [headers, abstract]

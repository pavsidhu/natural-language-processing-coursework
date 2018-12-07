import re

tags = ["sentence", "paragraph", "stime", "etime", "location", "speaker"]

flatten = lambda list: [item for sublist in list for item in sublist]

stringify_nested_array = lambda list: [" ".join(item) for item in list]


def split_email(email):
    """Splits an email into headers and the abstract"""

    pattern = r"([\S\s]+?Abstract: \n)([\S\s]+)"
    split_email = re.search(pattern, email)

    headers = split_email.group(1)
    abstract = split_email.group(2)

    return [headers, abstract]

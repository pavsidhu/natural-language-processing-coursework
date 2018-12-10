import re

tags = ["sentence", "paragraph", "stime", "etime", "location", "speaker"]

flatten = lambda list: [item for sublist in list for item in sublist]

stringify_nested_array = lambda list: [" ".join(item).lower() for item in list]


def split_email(email):
    """Splits an email into headers and the abstract"""

    pattern = r"([\S\s]+?Abstract: \n)([\S\s]+)"
    split_email = re.search(pattern, email)

    headers = split_email.group(1)
    abstract = split_email.group(2)

    return [headers, abstract]


def remove_duplicates(list):
    """Removes duplicate sublists in a list (case-insensitive)"""

    stringified_list = set(stringify_nested_array(list))
    unique_list = set()

    for i, value in enumerate(stringified_list):
        duplicate = False

        # Loop through names and check it's not a substring of another
        for j, sublist in enumerate(stringified_list):
            if i != j and value.lower() in sublist.lower():
                duplicate = True
                break

        if not duplicate:
            unique_list.add(value)

    return unique_list

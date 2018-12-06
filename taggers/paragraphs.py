import re


def tag_paragraphs(email):
    """
    Tag the start and end of paragraphs:
        <paragraphs>
            Ad aliqua velit ad ut ea velit do ullamco nisi non ex irure. Cillum
            consectetur enim ad velit sunt ullamco voluptate reprehenderit amet.
        </paragraph>
    """

    # Split the each into the meta data and the abstract
    pattern = r"([\S\s]+?Abstract: \n)([\S\s]+)"
    split_email = re.search(pattern, email)

    header = split_email.group(1)
    abstract = split_email.group(2)

    # Tag each paragraph in the abstract
    pattern = r"\n([A-Z0-9\"'](?:.+(?:\n(?!\n)))+.+\.)"
    replace = r"\n<paragraph>\1</paragraph>"
    abstract = re.sub(pattern, replace, abstract)

    # Put the meta data and abstract back together again
    email = header + abstract

    return email

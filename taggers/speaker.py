from nltk import pos_tag
from nltk.tokenize import word_tokenize
import re

from utils import stringify_nested_array


def tag_speaker(email, original_email, stanford_tags, tagged_speakers):
    """
    Tag speaker:
        <speaker>{{ speaker }}</speaker>
    """

    email, success = tag_with_regex(email)
    if success:
        return email

    email, success = tag_with_stanford_tagger(email, original_email, stanford_tags)
    if success:
        return email

    return email


def tag_with_regex(email):
    """
    Attempt to find the speaker using Regex
    """

    # Search for "SPEAKER: Michael Lee, CTO of Tech LTD"
    pattern = r"(?:Speaker|Who|Name):\s([^,<(\[\n]*)"
    search = re.search(pattern, email, flags=re.IGNORECASE)

    # If no results found, regex did not work
    if not search:
        return [email, False]

    name = search.group(1)
    email = tag_speaker_using_name(name, email)

    # If the speaker is a PHD, tag that inside the speaker too
    pattern = r"(</speaker>)(, PhD)"
    replace = r"\2\1"
    email = re.sub(pattern, replace, email)

    return [email, True]


# TODO: Handle multiple names
def tag_with_stanford_tagger(email, original_email, stanford_tags):
    """
    Uses the Stanford tagger as a last resort since it takes a long time to
    process
    """

    names = []
    i = 0

    # Get names from tagged text
    while i < len(stanford_tags):
        name = []

        # Chunk names
        while stanford_tags[i][1] == "PERSON":
            if i + 1 >= len(stanford_tags):
                name.append(stanford_tags[i][0])
                i += 1
                break

            name.append(stanford_tags[i][0])
            i += 1

        i += 1

        if name:
            names.append(name)

    unique_names = remove_duplicates_from_name(names)

    if unique_names:
        email = tag_speaker_using_name(unique_names[0], email)

        return [email, True]
    # Handle multiple potential speakers

    return [email, False]


def remove_duplicates_from_name(names):
    stringified_names = stringify_nested_array(names)

    unique_names = []

    # Remove duplicate names from names list such as single surnames
    # that are already part of a full name in the list
    for i, name in enumerate(stringified_names):
        duplicate = False

        # Loop through names and check it's not a substring of another
        for j, stringified_name in enumerate(stringified_names):
            if i != j and name in stringified_name:
                duplicate = True
                break

        if not duplicate:
            unique_names.append(name)

    return unique_names


# TODO: Support titles
def tag_speaker_using_name(name, email):
    """
    Adds the tags to the email for a given name
    """

    names = name.split()

    # Tag each name in the email
    for name in names:
        escaped_name = re.escape(name)
        pattern = rf"(\s|:)(?!<speaker>){escaped_name}(?!</speaker>)(\s|,|')"
        replace = rf"\1<speaker>{name}</speaker>\2"

        email = re.sub(pattern, replace, email)

    # Chunk together names next to each other
    pattern = r"</speaker>(, | )<speaker>"
    replace = r"\1"
    email = re.sub(pattern, replace, email)

    return email


def tag_speaker_using_name_with_title(title, name, email):
    """
    Adds the tags to the email for a given name that has a title
    """

    names = name.split()

    # Tag each name in the email
    for name in names:
        pattern = rf"(\s|:)(?!<speaker>){name}(?!</speaker>)(\s|,)"
        replace = rf"\1<speaker>{name}</speaker>\2"

        email = re.sub(pattern, replace, email)

    # Chunk together names next to each other
    pattern = r"</speaker>(, | )<speaker>"
    replace = r"\1"
    email = re.sub(pattern, replace, email)

    return email

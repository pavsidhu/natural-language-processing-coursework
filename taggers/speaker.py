from nltk import pos_tag
from nltk.tokenize import word_tokenize
import re

from utils import split_email, stringify_nested_array


def tag_speaker(email, original_email, stanford_tags, tagged_speakers):
    """
    Tag speaker:
        <speaker>{{ speaker }}</speaker>
    """

    email, success = tag_with_regex(email)
    if success:
        return email

    email = tag_with_stanford_tagger(email, original_email, stanford_tags)

    return email


def tag_with_regex(email):
    """
    Attempt to find the speaker using Regex
    """

    # Search for "SPEAKER: Michael Lee, CTO of Tech LTD"
    pattern = r"(?:Speaker|Who|Name|Instructor):\s([^,<(\[\n]*)"
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

    # if len(unique_names) == 1:
    #     email = tag_speaker_using_name(unique_names.pop(), email)
    if len(unique_names) > 0:
        names = find_speaker_from_names(unique_names, original_email)

        for name in names:
            email = tag_speaker_using_name(name, email)

    return email


def remove_duplicates_from_name(names):
    stringified_names = set(stringify_nested_array(names))
    # stringified_names = {v.lower(): v for v in stringified_names}.values()
    unique_names = set()

    # Remove duplicate names from names list such as single surnames
    # that are already part of a full name in the list
    for i, name in enumerate(stringified_names):
        duplicate = False

        # Loop through names and check it's not a substring of another
        for j, stringified_name in enumerate(stringified_names):
            if i != j and name.lower() in stringified_name.lower():
                duplicate = True
                break

        if not duplicate:
            unique_names.add(name)

    return unique_names


def find_speaker_from_names(names, original_email):
    """
    Given a list of names, find the real speaker
    """

    names = remove_posted_by_name(names, original_email)

    speaker = check_if_speaker_in_topic_header(names, original_email)
    if speaker:
        return [speaker]

    # speaker = get_speakers_using_title(names, original_email)
    # if speaker:
    #     return [speaker]

    speakers = get_speakers_using_sentence_detection(names, original_email)
    if speakers:
        return speakers

    # tokens = word_tokenize(original_email)
    # tags = pos_tag(tokens)
    # for name in names:
    # for tag in pos_tag(tokens):
    #     i = 0
    #     found = False

    #     while i <= len(name):
    #         if tag[i] == name[i]:

    #         i += 1

    return []


def check_if_speaker_in_topic_header(names, email):
    """Get name from Topic header if available and check it's the speaker"""

    pattern = r"Topic:\s?(.*)"
    search = re.search(pattern, email)

    if not search.groups():
        return None

    for name in names:
        if name in search.group(1):
            return name


def remove_posted_by_name(names, email):
    """Remove the PostedBy name from the names"""

    pattern = r"PostedBy:\s?(.*?)\son(?:.+\((.+?)\)\n)?"
    search = re.search(pattern, email)

    # Some names have a period instead of a space between their first and
    # last name, so replace it with a space
    posted_by = search.group(1).replace(".", " ")

    if posted_by:
        if posted_by in names:
            names.remove(posted_by)

        for n in posted_by.split():
            if n in names:
                names.remove(n)

    # Handle possible name in brackets after PostedBy
    posted_by = search.group(2)

    if posted_by:
        if posted_by in names:
            names.remove(posted_by)

        for n in posted_by.split():
            if n in names:
                names.remove(n)

    return names


def get_speakers_using_sentence_detection(names, email):
    """Look for patterns such as "{{ speaker }} will be talking about"""

    headers, abstract = split_email(email)

    speakers = []

    for name in names:
        escaped_name = re.escape(name)
        pattern_1 = rf"{escaped_name}[\S\s]+?will"
        search_1 = re.search(pattern_1, abstract)

        if search_1:
            speakers.append(name)

        pattern_2 = rf"(present|talk by)[\S\s]+?{escaped_name}"
        search_2 = re.search(pattern_2, abstract)

        if search_2:
            speakers.append(name)

    return speakers


# TODO: Support titles
def tag_speaker_using_name(name, email):
    """Adds the tags to the email for a given name"""

    names = name.split()

    # Tag each name in the email
    for name in names:
        escaped_name = re.escape(name)
        pattern = rf"(\s|:|>)(?!<speaker>)({escaped_name})(?!</speaker>)(\s|,|'|\")"
        replace = r"\1<speaker>\2</speaker>\3"

        email = re.sub(pattern, replace, email, flags=re.IGNORECASE)

    # Chunk together names next to each other
    pattern = r"</speaker>(, | |\n)<speaker>"
    replace = r"\1"
    email = re.sub(pattern, replace, email)

    # In case PostedBy is accidently taggedm remove it
    pattern = r"(PostedBy:.*)<speaker>(.*)</speaker>(.*)"
    replace = r"\1\2\3"
    email = re.sub(pattern, replace, email)

    return email

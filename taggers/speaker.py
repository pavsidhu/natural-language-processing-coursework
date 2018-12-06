from nltk import pos_tag
from nltk.tokenize import word_tokenize
import re


def tag_speaker(email, tagged_speakers):
    """
    Tag speaker:
        <speaker>{{ speaker }}</speaker>
    """

    email, success = tag_with_regex(email)

    if success:
        return email

    # tokens = word_tokenize(original_email)
    # tagged_email = pos_tag(tokens)

    # for tag in tagged_email:
    #     word, type = tag

    #     if type == "NNP" and is_name(word.lower(), tagged_speakers):
    #         pattern = rf"(\s)(?!<speaker>){word}(?!</speaker>)(\s)"
    #         replace = rf"\1<speaker>{word}</speaker>\2"

    #         email = re.sub(pattern, replace, email)

    return email


def tag_with_regex(email):
    """
    Attempt to find the speaker using Regex
    """

    # Search for "SPEAKER: Michael Lee, CTO of Tech LTD"
    pattern = r"(?:Speaker|Who):\s([^,<(\[\n]*)"
    search = re.search(pattern, email, flags=re.IGNORECASE)

    # If no results found, regex did not work
    if not search:
        return [email, False]

    names = search.group(1).split()

    # Tag each name in the email
    for name in names:
        pattern = rf"(\s|:)(?!<speaker>){name}(?!</speaker>)(\s|,)"
        replace = rf"\1<speaker>{name}</speaker>\2"

        email = re.sub(pattern, replace, email)

    # Chunk together names next to each other
    pattern = r"</speaker>(, | )<speaker>"
    replace = r"\1"
    email = re.sub(pattern, replace, email)

    # If the speaker is a PHD, tag that inside the speaker too
    pattern = r"(</speaker>)(, PhD)"
    replace = r"\2\1"
    email = re.sub(pattern, replace, email)

    return [email, True]


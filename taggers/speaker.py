from nltk import pos_tag
from nltk.tokenize import word_tokenize
import re


def tag_speaker(email, tagged_speakers):
    """
    Tag speaker:
        <speaker>{{ speaker }}</speaker>
    """

    tokens = word_tokenize(email)
    tagged_email = pos_tag(tokens)

    for tag in tagged_email:
        if tag[1] == "NNP" and tag[0].lower() in names:
            pattern = r"(?!<speaker>)" + tag[0] + r"(?!</speaker>)"
            replace = "<speaker>" + tag[0] + "</speaker>"
            email = re.sub(pattern, replace, email)

    email = email.replace("</speaker> <speaker>", " ")

    return email

from nltk.tag import UnigramTagger, BigramTagger, TrigramTagger, DefaultTagger
from nltk.tokenize import sent_tokenize
import re

from taggers.paragraphs import tag_paragraphs
from taggers.sentences import tag_sentences
from taggers.time import tag_time
from taggers.date import tag_date
from taggers.speaker import tag_speaker
from taggers.location import tag_location

tags = ["sentence", "paragraph", "stime", "etime", "location", "speaker"]

# Regex patterns to match tags
patterns = [str.format(r"<{}>([\S\s]+?)</{}>", tag, tag) for tag in tags]


def extract_tag_data(emails):
    """Extracts all the data from the tags in each email"""

    # Generate an dictionary to hold extracted data
    extracted_tags_data = dict((tag, []) for tag in tags)

    for email in emails:

        # Search for instances of each tag and add it to the results
        for tag, pattern in zip(tags, patterns):
            results = re.findall(pattern, email)

            extracted_tags_data[tag].extend(results)

    return extracted_tags_data


def remove_tags(emails):
    """Removes all the tags from each email"""

    untagged_emails = []

    for email in emails:
        # Go through each possible tag and remove it
        for pattern in patterns:
            email = re.sub(pattern, r"\1", email)

        untagged_emails.append(email)

    return untagged_emails


def tag_emails(emails, tags):
    """Helper function to tag a list of emails"""

    return [tag_email(email, tags) for email in emails]


def tag_email(email, tags):
    """Tags a single email"""

    email = tag_paragraphs(email)
    email = tag_sentences(email)
    email = tag_time(email)
    email = tag_date(email)
    email = tag_speaker(email, tags["speaker"])
    email = tag_location(email, tags["location"])

    return email

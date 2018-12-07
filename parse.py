from nltk.tag import UnigramTagger, BigramTagger, TrigramTagger, DefaultTagger
from nltk.tokenize import sent_tokenize
from nltk import StanfordNERTagger, word_tokenize
from os import getcwd
import re

from taggers.paragraphs import tag_paragraphs
from taggers.sentences import tag_sentences
from taggers.time import tag_time
from taggers.speaker import tag_speaker
from taggers.location import tag_location
from utils import tags

# Regex patterns to match tags
patterns = [str.format(r"<{}>([\S\s]+?)</{}>", tag, tag) for tag in tags]

# Regex pattern to remove unneeded tags from extracted data
nested_tag_pattern = r"</?(?:" + r"|".join(tags) + r")>"


def extract_tag_data(emails):
    """Extracts all the data from the tags in each email"""

    # Generate an dictionary to hold extracted data
    extracted_tags_data = dict((tag, []) for tag in tags)

    for email in emails:
        # Search for instances of each tag and add it to the results
        for tag, pattern in zip(tags, patterns):
            results = re.findall(pattern, email)

            # Remove nested tags from data i.e. sentence tags in paragraphs
            for i, result in enumerate(results):
                results[i] = re.sub(nested_tag_pattern, "", result)

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


# Initiate Stanford tagger
stanford_classifier = getcwd() + "/english.all.3class.distsim.crf.ser.gz"
stanford_ner_path = getcwd() + "/stanford-ner.jar"
stanford_tagger = StanfordNERTagger(
    stanford_classifier, stanford_ner_path, encoding="utf-8"
)


def tag_with_stanford_tagger(emails):
    """
    Tags a list of emails using the Stanford NER tagger
    """

    # Remove PostedBy header and first line in the email since it always
    # contains an unneeded name
    pattern = r"(^.*\n|PostedBy:.*\n)"
    replace = ""
    emails = [re.sub(pattern, replace, email) for email in emails]

    # Tokenize and tag the emails
    tokens = [word_tokenize(email) for email in emails]
    tags = stanford_tagger.tag_sents(tokens)

    return tags


def tag_emails(emails, tags):
    """Helper function to tag a list of emails"""

    stanford_tags = tag_with_stanford_tagger(emails)

    tagged_emails = [
        tag_email(emails[i], stanford_tags[i], tags) for i in range(0, len(emails))
    ]

    return tagged_emails


def tag_email(original_email, stanford_tags, tags):
    """Tags a single email"""

    email = tag_paragraphs(original_email)
    email = tag_sentences(email)
    email = tag_time(email)
    email = tag_speaker(email, original_email, stanford_tags, tags["speaker"])
    email = tag_location(email, tags["location"])

    return email

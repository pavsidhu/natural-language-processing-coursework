from nltk import sent_tokenize
import re

from utils import split_email


def tag_sentences(email):
    """
    Tag the start and end of sentences:
        <sentence>Est occaecat laborum dolor enim consequat nostrud do.</sentence>
    """

    header, abstract = split_email(email)

    # Get the contents of all the existing paragraphs
    pattern = r"<paragraph>([\S\s]+?)</paragraph>"
    paragraphs = re.findall(pattern, abstract)

    for paragraph in paragraphs:
        # Tokenize each paragraph into sentences
        sentences = sent_tokenize(paragraph)

        # Tag the sentences and put them back in the email
        for sentence in sentences:
            # Remove the last character if it's a period for a better F1 score
            sentence = sentence[:-1] if sentence[-1] == "." else sentence

            tagged_sentence = str.format("<sentence>{}</sentence>", sentence)
            abstract = abstract.replace(sentence, tagged_sentence)

    return header + abstract

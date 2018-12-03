from nltk import sent_tokenize
import re


def tag_sentences(email):
    """
    Tag the start and end of sentences:
        <sentence>Est occaecat laborum dolor enim consequat nostrud do.</sentence>
    """

    # Get the contents of all the existing paragraphs
    pattern = r"<paragraph>([\S\s]+?)</paragraph>"
    paragraphs = re.findall(pattern, email)

    for paragraph in paragraphs:
        # Tokenize each paragraph into sentences
        sentences = sent_tokenize(paragraph)

        for sentence in sentences:
            # Tag the sentences and put them back in the email
            tagged_sentence = str.format("<sentence>{}</sentence>", sentence)
            email = email.replace(sentence, tagged_sentence)

    return email
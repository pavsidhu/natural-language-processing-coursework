from nltk import FreqDist, word_tokenize
from nltk.corpus import stopwords as sw
from gensim.models import KeyedVectors
import re

from file_io import get_emails
import ontology_tree as tree
from utils import flatten

from anytree import Node, PostOrderIter


def construct_ontology():
    """Tag each email with an ontology from a generated ontology tree"""

    print("Fetching emails...")
    emails = get_emails("/test_untagged", file_name=True)

    stopwords = sw.words("english")

    print("Loading model...")
    model = KeyedVectors.load_word2vec_format(
        "GoogleNews-vectors-negative300.bin", binary=True, limit=10000
    )

    print("Classifying emails...")
    classified_emails = [
        {
            "name": email[0],
            "email": get_posted_by(email[1]),
            "topic": classify_email(email[1], model, stopwords),
        }
        for email in emails
    ]

    for email in classified_emails:
        path = get_node_path(email["topic"]) if email["topic"] else "empty"
        name = email["name"].ljust(10)
        print(name, path)


def classify_email(email, model, stopwords):
    """Classify an email to a given ontology"""

    if not email:
        return None

    topic = classify_with_word_vectors(email, model, stopwords)
    if topic and topic.name != "subject":
        return topic

    topic = classify_with_type_header(email)
    if topic:
        return topic

    return tree.computing


def classify_with_type_header(email):
    """Use the type header if available to attempt to classify the email"""

    type_header = get_type_header(email)

    if type_header in ["CS Seminar", "cmu.cs.scs", "Special CS Seminar'"]:
        return tree.computing
    elif type_header in [
        "Robotics Seminar",
        "cmu.cs.robotics",
        "cmu.cs.robotics.students",
        "Robotics Institute",
    ]:
        return tree.robotics
    elif type_header in ["AI Seminar"]:
        return tree.artificial_intelligence
    elif type_header in ["cmu.misc.environmental-health-and-safety"]:
        return tree.health_and_safety

    return None


def classify_with_word_vectors(email, model, stopwords):
    words = get_abstract_words(email)
    uncommon_words = list(filter(lambda word: not word in stopwords, words))

    topic = None
    top_similarity = 0.0

    for node in PostOrderIter(tree.subjects):
        total_similarity = 0.0

        for word in uncommon_words:
            similarity = 0.0

            try:
                similarity = model.similarity(word, node.name)
            except KeyError:
                pass

            total_similarity += similarity

        similarity = total_similarity / len(words)

        if similarity > top_similarity:
            topic = node
            top_similarity = similarity

    return topic


def get_abstract_words(email):
    """Gets the tokens from the abstract from an email"""

    pattern = r"([\S\s]+?Abstract: \n)([\S\s]+)"
    search = re.search(pattern, email)

    if search:
        abstract = search.group(2)
        tokens = word_tokenize(abstract)

        return tokens

    return None


def get_type_header(email):
    """Gets the type header from an email"""

    pattern = r"Type:\s{4}(.*)\n"
    search = re.search(pattern, email)

    if search:
        return search.group(1).lstrip()

    return None


def get_posted_by(email):
    """Gets the PostedBy header from an email"""

    pattern = r"PostedBy:\s(.*)\n"
    search = re.search(pattern, email)

    if search:
        return search.group(1)

    return None


def calculate_word_frequency(topic_headers):
    """Calculates the word frequencies in topic headers"""

    tokens = flatten([word_tokenize(topic_header) for topic_header in topic_headers])

    tokens = [
        word.lower()
        for word in tokens
        if not word.lower() in stopwords.words("english")
    ]

    word_frequencies = FreqDist(word.lower() for word in tokens)

    top_word_frequencies = word_frequencies.most_common(500)

    for x in top_word_frequencies:
        print(x)

    return top_word_frequencies


def get_node_path(node):
    """Returns the node path as a string"""

    if not node.parent:
        return node.name

    return f"{get_node_path(node.parent)} --> {node.name}"

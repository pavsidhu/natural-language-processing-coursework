import sys

from file_io import *
from parse import *
from f1_score import *
from ontology import *


def main(training):
    path = "/training" if training else "/untagged"

    original_emails = get_emails(path)

    tags = extract_tag_data(original_emails if training else get_emails("/training"))

    # Remove tags from tagged data if training
    emails = remove_tags(original_emails) if training else original_emails

    # Tag the emails
    parsed_emails = tag_emails(emails, tags)

    # Compare original data with parsed data to check accuracy
    if training:
        print_f1_score(original_emails, parsed_emails)

    output(parsed_emails)


if __name__ == "__main__":
    if len(sys.argv) == 1 or not sys.argv[1] in ["train", "test", "ontology"]:
        print('Please specify either "train", "test" or "ontology" as an argument')
        sys.exit()

    training = sys.argv[1] == "train"

    if sys.argv[1] == "ontology":
        construct_ontology()
    else:
        main(training)

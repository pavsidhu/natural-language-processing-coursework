from file_io import *
from parse import *
from compare import *
import sys


def main(training):
    path = "/training" if training else "/untagged"
    a = 90
    original_emails = get_emails(path)

    emails = original_emails
    tags = extract_tag_data(emails)

    # Remove tags from tagged data if training
    if training:
        emails = remove_tags(emails)

    # Tags the email
    parsed_emails = tag_emails(emails, tags)

    # Compare original data with parsed data to check accuracy
    if training:
        compare_emails(original_emails, parsed_emails)

    output(parsed_emails)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('Please specify either "train" or "test" as an argument')
        sys.exit()

    training = sys.argv[1] == "train"

    main(training)

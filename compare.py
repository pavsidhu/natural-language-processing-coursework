from parse import extract_tag_data


def compare_emails(original_emails, parsed_emails):
    """Compare emails and return the accuracy"""

    for i in range(0, len(original_emails)):
        original_email = original_emails[i]
        parsed_email = parsed_emails[i]

        original_email_data = extract_tag_data([original_email])
        parsed_email_data = extract_tag_data([parsed_email])

        for tag in ["paragraph", "sentence"]:
            f1_score = get_f1_score(tag, original_email_data, parsed_email_data)
            print(f"{tag}: {f1_score:.2f}")

        print("\n")


def get_f1_score(tag, original_email_data, parsed_email_data):
    """Calculates the f1 score of a tagged email and a retagged email"""

    true_positives = 0
    false_negatives = 0

    for data in parsed_email_data[tag]:
        if data in original_email_data[tag]:
            true_positives += 1

    for data in original_email_data[tag]:
        if not data in parsed_email_data[tag]:
            false_negatives += 1

    length = len(parsed_email_data[tag])

    precision = (true_positives / length) if length else 1
    recall = (true_positives / false_negatives) if false_negatives else 1

    if precision + recall == 0.0:
        return 0

    f1 = 2 * ((precision * recall) / (precision + recall))

    return f1

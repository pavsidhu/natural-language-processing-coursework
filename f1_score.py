from parse import extract_tag_data
from utils import tags


def print_f1_score(original_emails, parsed_emails):
    """Compare emails and print the f1 scores for each tag"""

    # Stores for each tag, the sum of the f1 scores
    sum_f1_scores = dict.fromkeys(tags, 0.0)

    for i in range(0, len(original_emails)):
        # Get tag data for the original and parsed email
        original_email_tags = extract_tag_data(original_emails[i : i + 1])
        parsed_email_tags = extract_tag_data(parsed_emails[i : i + 1])

        # Update the f1 sum for each tag
        for tag in tags:
            sum_f1_scores[tag] += get_f1_score(
                tag, original_email_tags, parsed_email_tags
            )

    print("F1 SCORES:")

    for tag, sum in sum_f1_scores.items():
        # Calculate the average f1 score
        average = sum / len(original_emails)

        # Prints in the format "Speaker: 0.80"
        print(f"{tag}: {average:.2f}")


def get_f1_score(tag, original_email_data, parsed_email_data):
    """Calculates the f1 score of a tagged email and a retagged email"""

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    # Calculate true positives
    for data in parsed_email_data[tag]:
        if data in original_email_data[tag]:
            true_positives += 1
        else:
            false_positives += 1

    # Calculate false negatives
    for data in original_email_data[tag]:
        if not data in parsed_email_data[tag]:
            false_negatives += 1

    precision = (
        (true_positives / (true_positives + false_positives))
        if false_positives
        else 1.0
    )
    recall = (true_positives / false_negatives) if false_negatives else 1.0

    f1 = (
        2 * ((precision * recall) / (precision + recall))
        if precision and recall
        else 0.0
    )

    return f1

from os import listdir, getcwd
from os.path import isfile, join
from nltk.corpus.reader import PlaintextCorpusReader
import os


def get_emails(path):
    """
    Returns a list of readers for all the files in the path
    """

    full_path = getcwd() + path
    files = [file for file in listdir(full_path) if isfile(join(full_path, file))]

    readers = [PlaintextCorpusReader(full_path, file).raw() for file in files]

    return readers


def output(emails):
    """
    Outputs a list of emails to the output/ directory
    """

    i = 0

    # Create output directory
    os.makedirs(os.path.dirname("output/"), exist_ok=True)

    for email in emails:
        # Generate file name
        file_name = str.format("output/{}.txt", i)

        # Save email to file
        with open(file_name, "w+") as file:
            file.write(str(email))

        i += 1

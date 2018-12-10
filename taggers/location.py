from nltk import RegexpParser, pos_tag, Tree
import requests
import re
import time

from utils import remove_duplicates


def tag_location(email, original_email, stanford_tags, tagged_locations):
    """
    Tag locations:
        <location>{{ location }}</location>
    """

    location = find_using_regex(original_email)
    if location:
        email = add_tags(email, location)
        return email

    email, success = find_using_tagged_locations(email, tagged_locations)
    if success:
        return email

    location = find_using_patterns(original_email)
    if location:
        email = add_tags(email, location)

    location = find_using_stanford_tagger(stanford_tags)
    if location:
        email = add_tags(email, location)

    email = email.replace("</location> <location>", "")
    email = email.replace("</location>, <location>", ", ")

    return email


def find_using_regex(email):
    """Use Regex to find a location"""

    pattern = r"(?:Place|Where):\s+(.+)"
    search = re.search(pattern, email, flags=re.IGNORECASE)

    return search.group(1) if search else None


def find_using_tagged_locations(email, tagged_locations):
    """Use the tagged dataset locations to find a match"""

    success = False

    for location in tagged_locations:
        escaped_location = re.escape(location)
        pattern = rf"(?<!<location>)({escaped_location})(?!</location>)"
        replace = r"<location>\1</location>"

        if re.search(pattern, email):
            email = re.sub(pattern, replace, email, flags=re.IGNORECASE)
            success = True
            break

    return [email, success]


def find_using_patterns(email):
    """Use sentence/location patterns to find the right location"""

    pattern = r"(?:\s|\n)(\S+\s?\d{4})"
    search = re.search(pattern, email)

    return search.group(1) if search else None


def find_using_stanford_tagger(stanford_tags):
    """Use the Stanford tagger to chunk location words"""

    # Chunk words tagged as locations
    chunk_gram = r"Location: {<LOCATION>*}"
    chunk_parser = RegexpParser(chunk_gram)
    tag_tree = chunk_parser.parse(stanford_tags)

    locations = []

    # Loop the tree and extract potential locations
    for subtree in tag_tree:
        if type(subtree) is Tree and subtree.label() == "Location":
            location = [word[0] for word in subtree]
            locations.append(location)

    if not locations:
        return None

    location = choose_best_location(locations)

    return location


def choose_best_location(locations):
    unique_locations = remove_duplicates(locations)

    """Uses Bing Web Search to see if a tagged location is a real location"""

    key = "2b18d2bbb30f4a82a53845076a562986"
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"

    for location in locations:
        # Prevent exceeding request quota
        time.sleep(0.3)

        response = requests.get(
            search_url,
            headers={"Ocp-Apim-Subscription-Key": key},
            params={
                "q": " ".join(location),
                "textDecorations": True,
                "textFormat": "HTML",
                "count": 3,
            },
        )
        response.raise_for_status()
        search_results = response.json()
        x = response.headers

        search_items = search_results["webPages"]["value"]

        for item in search_items:
            if "www.cmu.edu" in item["url"]:
                return " ".join(location)

    return None


def add_tags(email, location):
    """Add tags to the email"""
    escaped_location = re.escape(location)
    pattern = rf"({escaped_location})"
    replace = r"<location>\1</location>"

    email = re.sub(pattern, replace, email, flags=re.IGNORECASE)

    return email

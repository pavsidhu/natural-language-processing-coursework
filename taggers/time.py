import re


def tag_time(email):
    """
    Tag start and end time:
        <stime>{{ start_time }}</stime>
        <etime>{{ end_time }}</etime>
    """

    pattern = r"Time:     (.+)"
    time_header = re.search(pattern, email).group()

    if time_header:
        # Get tagged time header, start time and end time
        tagged_time_header, stime, etime = tag_times_header(time_header)

        # Change the email to the tagged header
        email = re.sub(time_header, tagged_time_header, email)

        # Tag all the stimes in the abstract
        if stime:
            email = tag_abstract(stime, "stime", email)

        # Tag all the etimes in the abstract
        if etime:
            email = tag_abstract(etime, "etime", email)

    return email


def tag_times_header(header):
    """Tag the time header"""

    time_pattern = r"(\d\d?:\d\d(?: ?AM| ?PM)?)"

    start_time = None
    end_time = None

    # If header contains a start and end time it will have a hyphen
    if "-" in header:
        pattern = f"{time_pattern} - {time_pattern}"
        replace = r"<stime>\1</stime> - <etime>\2</etime>"

        # Get the start and end times
        search = re.search(pattern, header)
        start_time = search.group(1)
        end_time = search.group(2)

        # Tag the header
        header = re.sub(pattern, replace, header)
    else:
        pattern = f"{time_pattern}"
        replace = r"<stime>\1</stime>"

        # Get the start time
        search = re.search(pattern, header)
        start_time = search.group(1)

        # Tag the header
        header = re.sub(pattern, replace, header)

    return [header, start_time, end_time]


def tag_abstract(time, type, email):
    """Tags any occurances of the time in the abstract"""

    # Parse the time
    hours, minutes, suffix = parse_time(time)

    # Generate possible regex patterns
    time_patterns = generate_time_patterns(hours, minutes, suffix)

    for pattern in time_patterns:
        pattern = rf"(?<!<{type}>)({pattern})(?!</{type}>)"
        tagged_time = rf"<{type}>\1</{type}>"

        email = re.sub(pattern, tagged_time, email, flags=re.IGNORECASE)

    # Handle edge case 12-1pm -> 1pm will already be tagged, so tag the start time
    if type == "etime":
        pattern = r"(\d\d?)( ?- ?<etime>)"
        replace = r"<stime>\1</stime>\2"

        email = re.sub(pattern, replace, email, flags=re.IGNORECASE)

    return email


def parse_time(time):
    """Takes in a time and returns it in 12 hour time"""
    pattern = r"(\d\d?):(\d\d)(?: (AM)| (PM))?"
    search = re.search(pattern, time)

    hours = search.group(1)
    minutes = search.group(2)
    suffix = (
        search.group(3) or search.group(4) or "AM"
    )  # Defaults to AM if a suffix isn't provided

    return [hours, minutes, suffix]


def generate_time_patterns(hours, minutes, suffix):
    """Generates all possible formats of a time"""

    times = []

    if suffix == "AM":
        times += [rf"({hours}:{minutes}(?: ?am| ?a.m| ?a.m)?)"]

        if minutes == "00":
            times += [rf"([^\d]{hours}(?: ?am| ?a.m| ?a.m))"]

    if suffix == "PM":
        times += [rf"({hours}:{minutes}(?: ?pm| ?p.m| ?p.m.)?)"]

        if minutes == "00":
            times += [rf"((?<!\d){hours}(?: ?pm| ?p.m| ?p.m.))"]

            if hours == "12":
                times += ["noon"]

    return times

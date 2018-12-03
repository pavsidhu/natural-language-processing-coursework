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

        # Parse the start/end time and replace the times in the text
        tag_abstract(stime, etime, email)

    return email


def tag_times_header(header):
    time_pattern = r"(\d\d?):(\d\d) ?(AM|PM)?"

    start_time = None
    end_time = None

    # If header contains a start and end time it will have a hyphen
    if "-" in header:
        pattern = f"({time_pattern})"
        replace = r"<stime>\1</stime>"
        header = re.sub(pattern, replace, header)

        search = re.search(pattern, header)

        start_time = {
            "hour": search.groups(2)[0],
            "minute": search.groups(3)[0],
            "suffix": search.groups(4)[0],
        }
    else:
        pattern = f"({time_pattern}) - ({time_pattern})"
        replace = r"<stime>\1</stime> - <etime>\5</etime>"
        header = re.sub(pattern, replace, header)

        search = re.search(pattern, header)

        start_time = {
            "hour": search.groups(2)[0],
            "minute": search.groups(3)[0],
            "suffix": search.groups(4)[0],
        }

        end_time = {
            "hour": search.groups(2)[0],
            "minute": search.groups(3)[0],
            "suffix": search.groups(4)[0],
        }

    return [header, start_time, end_time]


def tag_abstract(stime, etime, text):
    """Tags any occurances of the time in the abstract"""

    if stime:
        parse_time(stime)

    if etime:
        parse_time(etime)

    return text


def parse_time(time):

    if ":" in time:
        pattern = r"(\d\d?):(\d\d)( ?pm| ?am| ?p.m| ?a.m| ?p.m.| ?a.m)?"
        result = re.search(pattern, time, flags=re.IGNORECASE)
        # print(time, result.groups(1))
    else:
        pattern = r"[^\d](\d)( ?pm| ?am| ?p.m| ?a.m| ?p.m.| ?a.m)"
        result = re.search(pattern, time, flags=re.IGNORECASE)
        # print(time, result.groups())

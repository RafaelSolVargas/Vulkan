import re


def format_time(duration):
    if not duration:
        return "00:00"

    hours = duration // 60 // 60
    minutes = duration // 60 % 60
    seconds = duration % 60

    return "{}{}{:02d}:{:02d}".format(
        hours if hours else "",
        ":" if hours else "",
        minutes,
        seconds
    )


def is_url(string) -> bool:
    """Verify if a string is a url"""
    regex = re.compile(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    if re.search(regex, string):
        return True
    else:
        return False

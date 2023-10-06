import re
from elastic_breaking_changes.rules import rules

def remove_spaces(string):
    return ''.join(c for c in string if not c.isspace())

def check_for_broken_feature(query_string, reg, text):
    regex = re.compile(reg)
    match = regex.search(query_string)
    if match is not None:
        return text

def detect_breaking_changes(query):
    flat_query = remove_spaces(query)

    for key, value in rules.items():
        reg = key
        description = value
        breaking_change = check_for_broken_feature(flat_query, reg, description)
        if breaking_change:
            print(breaking_change + "==============================")
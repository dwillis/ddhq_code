import re
import csv

results = []

# Define your list of committees as dictionaries with name and id attributes
committees = [
    {"name": "Committee A", "id": 1},
    {"name": "Committee B", "id": 2},
    {"name": "Political Action Committee", "id": 3},
    {"name": "Super PAC", "id": 4},
    {"name": "Election Fund", "id": 5},
]

# Create a regular expression pattern using the committee names
pattern = r"PAID\s+FOR\s+BY\s+(?P<committee_name>{})(?![\w-])".format("|".join(map(lambda x: re.escape(x["name"]), committees)))

# Sample email collection
email_collection = [
    "Subject: Important Election Update\nPaid for By Committee A\n...",
    "Subject: Campaign Newsletter\nPaid for By Super PAC\n...",
    # Add more emails here
]

# Loop through emails and extract disclaimers along with committee IDs
for email in email_collection:
    disclaimer_match = re.search(pattern, email)
    if disclaimer_match:
        disclaimer_text = disclaimer_match.group(0)
        committee_name = disclaimer_match.group('committee_name')
        committee_id = next((committee["id"] for committee in committees if committee["name"] == committee_name), None)
        print("Disclaimer:", disclaimer_text)
        print("Committee ID:", committee_id)

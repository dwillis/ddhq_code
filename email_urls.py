from emailnetwork.extract import *
from datetime import datetime
from email.utils import getaddresses
from mailbox import mbox
import html2text
import csv

from mailbox import mboxMessage

from emailnetwork.utils import clean_subject, clean_body
from emailnetwork.emails import EmailAddress, EmailMeta, EmailBody
from emailnetwork.summary import DomainSummary
from emailnetwork.extract import extract_body, extract_meta

from emailnetwork.header import HeaderCounter

from urlextract import URLExtract
extractor = URLExtract()

reader = MBoxReader("/Volumes/LaCie2/ddhq/Takeout/Mail/All mail Including Spam and Trash.mbox")

textmaker = html2text.HTML2Text()
textmaker.ignore_links = True

urls = []

for email in reader.mbox:
    meta = extract_meta(email)
    print(meta.subject)
    try:
        body = extract_body(email)
    except:
        continue
    try:
        if extractor.has_urls(body.body):
            for url in extractor.find_urls(body.body):
                if meta.date:
                    urls.append([meta.origin_domain, meta.sender.name, meta.date, url])
                else:
                    urls.append([meta.origin_domain, meta.sender.name, None, url])
        else:
            continue
    except:
        continue

with open("email_urls.csv", "w") as urls_file:
    writer = csv.writer(urls_file)
    writer.writerow(['domain','sender', 'date','url'])
    for row in urls:
        writer.writerow(row)

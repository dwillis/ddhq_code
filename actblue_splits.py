import csv
import json
import requests
from requests_html import HTMLSession
import time
from bs4 import BeautifulSoup

actblue_splits = []

errors = []

session = HTMLSession()

with open("actblue_urls_recent.csv", "r") as actblue_file:
    reader = csv.DictReader(actblue_file)
    for row in reader:
        dict = {}
        cols = []
        try:
            time.sleep(0.5)
#            print(row['url'])
            r = session.get(row['url'])
            r.html.render()
            js = r.html.text.split('window.preloadedState = ')[1]
            j = js.split("\n")[0].replace("undefined", "0")
            ab_json = json.loads(j)
            recipients = len(ab_json['entities'])
            if "split evenly" in r.html.text:
                percentage = 50
            else:
                percentage = None
            if recipients > 1:
                print(row['url'])
                for count, recip in enumerate(ab_json['entities']):
                    name_key = f"candidate_{count+1}"
                    dict[name_key] = recip['display_name']
                    pct_key = f"candidate_{count+1}_percent"
                    dict[pct_key] = percentage
                    cols.append(dict[name_key])
                    cols.append(dict[pct_key])
                actblue_splits.append([row['url'], recipients] + cols)
        except:
            errors.append(row['url'])
            continue

with open("actblue_splits.csv", "w") as splits_file:
    writer = csv.writer(splits_file)
    writer.writerow(['url', 'candidates', 'candidate_1_name', 'candidate_1_percent','candidate_2_name', 'candidate_2_percent', 'candidate_3_name', 'candidate_3_percent', 'candidate_4_name', 'candidate_4_percent', 'candidate_5_name', 'candidate_5_percent'])
    writer.writerows(actblue_splits)

with open("actblue_errors.csv", "w") as errors_file:
    writer = csv.writer(errors_file)
    writer.writerow(['url'])
    writer.writerows(errors)

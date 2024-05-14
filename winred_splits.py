import csv
import requests
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

ua = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/69.0.3497.100 Safari/537.36"
)


winred_splits = []

with open("winred_urls.csv", "r") as winred_file:
    reader = csv.DictReader(winred_file)
    for row in reader:
        try:
            time.sleep(0.5)
            print(row['url'])
            candidates = 0
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page(user_agent=ua)
                page.goto(row['url'])
                page.wait_for_timeout(1000)
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                if soup.find('input', id="candidate1-amount"):
                    candidates = 1
                    candidate_1_name = soup.find('input', id="candidate1-amount").next.next['value']
                    candidate_1_percent = soup.find('input', id="candidate1-amount")['data-default-percentage']
                    to_add = [row['url'], candidate_1_name, candidate_1_percent]
                if soup.find('input', id="candidate2-amount"):
                    candidates = 2
                    candidate_2_name = soup.find('input', id="candidate2-amount").next.next['value']
                    candidate_2_percent = soup.find('input', id="candidate2-amount")['data-default-percentage']
                    to_add.extend([candidate_2_name, candidate_2_percent])
                if soup.find('input', id="candidate3-amount"):
                    candidates = 3
                    candidate_3_name = soup.find('input', id="candidate3-amount").next.next['value']
                    candidate_3_percent = soup.find('input', id="candidate3-amount")['data-default-percentage']
                    to_add.extend([candidate_3_name, candidate_3_percent])
                if soup.find('input', id="candidate4-amount"):
                    candidates = 4
                    candidate_4_name = soup.find('input', id="candidate4-amount").next.next['value']
                    candidate_4_percent = soup.find('input', id="candidate4-amount")['data-default-percentage']
                    to_add.extend([candidate_4_name, candidate_4_percent])
                if soup.find('input', id="candidate5-amount"):
                    candidates = 5
                    candidate_5_name = soup.find('input', id="candidate5-amount").next.next['value']
                    candidate_5_percent = soup.find('input', id="candidate5-amount")['data-default-percentage']
                    to_add.extend([candidate_5_name, candidate_5_percent])
                if candidates > 0:
                    to_add.insert(1, candidates)
                    winred_splits.append(to_add)
        except:
            continue

with open("winred_splits.csv", "w") as splits_file:
    writer = csv.writer(splits_file)
    writer.writerow(['url', 'candidates', 'candidate_1_name', 'candidate_1_percent','candidate_2_name', 'candidate_2_percent', 'candidate_3_name', 'candidate_3_percent', 'candidate_4_name', 'candidate_4_percent', 'candidate_5_name', 'candidate_5_percent'])
    writer.writerows(winred_splits)

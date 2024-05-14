import requests
from bs4 import BeautifulSoup
import json
import csv

def extract_survey_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'DNT': '1',  # Do Not Track Request Header
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'TE': 'Trailers'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    additional_fields = soup.find_all('div', class_='additional-field')

    results = []
    for field in additional_fields:
        question_tag = field.find('p')
        if not question_tag:
            continue

        question = question_tag.get_text(strip=True)
        answers_tags = field.find_all('label')

        answers = [answer_tag.get_text(strip=True) for answer_tag in answers_tags]

        if not answers:
            answers = []

        results.append({
            'url': url,
            'question': question,
            'answers': answers
        })

    return results

def save_to_json(data, filename='winred_questions.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def process_urls_from_csv(csv_filename):
    all_survey_data = []

    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['url'].strip()  # Replace 'url' with the actual name of your column header
            try:
                survey_data = extract_survey_info(url)
                all_survey_data.extend(survey_data)
            except requests.exceptions.HTTPError as e:
                print(f"HTTP Error while processing {url}: {e}")
            except requests.exceptions.RequestException as e:
                print(f"Error while processing {url}: {e}")

    save_to_json(all_survey_data)

# Example usage:
# Make sure your CSV file contains a 'url' header or update the header name accordingly.
csv_filename = 'winred_urls.csv'
process_urls_from_csv(csv_filename)

print(f"All survey data has been saved to 'winred_questions.json'")

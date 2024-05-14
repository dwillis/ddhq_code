import csv
from bs4 import BeautifulSoup
import requests

results = []

url = "https://ent.sos.ks.gov/kssos_ent.html"
r = requests.get(url)
soup = BeautifulSoup(r.text, features="html.parser")

counties = soup.find('map', id="Map1").find_all('area')
for county in counties:
    result = {}
    result['name'] = county['alt']
    county_table = BeautifulSoup(county['title'], features="html.parser")
    result['precincts'] = county_table.find_all('tr')[0].text.split('County')[1]
    position = county_table.find_all('tr')[2].find_all('td')[1].text
    result[position] = int(county_table.find_all('tr')[2].find_all('td')[2].text.replace(',',''))
    position2 = county_table.find_all('tr')[2].find_all('td')[3].text
    result[position2] = int(county_table.find_all('tr')[2].find_all('td')[4].text.replace(',',''))
    results.append(result)

with open("ks_abortion_vote.csv", "w") as output_file:
    csv_file = csv.writer(output_file)
    csv_file.writerow(['county', 'precincts', 'yes_votes', 'no_votes'])
    for result in results:
        csv_file.writerow([result['name'], result['precincts'], result['Yes'], result['No']])

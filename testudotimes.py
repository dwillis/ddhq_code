import csv
from itertools import islice
import requests
from bs4 import BeautifulSoup

urls = ['https://www.testudotimes.com/2022/10/10/23396212/grading-maryland-footballs-position-groups-after-its-loss-to-purdue','https://www.testudotimes.com/2022/9/26/23372215/grading-maryland-footballs-position-groups-after-its-seven-point-loss-at-no-4-michigan','https://www.testudotimes.com/2022/10/3/23384502/grading-maryland-footballs-position-groups-after-its-win-over-michigan-state','https://www.testudotimes.com/2022/9/19/23360398/grading-maryland-footballs-position-groups-after-its-hard-fought-win-over-smu','https://www.testudotimes.com/2022/9/5/23337251/grading-maryland-footballs-position-groups-after-its-season-opening-win-over-buffalo','https://www.testudotimes.com/2021/10/3/22706142/grading-maryland-footballs-positions-after-its-crushing-loss-to-no-5-iowa-stats-taulia-tagovailoa','https://www.testudotimes.com/2021/11/8/22767693/grading-maryland-footballs-positions-after-its-loss-to-no-22-penn-state-taulia-tagovailoa-stats','https://www.testudotimes.com/2021/9/19/22680845/grading-maryland-footballs-positions-after-its-win-over-illinois-taulia-tagovailoa-tayon-fleet-davis','https://www.testudotimes.com/2021/9/6/22658385/grading-maryland-footballs-positions-after-its-strong-win-over-west-virginia-taulia-tagovailoa','https://www.testudotimes.com/2021/10/11/22719979/grading-maryland-footballs-positions-after-its-loss-to-ohio-state-stats-recap-taulia-tagovailoa','https://www.testudotimes.com/2021/11/29/22806717/grading-maryland-footballs-positions-after-its-win-over-rutgers-taulia-tagovailoa-big-ten-conference','https://www.testudotimes.com/2021/11/22/22794722/grading-maryland-footballs-positions-after-its-loss-to-no-8-michigan-taulia-tagovailoa','https://www.testudotimes.com/2021/9/13/22669805/grading-maryland-footballs-positions-after-its-win-over-howard-taulia-tagovailoa-dontay-demus-jr','https://www.testudotimes.com/2021/11/15/22781399/grading-maryland-footballs-positions-after-its-40-21-loss-to-no-8-michigan-state-taulia-tagovailoa','https://www.testudotimes.com/2021/10/25/22743201/grading-maryland-footballs-positions-after-its-road-loss-to-minnesota-stats-taulia-tagovailoa','https://www.testudotimes.com/2021/9/27/22694644/grading-maryland-footballs-positions-after-its-win-over-kent-state-stats-taulia-tagovailoa','https://www.testudotimes.com/2021/11/1/22755841/grading-maryland-footballs-positions-after-its-tight-win-over-indiana-taulia-tagovailoa']

grades = []

for url in urls:
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    strong_tags = soup.select("strong")[1:]
    it = iter(strong_tags)
    pairs = list(iter(lambda: tuple(islice(it, 2)), ()))
    for pair in pairs:
        print(pair)
        grades.append([url, soup.time['datetime'], pair[0].text, pair[1].text.split(": ")[1]])


with open("testudotimes_grades.csv", "w") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['url', 'datetime', 'position', 'grade'])
    writer.writerows(grades)

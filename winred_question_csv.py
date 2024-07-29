import json
import csv

# Read JSON data from file
with open('winred_questions.json', 'r') as json_file:
    data = json.load(json_file)

# Define the CSV file name
csv_file = 'winred_questions.csv'

# Write data to CSV file
with open(csv_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['url', 'question'])
    
    for item in data:
        csv_writer.writerow([item['url'], item['question']])

print(f'Data has been written to {csv_file}')

import json
import time
from sqlite_utils import *
from groq import Groq

client = Groq(api_key='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')
db = Database('emails.db')

entities = []

for email in db['emails'].rows_where("year = 2024 and month = 5"):
    time.sleep(1)
    print(email['subject'])

    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "Produce a JSON object with the following keys: names, places, organizations and products, each of which is an array, plus committee, which is the name of the committee in the disclaimer that begins with Paid for by without the treasurer name. Only include full names of individuals."
                },
                {
                    "role": "user",
                    "content": email['body']
                }
            ],
            temperature=1,
            max_tokens=4030,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )

        response = json.loads(completion.choices[0].message.content)
        obj = response | email
        entities.append(obj)
    except:
        continue

with open("email_entities/may_2024.json", 'w') as file:
    json.dump(entities, file, indent=4)

#This Python script is licensed under the MIT License.

#Copyright (c) 2023 Semantic Science

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import re
import csv
import os

csv_filename = 'log_intent_results.csv' #resulting file

fieldnames = ['transcription','intent']

with open(csv_filename, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='|')
    writer.writeheader()

# Open the JSON file
with open('report.json', 'r') as f: #dialogflow log file from Logs Explorer
    # Load the contents of the file as a JSON object
    data = json.load(f)

# Iterate over the elements in the JSON array
for element in data:
    # Do something with each element
    for key, value in element.items():

        if key == 'textPayload' and 'Dialogflow Response' in value:
            log_intent = 'NOT FOUND'
            log_transcription = 'NOT FOUND'
            transcription = re.search(r'resolved_query:\s*"([^"]+)"', value)

            if transcription:
                log_transcription = transcription.group(1)
                print(log_transcription)
            else:
                print("No match found")

            intent = re.search(r'intent_name:\s*"([^"]+)"', value)

            if intent:
                log_intent = intent.group(1)
                print(log_intent)
            else:
                print("No match found")

            data = {'transcription': log_transcription, 'intent': log_intent}

            with open(csv_filename, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='|')
                writer.writerow(data)

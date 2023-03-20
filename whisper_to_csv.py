#This Python script is licensed under the MIT License.

#Copyright (c) 2023 Semantic Science

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import whisper
import csv
import os
import datetime

# Define the directory path where .wav files are located
directory_path = '.' #set directory location with audio files

model = whisper.load_model('medium', 'cpu')

csv_filename = 'outputresult.csv'

fieldnames = ['date','filename','transcription','duration']

with open(csv_filename, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='|')
    writer.writeheader()

# Iterate over the files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.WAV'): # check if the file is a .wav file
        result = model.transcribe(filename)
        print(filename, result["text"])
        data = {'date': datetime.datetime.now(), 'filename': filename, 'transcription': result["text"]}

        with open(csv_filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='|')
            writer.writerow(data)
            #remove the file
            print("Delete: " + filename)
            os.remove(filename)


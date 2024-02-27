#This Python script is licensed under the MIT License.
#Copyright (c) 2023 Semantic Science
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import whisper
import csv
import os
import datetime
import pandas as pd

# Define the directory path where .wav files are located
directory_path = '.' #set directory location with audio files

DEVICE = 'cuda'

model = whisper.load_model('tiny.en', device = DEVICE)

# Load your CSV file
csv_file_path = 'output.csv'  # Update this to the path of your CSV file
df = pd.read_csv(csv_file_path)

# Initialize the "Zorro" column with empty strings
df['Zorro'] = ""

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Call the transcribe function with the WAV file name
    #transcription = transcribe(row['WAV File Name'])

    filename = os.path.join(directory_path, row['WAV File Name'])
    print("working on: " + filename)
    try:
        result = model.transcribe(filename)
    except:
        result["text"] = "FILE ERROR"

    # Store the transcription in the "Zorro" column
    print("result: " + result["text"])
    df.at[index, 'Zorro'] = result["text"]

# Save the modified DataFrame back to a CSV file
# This implementation is able to consume the results from Avaya AEP Transcriptions results csv and update it with whisper results as a separate column
output_csv_file_path = 'modified_file.csv'  # Update this to your desired output file path
df.to_csv(output_csv_file_path, index=False)

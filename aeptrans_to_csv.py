#This Python script is licensed under the MIT License.

#Copyright (c) 2023 Semantic Science

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import csv
import os
import xml.etree.ElementTree as ET
import lxml

import xml.etree.ElementTree as ET

def extract_wav_file_name(url):
    """Extracts WAV file name from URL."""
    if url and url.endswith('.wav'):
        return os.path.basename(url)
    return None

def parse_xml_file(xml_file):
    """Parses the XML file to extract required information."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Initialize a list to hold (transcription, wav_file_name) tuples
    results = []

    # Iterate over each 'Speech' tag instead of directly looking for 'RecResult'
    for speech in root.findall('.//SpeechFail'):
        # Find the 'RecResult' within the current 'Speech'
        rec_result = speech.find('./RecResult')
        transcription = rec_result.text.strip() if rec_result is not None and rec_result.text else None

        # Find the 'URL' within the current 'Speech'
        url_tag = speech.find('./URL')
        wav_file_name = extract_wav_file_name(url_tag.text) if url_tag is not None else None

        if transcription and wav_file_name:
            results.append((transcription, wav_file_name))

    return results

def process_xml_files(directory, csv_file_name):
    """Processes all XML files in the directory and writes to a CSV file."""
    # Check if the file already exists to determine whether to add the header
    file_exists = os.path.isfile(csv_file_name)
    
    with open(csv_file_name, mode='a+', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Only write the header if the file did not exist
        if not file_exists:
            writer.writerow(["XML File Name", "WAV File Name", "Transcription"])

        for filename in os.listdir(directory):
            if filename.endswith('.xml'):
                xml_file_path = os.path.join(directory, filename)
                print("File: " + xml_file_path)
                results = parse_xml_file(xml_file_path)

                for transcription, wav_file_name in results:
                    print("Writing: " + filename, wav_file_name, transcription)
                    writer.writerow([filename, wav_file_name, transcription])

# This script takes Avaya AEP transcription and attempts to extract utterances and transcriptions into csv
directory_path = '.'  # Replace with the path to your XML files
csv_file_name = 'output.csv'
process_xml_files(directory_path, csv_file_name)


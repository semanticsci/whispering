#This Python script is licensed under the MIT License.

#Copyright (c) 2023 Semantic Science

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


#This is a utility script that allows to extract intents automatically out of the
#transcriptions using BERTTopics

#Installation
# pip install bertopic
# pip install bertopic[visualization]
# pip install bertopic[flair]
# pip install bertopic[gensim]
# pip install bertopic[spacy]
# pip install bertopic[use]



#import packages

import pandas as pd 
import numpy as np
from bertopic import BERTopic

#load data 
import pandas as pd 

from sklearn.feature_extraction.text import CountVectorizer

import csv
import os
import datetime

df = pd.read_csv("intents_medicare_short.csv", delimiter='|')
 
# we add this to remove stopwords
vectorizer_model = CountVectorizer(ngram_range=(1, 3), stop_words="english")

# create model

model = BERTopic(
    vectorizer_model=vectorizer_model,
    language='english', calculate_probabilities=True,
    verbose=True
)

#convert to list
docs = df.transcription.to_list()

topics, probabilities = model.fit_transform(docs)

#print(model.get_topic_freq().head(50))
#print(model.get_topic(0))


freq = model.get_topic_info()
print(freq.head(50))

topic_iter = 0

#create text file per topics
while topic_iter < 36:
    topic_id = topic_iter  # Choose the topic you want to explore

    csv_filename = freq.Name[topic_iter+1] + ".csv"

    print("Creating: ", csv_filename)

    fieldnames = ['transcription','info']

    with open(csv_filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()

    topic_sentences = []

    for i, t in enumerate(topics):
        if t == topic_id:
            topic_sentences.append(df.iloc[i]['transcription'])

    for s in topic_sentences:
        data = {'transcription': s, 'info': ""}
        with open(csv_filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='|')
            writer.writerow(data)

    topic_iter += 1

    print("Done. Going to next file")


#model.visualize_topics()

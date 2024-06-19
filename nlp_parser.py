import json

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

response = SentimentIntensityAnalyzer()

with open('sampledata.json', 'r') as file:
    data = json.load(file)

texts = [item["text"] for item in data]

print(texts)

for t in texts:
    print(response.polarity_scores(t))
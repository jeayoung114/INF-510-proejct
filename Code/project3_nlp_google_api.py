import os
import pandas as pd
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

###https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python
print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])


###Sentiment_analysis with google api
def sentiment_analysis(text):
# Instantiates a client

    client = language.LanguageServiceClient()

    # The text to analyze

    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    # print('Text: {}'.format(text))
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
    return (sentiment.score, sentiment.magnitude)


"""
Sentiment analysis response fields
score of the sentiment ranges between -1.0 (negative) and 1.0 (positive) 
and corresponds to the overall emotional leaning of the text.
Magnitude indicates the overall strength of emotion (both positive and negative) within the given text,
between 0.0 and +inf .
"""

df=pd.read_csv("../Dataset/2_crawled_data_with_yelp.csv")

##Cleanse text
for i in range(len(df["review"])):
    text = df["review"][i]
    text = text.replace('\r', '')
    text = text.replace('\n', '')

    df["review"][i] = text

## Calculate sentiment score of the review
print("###############Sentiment score of review###############")
sentiment=[]
for i in range(len(df["name"])):
    sentiment.append(sentiment_analysis(df["review"][i]))


### Calculate sentiment score of the comments
print("###############Sentiment score of the reviews###############")
comment_sentiment_list=[]
for i in range(len(df['name'])):
    comment_sentiment_list.append(sentiment_analysis(df['comment'][i]))

print("###############Make new CSV File###############")
df['review_sentiment']=sentiment
df['comment_sentiment']=comment_sentiment_list

df.to_csv("../Dataset/3_crawled_data_with_sentiment.csv",index=0,index_label='num')


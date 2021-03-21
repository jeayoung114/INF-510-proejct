import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


###Get data from csv file
df=pd.read_csv("../Dataset/5_crawled_data_with_open_hour_revision.csv")

def imputation(df):
    ###Rating in Blog
    ###Imputation : Change 'no rating' to 0
    for i in range(len(df['rating_in_site'])):
        try:
            df['rating_in_site'][i]=float(df['rating_in_site'][i])
        except:
            df['rating_in_site'][i]=0
    return df

def select_sentiment_score(df):
    ### Select Sentiment score from (Sentiment.score, Sentiment.magnitude)
    for i in range(len(df['review_sentiment'])):
        a=df['review_sentiment'][i].find(',')
        df['review_sentiment'][i]=float(df['review_sentiment'][i][1:a])

    for i in range(len(df['comment_sentiment'])):
        a=df['comment_sentiment'][i].find(',')
        df['comment_sentiment'][i]=float(df['comment_sentiment'][i][1:a])
    return df


def dataframe_for_scatter_plot_matrix(df):
    ###Create a dataframe for scatter matrix plot
    df_scatter=pd.DataFrame({'blog_score': list(df['rating_in_site']),
                         'Yelp_score': list(df['rating']),
                   'review_score': list(df['review_sentiment']),
                   'comment_score': list(df['comment_sentiment'])})
    return df_scatter

df=imputation(df)
df=select_sentiment_score(df)
df_scatter=dataframe_for_scatter_plot_matrix(df)


###plot and save
pd.plotting.scatter_matrix(df_scatter)
plt.savefig("../Result/Scatter_plot_matrix.png")





# regression plot using seaborn
fig = plt.figure(figsize=(10, 7))
sns.regplot(x=df['review_count'], y=df['rating'], color='blue', marker='+')

# Legend, title and labels.
plt.title('Relationship between the number of comments and Rating', size=24)
plt.xlabel('The number of comments', size=18)
plt.ylabel('Rating', size=18)

###Save the plot
plt.savefig("../Result/Regression_plot_between_Reviewcount_and_Rating.png")
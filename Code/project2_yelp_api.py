from yelpapi import YelpAPI
import requests
import pandas as pd

df=pd.read_csv("../Dataset/1_crawled_data.csv")
business_id_list=[]
review_count_list=[]
rating_list=[]
open_hour_list=[]
comment_list=[]


###Account_Info
api_key='NRW4lhT6TdYSpTXi5YbwSgMdgt_YlbPIJthLFM6iL1jc-Y50HyHtv_IPVg4oDw_WWlDNN4h7JzzZwfcFQykneec_AzqmrV1dHaTOY6bJrouZIpoPbCLuPpBDk6CaXnYx'
url = "https://api.yelp.com/v3//businesses/{id}/reviews"
yelp_id='X1L0AXqPtWg9UUmFYSw-VQ'
yelp_api = YelpAPI(api_key)

###Search Restaurants
for i in range(len(df['name'])):

    search_results = yelp_api.search_query(term=df['name'][i], location='Los Angeles, CA')

    business_id = search_results['businesses'][0]['id']
    business_id_list.append(business_id)

    review_count = search_results['businesses'][0]['review_count']
    review_count_list.append(review_count)

    rating = search_results['businesses'][0]['rating']
    rating_list.append(rating)

    url = 'https://api.yelp.com/v3/businesses/' + business_id

    headers = {
        'Authorization': 'Bearer %s' % api_key
    }

    # Run parameters through response and save json as data
    response = requests.get(url, headers=headers)
    data = response.json()

    try:
        open_hour = data['hours'][0]['open']
        open_hour_list.append(open_hour)
    except:
        open_hour_list.append("Not open")

print("###############The number of comments###############")
print(review_count_list)
print("###############Rating in Yelp###############")
print(rating_list)

###Change Open Hour Format
def change(open_hour_list):
    if open_hour_list[i][j]['day']==0:
            open_hour_list[i][j]='On Monday open : {} close {} open overnight : {}'.format(open_hour_list[i][j]['start'],open_hour_list[i][j]['end'],open_hour_list[i][j]['is_overnight'])
    elif open_hour_list[i][j]['day']==1:
        open_hour_list[i][j]='On Tuesday open : {} close {} open overnight : {}'.format(open_hour_list[i][j]['start'],open_hour_list[i][j]['end'],open_hour_list[i][j]['is_overnight'])
    elif open_hour_list[i][j]['day']==2:
        open_hour_list[i][j]='On Wednesday open : {} close {} open overnight : {}'.format(open_hour_list[i][j]['start'],open_hour_list[i][j]['end'],open_hour_list[i][j]['is_overnight'])
    elif open_hour_list[i][j]['day']==3:
        open_hour_list[i][j]='On Thursday open : {} close {} open overnight : {}'.format(open_hour_list[i][j]['start'],open_hour_list[i][j]['end'],open_hour_list[i][j]['is_overnight'])
    elif open_hour_list[i][j]['day']==4:
        open_hour_list[i][j]='On Friday open : {} close {} open overnight : {}'.format(open_hour_list[i][j]['start'],open_hour_list[i][j]['end'],open_hour_list[i][j]['is_overnight'])
    elif open_hour_list[i][j]['day']==5:
        open_hour_list[i][j]='On Saturday open : {} close {} open overnight : {}'.format(open_hour_list[i][j]['start'],open_hour_list[i][j]['end'],open_hour_list[i][j]['is_overnight'])
    elif open_hour_list[i][j]['day']==6:
        open_hour_list[i][j]='On Sunday open : {} close {} open overnight : {}'.format(open_hour_list[i][j]['start'],open_hour_list[i][j]['end'],open_hour_list[i][j]['is_overnight'])
    return open_hour_list

for i in range(len(open_hour_list)):
    for j in range(len(open_hour_list[i])):
        try:
            change(open_hour_list)
        except:
            continue

        comment_list = []
print("###############Open_Hour_List###############")
print(open_hour_list)

### Get 3 comments of the restaurant
def comment(business_id):
    headers = {
        'Authorization': 'Bearer %s' % api_key
    }
    url = "https://api.yelp.com/v3/businesses/" + business_id + "/reviews"
    response = requests.get(url, headers=headers)
    data = response.json()

    review = []
    for i in range(3):
        review.append(data['reviews'][i]['text'])
    return review
for i in business_id_list:
    try:
        comment_list.append(comment(i))
    except:
        comment_list.append("No review")
print("###############Getting Comments###############")
print(comment_list)

###Make new CSV file
print("###############Make new CSV File###############")
df['business_id']=business_id_list
df['review_count']=review_count_list
df['rating']=rating_list
df['open_hour']=open_hour_list
df['comment']=comment_list

df.to_csv("../Dataset/2_crawled_data_with_yelp.csv",index=0,index_label='num')
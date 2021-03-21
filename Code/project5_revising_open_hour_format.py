######Most of this code is duplication of project2_yelp_api.py
######In project2_yelp_api.py, open_hour is stored in not appropriate form to display on the map
######Therefore, I changed the format as below
###### df['Monday']=1000-1800
###### or if the open hour is separated,
###### df['Monday']=1000-1500,1700-2300

from yelpapi import YelpAPI
import requests
import pandas as pd

df=pd.read_csv("../Dataset/4_crawled_data_with_geo_data.csv")

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
monday = [[] for i in range(len(df['name']))]
tuesday = [[] for i in range(len(df['name']))]
wednesday = [[] for i in range(len(df['name']))]
thursday = [[] for i in range(len(df['name']))]
friday = [[] for i in range(len(df['name']))]
saturday = [[] for i in range(len(df['name']))]
sunday = [[] for i in range(len(df['name']))]


def change(open_hour_list):
    ### Monday
    if open_hour_list[i][j]['day'] == 0:
        monday[i].append(str(open_hour_list[i][j]['start']) + '-' + str(open_hour_list[i][j]['end']))
        open_hour_list[i][j] = 'On Monday open : {} close {} open overnight : {}'.format(open_hour_list[i][j]['start'],
                                                                                         open_hour_list[i][j]['end'],
                                                                                         open_hour_list[i][j][
                                                                                             'is_overnight'])
    ###Tuesday
    elif open_hour_list[i][j]['day'] == 1:
        tuesday[i].append(str(open_hour_list[i][j]['start']) + '-' + str(open_hour_list[i][j]['end']))
        open_hour_list[i][j] = 'On Tuesday open : {} close {} open overnight : {}'.format(open_hour_list[i][j]['start'],
                                                                                          open_hour_list[i][j]['end'],
                                                                                          open_hour_list[i][j][
                                                                                              'is_overnight'])
    ###Wednesday
    elif open_hour_list[i][j]['day'] == 2:
        wednesday[i].append(str(open_hour_list[i][j]['start']) + '-' + str(open_hour_list[i][j]['end']))
        open_hour_list[i][j] = 'On Wednesday open : {} close {} open overnight : {}'.format(
            open_hour_list[i][j]['start'], open_hour_list[i][j]['end'], open_hour_list[i][j]['is_overnight'])

    ###Thursday
    elif open_hour_list[i][j]['day'] == 3:
        thursday[i].append(str(open_hour_list[i][j]['start']) + '-' + str(open_hour_list[i][j]['end']))
        open_hour_list[i][j] = 'On Thursday open : {} close {} open overnight : {}'.format(
            open_hour_list[i][j]['start'], open_hour_list[i][j]['end'], open_hour_list[i][j]['is_overnight'])

    ###Friday
    elif open_hour_list[i][j]['day'] == 4:
        friday[i].append(str(open_hour_list[i][j]['start']) + '-' + str(open_hour_list[i][j]['end']))
        open_hour_list[i][j] = 'On Friday open : {} close {} open overnight : {}'.format(open_hour_list[i][j]['start'],
                                                                                         open_hour_list[i][j]['end'],
                                                                                         open_hour_list[i][j][
                                                                                             'is_overnight'])

    ###Saturday
    elif open_hour_list[i][j]['day'] == 5:
        saturday[i].append(str(open_hour_list[i][j]['start']) + '-' + str(open_hour_list[i][j]['end']))
        open_hour_list[i][j] = 'On Saturday open : {} close {} open overnight : {}'.format(
            open_hour_list[i][j]['start'], open_hour_list[i][j]['end'], open_hour_list[i][j]['is_overnight'])

    ###Sunday
    elif open_hour_list[i][j]['day'] == 6:
        sunday[i].append(str(open_hour_list[i][j]['start']) + '-' + str(open_hour_list[i][j]['end']))
        open_hour_list[i][j] = 'On Sunday open : {} close {} open overnight : {}'.format(open_hour_list[i][j]['start'],
                                                                                         open_hour_list[i][j]['end'],
                                                                                         open_hour_list[i][j][
                                                                                             'is_overnight'])

    return open_hour_list, monday, tuesday, wednesday, thursday, friday, saturday, sunday


for i in range(len(open_hour_list)):
    for j in range(len(open_hour_list[i])):
        try:
            (open_hour_list, monday, tuesday, wednesday, thursday, friday, saturday, sunday) = change(open_hour_list)
        except:
            continue

#### if there is empty list in the list of open hour of the day, it is closed day of the restaurant
for day in monday, tuesday, wednesday, thursday, friday, saturday, sunday:
    for i in range(len(day)):
        if day[i]==[]:
            day[i].append('not open')



#### Save the crawled data into csv file
df['monday']=monday
df['tuesday']=tuesday
df['wednesday']=wednesday
df['thursday']=thursday
df['friday']=friday
df['saturday']=saturday
df['sunday']=sunday

df.to_csv("../Dataset/5_crawled_data_with_open_hour_revision.csv",index=0,index_label='num')
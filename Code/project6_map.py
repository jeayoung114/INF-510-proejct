import pandas as pd
import numpy as np
import folium
import json
from folium import plugins

###import crawled csv data
df=pd.read_csv("../Dataset/5_crawled_data_with_open_hour_revision.csv")
##Calculate average latitude and longitude of the restaurants
avg_lat=sum(df['lat'])/len(df['lat'])
avg_lng=sum(df['lng'])/len(df['lng'])

def dataframe_to_json(df):
    ###Change dataframe to Json to show it on the map
    features = [0 for i in range(len(df['name']))]
    for i in range(len(df['name'])):

        #### Feature structure of JSON
        features[i] = dict()
        features[i]['id'] = int(df.iloc[i]['num'])
        features[i]['type'] = 'Feature'

        ####Properties of JSON
        properties = dict()
        properties['Name'] = df.iloc[i]['name']
        properties['famous_for'] = df.iloc[i]['famous_for']
        properties['webpage'] = df.iloc[i]['website']
        properties['address'] = df.iloc[i]['address'][1:-1]
        #     try:
        properties['rating_in_blog'] = str(df.iloc[i]['rating_in_site'])
        #     except:
        #         properties['rating_in_blog']=df.iloc[i]['rating_in_cite']
        properties['rating_in_yelp'] = str(df.iloc[i]['rating'])
        properties['sentiment_score_review'] = df.iloc[i]['review_sentiment'][1:6]
        properties['sentiment_score_comment'] = df.iloc[i]['comment_sentiment'][1:6]
        properties['review number'] = str(df.iloc[i]['review_count'])
        properties['Open Hour'] = df.iloc[i]['open_hour']
        properties['weather'] = df.iloc[i]['weather']
        properties['temperature'] = df.iloc[i]['temperature']
        properties['Monday'] = df.iloc[i]['monday']
        properties['Tuesday'] = df.iloc[i]['tuesday']
        properties['Wednesday'] = df.iloc[i]['wednesday']
        properties['Thursday'] = df.iloc[i]['thursday']
        properties['Friday'] = df.iloc[i]['friday']
        properties['Saturday'] = df.iloc[i]['saturday']
        properties['Sunday'] = df.iloc[i]['sunday']

        properties['style'] = {'markerColor': '#00000000', 'color': '#00000000'}
        properties['highlight'] = {}

        features[i]['properties'] = properties

        features[i]['geometry'] = dict()
        features[i]['geometry']['type'] = 'Point'
        features[i]['geometry']['coordinates'] = [float(df.iloc[i]['lng']), float(df.iloc[i]['lat'])]

###Format of the json data
# data={'type' : 'FeatureCollection','type': 'Feature',
#     'features':[{
#         'id':a,
#       'properties':{},
#       'geometry':{'type': 'Point','coordinates':[lat,lng]}}]}


####Create a JSON data with features
    data = dict()
    data['type'] = 'FeatureCollection'
    data['features'] = features
    return data


def save_json(data):
    ### store the json data above in txt format
    with open('../Dataset/data.txt', 'w') as outfile:
        json.dump(data, outfile)
    return 0

### Create data of lat and lng
data_1 = np.array(
    [
       df['lat'],df['lng']
    ]
).T



###make a map which shows the information and scores of the restaurants
###make a layer of open hours
###make a layer of concentration
def build_map(data,data_1):

    ###Initialize a map centered [avg_lat, avg_lng]
    m = folium.Map([avg_lat, avg_lng], zoom_start=10)
    ### add markers to the map which shows the information of ['Name','famous_for','webpage','address','rating_in_blog','rating_in_yelp','sentiment_score_review','sentiment_score_comment','weather','temperature'].
    folium.GeoJson(data, name='Restaurants', tooltip=folium.features.GeoJsonTooltip(fields=['Name','famous_for','webpage','address','rating_in_blog','rating_in_yelp','sentiment_score_review','sentiment_score_comment','weather','temperature'], localize=True)).add_to(m)
    ### add additional layer which shows the open hour
    folium.GeoJson(data, name='Open Hours', tooltip=folium.features.GeoJsonTooltip(fields=['Name','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], localize=True)).add_to(m)
    ### add additional layer which shows the concentration of the restaurants based on cluster
    plugins.MarkerCluster(data_1, popups=list(df['name']), name='Concentration').add_to(m)###this uses data_1 as lat and lng are the only information needed to make this layer
    folium.LayerControl(collapsed=False).add_to(m)
    m.save('../Result/map_LA')

    ###Save as an html file
    m.save(outfile='../Result/map_LA.html')
    return m



data=dataframe_to_json(df)
save_json(data)
m=build_map(data,data_1)

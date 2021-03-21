import pandas as pd
import googlemaps

### write your own api key
api_key='AIzaSyC75rG-FIOK-chLkdpnmckBCuhdfcbasRA'

###import crawled csv data
df=pd.read_csv("../Dataset/3_crawled_data_with_sentiment.csv")
gmaps=googlemaps.Client(key=api_key)


###use geocoding api to get latitude and longitude of restaurants
lat = []
lng = []
for i in range(len(df["address"])):
    print(df["address"][i])
    json_var = gmaps.geocode(df["address"][i])
    lat.append(json_var[0]["geometry"]['location']['lat'])
    lng.append(json_var[0]["geometry"]['location']['lng'])


###get Weather and temperature

import requests
def get_weather(lat,lng):
    query1='https://api.weather.gov/points/'+lat+','+lng+'/forecast/hourly'
    req=requests.get(query1)
    js=req.json()
    # pretty_json1=json.dumps(js, indent=4)

    weather = js["properties"]["periods"][1]['shortForecast']
    temperature = js["properties"]["periods"][1]['temperature']

    return (weather,temperature)


weather=[]
temperature=[]
for i in range(len(lat)):
    print(get_weather(str(lat[i]),str(lng[i]))[0])
    weather.append(get_weather(str(lat[i]),str(lng[i]))[0])
    print(get_weather(str(lat[i]),str(lng[i]))[1],'F')
    temperature.append(str(get_weather(str(lat[i]),str(lng[i]))[1])+'F')

###df to csvs
print("###############Make new CSV File###############")
df['lat']=lat
df['lng']=lng
df['weather']=weather
df['temperature']=temperature
df.to_csv("../Dataset/4_crawled_data_with_geo_data.csv",index=0,index_label='num')


import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml
import urllib.request
from math import ceil
import geopandas as gpd
import matplotlib.pyplot as plt

def get_efl_info():
    
    wiki_html = requests.get("https://en.wikipedia.org/wiki/EFL_Championship").text
    soup = BeautifulSoup(wiki_html, 'lxml')
    table_html = soup.find("table",{"class":"wikitable sortable"})
    df = pd.read_html(str(table_html))[0]
    df = df[['Club', 'Stadium']]
    
    return df


def get_directions(origin, destination):
    
    endpoint = "https://maps.googleapis.com/maps/api/directions/json?"
    API_KEY = "AIzaSyBGvB6ZBzBcbDeldip506009a1YCkObp0A"
    nav_request = f"origin={origin}&destination={destination}&key={API_KEY}"
    request = endpoint + nav_request
    response = urllib.request.urlopen(request).read()
    directions = json.loads(response)
    
    return directions


def get_distance(directions):
    return directions['routes'][0]['legs'][0]['distance']['value']

def get_lat_long(directions):
    end_location = directions['routes'][0]['legs'][0]['end_location']
    latitude = end_location['lat']
    longitude = end_location['lng']
    return (latitude, longitude)


def convert_distance_m_to_km(distance):
    distance_km = ceil(distance / 1000)
    return distance_km


def replace_space_with_plus(string):
    string = string.replace(' ', '+')
    return string


def main():
    origin = "NG13AA"
    stadium_list = {}
    
    df = get_efl_info()

    for stadium, club in zip(df.Stadium, df.Club):
        print(stadium, club)
        destination = stadium + club
        destination = replace_space_with_plus(destination)
        directions = get_directions(origin, destination)
        distance = get_distance(directions)
        lat_long = get_lat_long(directions)
        stadium_list[stadium] = {
            "distance": convert_distance_m_to_km(distance),
            "latitude": lat_long[0],
            "longitude": lat_long[1],
        }

    lat_long_df = pd.DataFrame.from_dict(stadium_list).T
    df = df.merge(lat_long_df, how='inner', left_on='Stadium', right_index=True)
    return df

if __name__ == '__main__':
    df = main()
    
    uk.plot(figsize=(10,10))
    
    
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude)
    )
    
    
    
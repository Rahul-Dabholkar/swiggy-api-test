# Importing libraries
import requests
import json
import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8') #alternate to bs4

# headers
headers = {
    'authority': 'www.swiggy.com',
    '__fetch_req__': 'true',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.8',
    'content-type': 'application/json',
    # 'cookie': '__SW=IZGWvjE81SKycExV9gpRE1YkGPxLpPn8; _device_id=e9290c6c-eced-a446-bfb4-076ef3b6fee1; _is_logged_in=1; _session_tid=a4164c06f707391b8ca05f757a56d66e7ef3ce9a57e5817d482d0d81470c78281f6e6518e0e06d3e5409d21193eaa84ab836bddd63b827f51d438b1dd675ed0fa0ef29362a32c5a359c7e20c350b8fec17f2ed57f3a92d7a0d05468b88180216a59bd7f22838983b3f21c27447426bb9; fontsLoaded=1; _ot=REGULAR; userLocation={%22address%22:%226%2C%20Golibar%20Rd%2C%20Khar%2C%20Golibar%2C%20Khar%20East%2C%20Mumbai%2C%20Maharashtra%20400055%2C%20India%22%2C%22area%22:%22Khar%20East%22%2C%22id%22:%22258105474%22%2C%22lat%22:%2219.07456744509559%22%2C%22lng%22:%2272.84382541436504%22}; dadl=true; _sid=4ztc0ec8-49f0-46e6-b148-997b8dad64d6',
    'if-none-match': 'W/"5dee-BKPCIzKThBSXxbhPCOxDyL86WiA"',
    'referer': 'https://www.swiggy.com/restaurants/maniks-modern-fresh-popcorn-patel-mahal-matunga-mumbai-44397',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

# parameters set to get cheapest items in locality
params = {
    'lat': '19.07456744509559',
    'lng': '72.84382541436504',
    'menuId': '44397',
}

# getting entire menu
response = requests.get('https://www.swiggy.com/dapi/menu/v4/full', params=params, headers=headers)
response = response.text
data = json.loads(response)

# TARGET
# Restaurant details: Name, Area, Timing, Distance, Discount, Delivery Fee, Rating
name = data['data']['name']
area = data['data']['area']
locality = data['data']['locality'] # Locality is taken - area and location is different for some restaurants
timing = data['data']['sla']['deliveryTime'] # I will assume this as delivery time
distance = data['data']['sla']['lastMileDistanceString']
rating = data['data']['avgRating']
cost_for_two = data['data']['costForTwo']
restaurant_data = {'name' : name,
        'area' : area,
        'locality' : locality,
        'timing' : timing,
        'distance' : distance,
        'rating' : rating,
        'cost_for_two' : cost_for_two}

# TARGET
# Item Details: Name, Price, Rating (if available)
items = data['data']['menu']['items']
ids = []
for idtag in items:
    ids.append(idtag)

items_details = []
for i in ids:
    name = items[i]['name']
    category = items[i]['category']

    veg_or_nonveg = items[i]['isVeg']
    if veg_or_nonveg == 1:
        veg_or_nonveg = True
    veg_or_nonveg = False

    price = (items[i]['price'] / 100)
    
    # ratings are not available

    items_details.append({'name': name, 'category': category, 'veg_or_nonveg': veg_or_nonveg, 'price': price})

# final data of - restraunt details, cheap item details
complete = {'restraunt': restaurant_data,
            'menu_items': items_details}

print(complete)

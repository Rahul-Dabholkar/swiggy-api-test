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
    'if-none-match': 'W/"8cea-7Z0JmmzY7Yl/M4XmN4IGQDftuJg"',
    'referer': 'https://www.swiggy.com/?sortBy=COST_FOR_TWO',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

# parameters set to get cheapest restaurants in locality
params = {
    'lat': '19.07456744509559',
    'lng': '72.84382541436504',
    'sortBy': 'COST_FOR_TWO',
    'page_type': 'DESKTOP_WEB_LISTING',
}


response = requests.get('https://www.swiggy.com/dapi/restaurants/list/v5', params=params, headers=headers)
response = response.text
data = json.loads(response)

# getting the total pages - this can be incremented in a for loop to get more results
page = data['data']['pages']


######## For this test data I will only scrape the first instance of restaurants that appear when sorted by price. #######

marker = 0
for i in range(page):

    headers = {
    'authority': 'www.swiggy.com',
    '__fetch_req__': 'true',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.8',
    'content-type': 'application/json',
    # 'cookie': '__SW=IZGWvjE81SKycExV9gpRE1YkGPxLpPn8; _device_id=e9290c6c-eced-a446-bfb4-076ef3b6fee1; _is_logged_in=1; _session_tid=a4164c06f707391b8ca05f757a56d66e7ef3ce9a57e5817d482d0d81470c78281f6e6518e0e06d3e5409d21193eaa84ab836bddd63b827f51d438b1dd675ed0fa0ef29362a32c5a359c7e20c350b8fec17f2ed57f3a92d7a0d05468b88180216a59bd7f22838983b3f21c27447426bb9; fontsLoaded=1; _ot=REGULAR; userLocation={%22address%22:%226%2C%20Golibar%20Rd%2C%20Khar%2C%20Golibar%2C%20Khar%20East%2C%20Mumbai%2C%20Maharashtra%20400055%2C%20India%22%2C%22area%22:%22Khar%20East%22%2C%22id%22:%22258105474%22%2C%22lat%22:%2219.07456744509559%22%2C%22lng%22:%2272.84382541436504%22}; dadl=true; _sid=4ztc0ec8-49f0-46e6-b148-997b8dad64d6',
    'if-none-match': 'W/"89d9-/e1S8qw96nTIV2WqY0/rqKgLzSs"',
    'referer': 'https://www.swiggy.com/?sortBy=COST_FOR_TWO',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    params = {
        'page': marker,
        'lat': '19.07456744509559',
        'lng': '72.84382541436504',
        'sortBy': 'COST_FOR_TWO',
        'page_type': 'DESKTOP_WEB_LISTING',
    }

    response = requests.get('https://www.swiggy.com/dapi/restaurants/list/v5', params=params, headers=headers)
    response = response.text

    # print('page no : '+str(page))

    # scraping data of all restraunts
    data = json.loads(response)
    all_rest = data['data']['cards'][i]['data']['data']['cards']
    restaurants = []
    for i in range(len(all_rest)):
        name = all_rest[i]['data']['name']
        area = all_rest[i]['data']['area']
        cusines = all_rest[i]['data']['cuisines']
        delivery_time = all_rest[i]['data']['deliveryTime']
        rating = all_rest[i]['data']['avgRating']
        cost_for_two = all_rest[i]['data']['costForTwoString']

        restaurants.append([name, area, cusines, delivery_time, rating, cost_for_two])
    
    # making and extracting dataframe of restaurants list 
    restaurants = pd.DataFrame(restaurants, columns=['name','area','cusines','delivery time', 'rating', 'cost_for_two'])

    # reindexing - to start from 1
    restaurants.index = np.arange(1, len(restaurants) + 1)

    # when scraping multiple pages. this is supossed to be out of for loop
    restaurants.to_csv('cheap-restaurants.csv')
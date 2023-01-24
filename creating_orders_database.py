# Importing libraries
import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8') #alternate to bs4

# cookies
cookies = {
    '__SW': 'IZGWvjE81SKycExV9gpRE1YkGPxLpPn8',
    '_device_id': 'e9290c6c-eced-a446-bfb4-076ef3b6fee1',
    '_is_logged_in': '1',
    '_session_tid': 'a4164c06f707391b8ca05f757a56d66e7ef3ce9a57e5817d482d0d81470c78281f6e6518e0e06d3e5409d21193eaa84ab836bddd63b827f51d438b1dd675ed0fa0ef29362a32c5a359c7e20c350b8fec17f2ed57f3a92d7a0d05468b88180216a59bd7f22838983b3f21c27447426bb9',
    'fontsLoaded': '1',
    '_ot': 'REGULAR',
    'userLocation': '{%22address%22:%226%2C%20Golibar%20Rd%2C%20Khar%2C%20Golibar%2C%20Khar%20East%2C%20Mumbai%2C%20Maharashtra%20400055%2C%20India%22%2C%22area%22:%22Khar%20East%22%2C%22id%22:%22258105474%22%2C%22lat%22:%2219.07456744509559%22%2C%22lng%22:%2272.84382541436504%22}',
    'dadl': 'true',
    '_sid': '50hf8aaa-14ad-491e-b5b1-e4a5f754a82a',
}

# headers
headers = {
    'authority': 'www.swiggy.com',
    '__fetch_req__': 'true',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.6',
    'content-type': 'application/json',
    # 'cookie': '__SW=IZGWvjE81SKycExV9gpRE1YkGPxLpPn8; _device_id=e9290c6c-eced-a446-bfb4-076ef3b6fee1; _is_logged_in=1; _session_tid=a4164c06f707391b8ca05f757a56d66e7ef3ce9a57e5817d482d0d81470c78281f6e6518e0e06d3e5409d21193eaa84ab836bddd63b827f51d438b1dd675ed0fa0ef29362a32c5a359c7e20c350b8fec17f2ed57f3a92d7a0d05468b88180216a59bd7f22838983b3f21c27447426bb9; fontsLoaded=1; _ot=REGULAR; userLocation={%22address%22:%226%2C%20Golibar%20Rd%2C%20Khar%2C%20Golibar%2C%20Khar%20East%2C%20Mumbai%2C%20Maharashtra%20400055%2C%20India%22%2C%22area%22:%22Khar%20East%22%2C%22id%22:%22258105474%22%2C%22lat%22:%2219.07456744509559%22%2C%22lng%22:%2272.84382541436504%22}; dadl=true; _sid=50hf8aaa-14ad-491e-b5b1-e4a5f754a82a',
    'if-none-match': 'W/"1d019-PAjlzPWaqrPnbgGm0Hr8/N9hY5A"',
    'referer': 'https://www.swiggy.com/my-account',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

# parameters set to get all the orders
params = {
    'order_id': '',
}

# getting all the orders details
response = requests.get('https://www.swiggy.com/dapi/order/all', params=params, cookies=cookies, headers=headers)
response = response.text
data = json.loads(response)

orders = data['data']['orders']

# TARGET
# Question 2: Find out your total expense on swiggy and store the details in database.
# - total expense
# - expense in last 4 months
# - most ordered dish, most favourite restraunt, avg order value


# getting all the required information to query the database
all_orders = []
counter = 1
for order in range(len(orders)):
    order_items = orders[order]['order_items'][0]['name']
    order_items_quantity = orders[order]['order_items'][0]['quantity']

    restaurant_name = orders[order]['restaurant_name']
    restaurant_locality = orders[order]['restaurant_locality']

    order_time_str = orders[order]['order_time']
    order_date_str = order_time_str.split()                                 # we only need the date
    order_date = datetime.strptime(order_date_str[0], '%Y-%m-%d').date()    # converting it to DT format

    delivery_fee = orders[order]['order_delivery_charge']
    original_price = orders[order]['order_restaurant_bill'] # with delivery charges
    price_discount = orders[order]['order_discount']
    final_price = orders[order]['order_total'] # with delivery charges

    all_orders.append([order_items, int(order_items_quantity), \
                       restaurant_name, restaurant_locality, \
                       order_date, \
                       float(delivery_fee), float(original_price), float(price_discount), float(final_price)])

#print(all_orders)
orders_df = pd.DataFrame(all_orders, columns=['order_items','order_items_quantity','restaurant_name','restaurant_locality', 'order_date', 'delivery_fee', 'original_price', 'price_discount', 'final_price'])

# reindexing - to start from 1
orders_df.index = np.arange(1, len(orders_df) + 1)

######## CREATING A DATABASE ########
# conn = sqlite3.connect('orders.db')
# table_name = 'Orders'
# cursor = conn.cursor()
# query = f"CREATE TABLE IF NOT EXISTS {table_name}( order_items TEXT, \
#                                                    order_items_quantity INTEGER,\
#                                                    restaurant_name TEXT, \
#                                                    restaurant_locality TEXT,\
#                                                    order_date REAL, \
#                                                    delivery_fee REAL, \
#                                                    original_price REAL, \
#                                                    price_discount REAL, \
#                                                    final_price REAL)"
# cursor.execute(query)


# new short method to make database
orders_df.to_sql(name='Orders', con=conn, if_exists='replace', index=False)
conn.commit()
import sqlite3
from sqlite3 import Error

# connecting to database
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# Total Orders
def total_orders(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Orders")
    total = cur.fetchone()

    print(f'The total number of orders is {total[0]}.')

# Total expense
def total_expense(conn):
    cur = conn.cursor()
    cur.execute("SELECT SUM(final_price) FROM Orders")
    total = cur.fetchone()

    print(f'The total spent on orders is {total[0]}.')

# Total expense in last 4 months
def total_expense_4months(conn):

    cur = conn.cursor()
    cur.execute("SELECT SUM(final_price) FROM Orders WHERE date(order_date) > date('2022-09-01')")
    total = cur.fetchone()

    print(f'The total spent on orders in last 4 months is {total[0]}.')

# most ordered dish
def most_ordered_dish(conn):
    cur = conn.cursor()
    cur.execute("SELECT order_items, COUNT(order_items) FROM Orders GROUP BY order_items ORDER BY COUNT(order_items) DESC LIMIT 1")
    total = cur.fetchone()

    print(f'The most ordered dish is {total[0]} which was ordered {total[1]} times.')

# most favourite restraunt
def most_fav_rest(conn):
    cur = conn.cursor()
    cur.execute("SELECT restaurant_name, COUNT(restaurant_name) FROM Orders GROUP BY restaurant_name ORDER BY COUNT(restaurant_name) DESC LIMIT 1")
    total = cur.fetchone()

    print(f'The favourite restaurant to order from is {total[0]}.\nThere were total {total[1]} orders placed from this restaurant.')

# avg order value
def avg_order_value(conn):
    cur = conn.cursor()
    cur.execute("SELECT AVG(final_price) FROM Orders")
    total = cur.fetchone()

    print(f'The average order value is {total[0]}.')

# main function
def main():
    database = r'orders.db'
    conn = create_connection(database)
    with conn:
        total_orders(conn)
        total_expense(conn)
        total_expense_4months(conn)
        most_ordered_dish(conn)
        most_fav_rest(conn)
        avg_order_value(conn)
        
if __name__ == '__main__':
    main()
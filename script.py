# List of currency pairs to insert (you can expand this to 300)
currency_pairs = [
    ('USD/EUR', 0.85),
    ('GBP/USD', 1.38),
    ('JPY/USD', 0.009),
    ('AUD/USD', 0.75),
    ('CAD/USD', 0.80)
    # Add more pairs here...
]

# Connect to the database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Insert multiple records in one go
cursor.executemany("INSERT INTO rates (ccy_couple, rate, event_time) VALUES (?, ?, strftime('%s', 'now') * 1000)", currency_pairs)

# Commit the changes
conn.commit()

# Query to check data
cursor.execute("SELECT * FROM rates")
data = cursor.fetchall()
print("Updated rates data:")
for row in data:
    print(row)

# Close connection
conn.close()

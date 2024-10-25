from flask import Flask, render_template
import sqlite3
import requests
import time
time.sleep(1)  # pauses for 1 second


app = Flask(__name__)

# Sample list of currency couples
currency_pairs = ['USD/EUR', 'GBP/USD', 'JPY/USD']

def fetch_rates():
    rates = {}
    url = " https://v6.exchangerate-api.com/v6/5742d97041e6316906d41ccc/latest/USD"  # Replace with your API key
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for pair in currency_pairs:
            base, target = pair.split('/')
            if base in data['conversion_rates'] and target in data['conversion_rates']:
                rate = data['conversion_rates'][target] / data['conversion_rates'][base]
                rates[pair] = rate
    except requests.exceptions.RequestException as e:
        print(f"Error fetching rates: {e}")
    return rates

def store_rates(rates):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    for ccy_couple, rate in rates.items():
        cursor.execute("INSERT INTO rates (ccy_couple, rate, event_time) VALUES (?, ?, ?)",
                       (ccy_couple, rate, int(time.time() * 1000)))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    rates = fetch_rates()
    if rates:
        store_rates(rates)
    return render_template('index.html', rates=rates)

if __name__ == "__main__":
    app.run(port=5001)


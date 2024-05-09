import requests
import time
import mysql.connector
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def fetch_data():
    try:
        response = requests.get("https://4feaquhyai.execute-api.us-east-1.amazonaws.com/api/pi")
        data = response.json()
        print(data.get('factor'), data.get('pi'), data.get('time'))
        return data.get('factor'), data.get('pi'), data.get('time')
    except Exception as e:
        print("Error fetching data:", e)
        return None, None, None

def store_data(factor, pi, api_time, cursor, db):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                factor INT,
                pi_value FLOAT,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("INSERT INTO api_data (factor, pi_value, time) VALUES (%s, %s, %s)", (factor, pi, api_time))
        db.commit()
        print("Data stored successfully.")
    except Exception as e:
        print("Error storing data:", e)

def fetch_data_from_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Iswim4EST!",
            port="3306",
            database="Pi_Analysis" 
        )
        cursor = db.cursor()
        query = "SELECT factor, pi_value, time FROM api_data"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        db.close()
        return rows
    except Exception as e:
        print("Error fetching data from database:", e)
        return None

def create_dataframe(rows):
    if rows:
        df = pd.DataFrame(rows, columns=['factor', 'pi_value', 'time'])
        df['time'] = pd.to_datetime(df['time'])
        return df
    else:
        return None

def plot_data(df):
    if df is not None:
        plt.figure(figsize=(10, 6))
        plt.plot(df['time'], df['pi_value'], label='Pi')
        plt.plot(df['time'], df['factor'], label='Factor')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('Comparison of Pi and Factor over Time')
        plt.legend()
        plt.show()
    else:
        print("No data to plot.")

def main():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Iswim4EST!",
        port="3306",
        database="Pi_Analysis" 
    )
    cursor = db.cursor()
    
    current_time = datetime.now()
    target_time = current_time.replace(hour=current_time.hour + 1, minute=0, second=0, microsecond=0)
    print(current_time, target_time)

    while True:
        if datetime.now() >= target_time:
            break

    for _ in range(60):
        factor, pi, api_time = fetch_data()
        if factor is not None and pi is not None and api_time is not None:
            store_data(factor, pi, api_time, cursor, db)
        time.sleep(59.75)

    cursor.close()
    db.close()

    rows = fetch_data_from_db()
    df = create_dataframe(rows)
    plot_data(df)

if __name__ == "__main__":
    main()

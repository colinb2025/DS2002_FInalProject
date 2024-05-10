import requests
import mysql.connector
db = mysql.connector.connect(
    host="localhost"
    , user="root"
    , password="Olliem-2002"
    , database="data_project",
    port= "3306"
)
cursor = db.cursor()
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS player_data(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(45),
    score INT,
    rounds INT,
    wins INT
)
""")

# Table queries for ETL database
create_country_table_query = """
CREATE TABLE IF NOT EXISTS Country (
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    capital VARCHAR(255),  
    currencies VARCHAR(255),
    languages VARCHAR(255)
)
"""

# Create country table
try:
    cursor.execute(create_country_table_query)
except mysql.connector.Error as error:
    print("Error creating table:", error)

# Function to extract and load country data
def extract_transform_load(country):
    try:
        endpoint = f"https://restcountries.com/v3.1/name/{country}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and data[0].get("name"):
                country_data = data[0]
                full_name = country_data["name"].get("common")
                capital = ", ".join(country_data.get("capital", []))
                
                # Extract currencies
                currencies = ", ".join([f"{currency_data.get('name', '')} ({currency_code})" 
                                        for currency_code, currency_data in country_data.get("currencies", {}).items()])

                # Extract languages
                languages = ", ".join([f"{language_name} ({language_code})" 
                                       for language_code, language_name in country_data.get("languages", {}).items()])

                cursor.execute("INSERT INTO Country (name, capital, currencies, languages) VALUES (%s, %s, %s, %s)",
                               (full_name, capital, currencies, languages))
                db.commit()
                print(f"Data for {full_name} inserted successfully.")
            else:
                print(f"No valid data found for {country}")
        else:
            print(f"Failed to retrieve data for {country}. Status code: {response.status_code}")
            print(f"Please make sure that '{country}' is your desired input")
    except mysql.connector.Error as sql_error:
        print("MySQL error:", sql_error)
    except requests.RequestException as req_error:
        print("Request error:", req_error)
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to retrieve the official country name to assist with duplicates
def get_official_country_name(country):
    try:
        endpoint = f"https://restcountries.com/v3.1/name/{country}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and data[0].get("name"):
                official_name = data[0]["name"].get("common")
                return official_name
            else:
                print(f"No valid data found for {country}")
        else:
            print(f"Failed to retrieve data for {country}. Status code: {response.status_code}")
            print(f"Please make sure that '{country}' is your desired input")
    except requests.RequestException as req_error:
        print("Request error:", req_error)
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

# Iterate through every country in the API
def iterate_countries():
    try:
        endpoint = "https://restcountries.com/v3.1/all"
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            for country_data in data:
                full_name = country_data["name"].get("common")
                extract_transform_load(full_name)
        else:
            print(f"Failed to retrieve country data. Status code: {response.status_code}")
    except requests.RequestException as req_error:
        print("Request error:", req_error)
    except Exception as e:
        print(f"An error occurred: {e}")

iterate_countries()

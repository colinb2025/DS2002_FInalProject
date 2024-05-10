# DS2002 FInal Projects

# Pi Data Analysis

Pi Analysis Data Fetcher is a Python script designed to fetch data from a remote API, store it in a MySQL database, and visualize it using Pandas and Matplotlib libraries. The script fetches the value of Pi, changing minutely, and its factor from a specified API endpoint, stores it in a database, and generates a time-series plot comparing Pi values and factors over time.

## Features

- **Data Fetching**: The code makes a call to the API to gather and store data within MySQL, storing it for use throughout the rest of the project. 

- **Data Visualization**: The script utilizes Pandas and Matplotlib libraries to create a time-series plot at the end of the sixty minute window. It generates a visual representation of the data fetched from the API and stored in the database.

## Usage

To use the Pi Analysis Data Fetcher, follow these steps:

1. **Database Configuration**: Set up a MySQL database where fetched data will be stored. Update the database connection details (host, user, password, port, database) in the `project_1.py` script.

2. **Running the Script**: Execute the `project_1.py` script to start fetching data from the API. The script will continuously fetch data on a minutely basis over the course of an hour and store it in the database.

3. **Visualization**: After fetching and storing data for an hour, the script will generate a time-series plot comparing Pi values and factors over time. You can visualize this plot to analyze the trends in Pi values and factors.

## Contributing


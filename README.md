# DS2002 FInal Projects



# Pi Data Analysis (Project1)

Pi Analysis Data Fetcher is a Python script designed to fetch data from a remote API, store it in a MySQL database, and visualize it using Pandas and Matplotlib libraries. The script fetches the value of Pi, changing minutely, and its factor from a specified API endpoint, stores it in a database, and generates a time-series plot comparing Pi values and factors over time.

## Features

- **Data Fetching**: The code makes a call to the API to gather and store data within MySQL, storing it for use throughout the rest of the project. 

- **Data Visualization**: The script utilizes Pandas and Matplotlib libraries to create a time-series plot at the end of the sixty minute window. It generates a visual representation of the data fetched from the API and stored in the database.

## Usage

To use the Pi Analysis Data Fetcher, follow these steps:

1. **Database Configuration**: Set up a MySQL database where fetched data will be stored. Update the database connection details (host, user, password, port, database) in the `project_1.py` script.

2. **Running the Script**: Execute the `project_1.py` script to start fetching data from the API. The script will continuously fetch data on a minutely basis over the course of an hour and store it in the database.

3. **Visualization**: After fetching and storing data for an hour, the script will generate a time-series plot comparing Pi values and factors over time. You can visualize this plot to analyze the trends in Pi values and factors.

## Project Information and Contributors

This project was done by Colin Bitz for the class DS2002 at the University of Virginia. 



# CountryBot Discord Bot (Project2)

CountryBot is a Discord bot designed to entertain users with a geography-based game. The bot pulls data from an API and stores it in MySQL, where data can be adjusted and used as needed. This database provides users with information countries and prompting them to guess the correct country based on given hints. It also supports basic chat functionalities and provides assistance upon request.

## Features

- **Geography Game**: Users can initiate a private message with the bot to play a geography-based game. The bot provides hints about a country's capital, currency, and language, and users have to guess the correct country within three attempts.

- **Score Tracking**: The bot tracks users' scores based on the number of correct guesses and hints used during the game. It maintains a leaderboard of top scorers, calculating score by `2 * (-guesses + 4)`. 

- **Chat Interaction**: Users can interact with the bot in the main chat by typing commands like "hi", "hello", "hey" to receive greetings, and "help" to get instructions on how to play the game. Once you have initiated a private chat, there are additional commands that can be used to allow for increased functionality. 

## Usage

To use the CountryBot, follow these steps:

1. **Setup**: If you would like to have a local version of the code, clone the repository and install the required dependencies using `pip install -r requirements.txt` if libraries are not installed.

2. **Database Configuration**: You need to set up a MySQL database for storing country and player data. Update the database connection details in the `get_country_data`, `submit_player`, and `leaderboard` functions in `bot.py` as well as in `Databases.py`. In these three instances, you will need to change the password to your MySQL password. 

3. **Discord Token**: Create a `.env` file in the project directory and add our Discord bot token, provided here: `DISCORD_TOKEN=<provided_token>`.

4. **Running the Bot**: We have integrated everything including database work, API connection, and chat functions into `bot.py`. Simply running `bot.py` will run the bot. It will connect to Discord using the provided token and be ready to respond to messages and game requests.

5. **Interacting with the Bot**: Users can interact with the bot in the main chat by typing commands like "hi", "hello", "hey" to receive greetings. To learn more, users should follows prompt until eventually given a private chat where they will given further instruction on how to play the game. This decision was made with a user-friendly design in mind, ensuring that the main channel would not be clogged by many users.

## Project Information and Contributors

This project was done by Oliver Mills and Colin Bitz for the class DS2002 at the University of Virginia. 

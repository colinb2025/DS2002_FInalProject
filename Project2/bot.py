# Import necessary modules
from typing import Final
import os

import mysql.connector
from dotenv import load_dotenv
from discord import Intents, Client, Message
from Response import get_response
from random import choice, randint, random

# database info in get country data and player related functions

# Step 0: load our token from somewhere safe
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# print (TOKEN)

# Step 1: BOT SETUP Without intents your bot won't respond
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

# Define global variable to track game in progress
game_in_progress = False

# mysql database connection information
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Olliem-2002",
    port="3306",
    database="data_project"
)
cursor = db.cursor()


# Step 2: Message Function
async def send_message(message: Message, user_message: str) -> None:
    global game_in_progress
    user_input = ""
    if not user_message:
        print('(Message was empty because intents were not enabled...prob)')
        return

    # Check for special keyword 'game' to initiate private message
    if "game" in user_message.lower() and not game_in_progress:
        game_in_progress = True
        await message.author.send("**Welcome!** \n"
                                  "We\'ll play our game here to not clog up the main chat \n"
                                  "I will give you a country capital, currency, or/or language \n"
                                  "You will have to give me the correct country to receive credit \n"
                                  "You only have three lives so plan your rounds accordingly"
                                  "\n"
                                  "You will be scored by how many guesses and hints you use for each round.\n"
                                  "Please tell me a number of rounds you would like to play by typing "
                                  "**\'rounds\'**\n"
                                  "After that, type **\'start\'** to begin the game \n"
                                  "Typing **\'leaderboard\'** will show you the top 5 scores\n"
                                  "Typing **\'exit\'** will end the game\n"
                                  "\n"
                                  "Commands overview: \n"
                                  "**Rounds:** How many rounds you want to play\n"
                                  "**Start:** Starts the game\n"
                                  "**Leaderboard:** Shows the top 5 scores\n"
                                  "**Exit**: Ends the game")

        while user_input != "exit":
            user_input = await client.wait_for('message', check=lambda m: m.author == message.author)
            if user_input.content.lower() == "rounds":
                # Wait for the next message containing the round count
                await message.author.send("Please enter the number of **\'Rounds\'** you would like to play")
                round_count_message = await client.wait_for('message', check=lambda m: m.author == message.author)
                while round_count_message.content.lower() != "exit":
                    try:
                        rounds = int(round_count_message.content)
                        await message.author.send(f"You chose to play {rounds} rounds.")

                        # Wait for the player to say "start" to begin the game
                        await message.author.send("Type **'start'** to begin the game.")
                        start_message = await client.wait_for('message', check=lambda m: m.author == message.author)
                        while start_message.content.lower() != "exit":
                            if start_message.content.lower() == "start":
                                # Start game with specified number of rounds
                                await start_game(message.author, rounds)  # Assuming you have a start_game function
                                start_message.content = "exit"
                                game_in_progress = False
                                return
                            else:
                                await message.author.send("Invalid input. Please type 'start' to begin the game.")
                                start_message = await client.wait_for('message',
                                                                      check=lambda m: m.author == message.author)
                        await message.author.send("Goodbye")
                        game_in_progress = False
                        return
                    except ValueError:
                        await message.author.send("Invalid input. Please enter a valid number for rounds.")
                        round_count_message = await client.wait_for('message',
                                                                    check=lambda m: m.author == message.author)

                await message.author.send("Goodbye")
                game_in_progress = False
                return
            elif user_input.content.lower() == "leaderboard":
                top5 = await leaderboard()
                place = 1
                for row in top5:
                    user = row[1]
                    score = row[2]
                    wins = row[4]
                    rounds = row[3]
                    await message.author.send(f"{place}: **{user}**: **{score}**(**{wins}/{rounds}**)")
                    place += 1
            elif user_input.content.lower() == "exit":
                game_in_progress = False
                await message.author.send("Goodbye")
                break
            else:
                await message.author.send("Invalid input. Please enter one of the following: \n"
                                          "**Rounds:** How many rounds you want to play\n"
                                          "**Leaderboard:** Shows the top 5 scores\n"
                                          "**Exit**: ends the game")

    # check to see if you need to respond to private messages
    if is_private := user_message.startswith('?'):
        user_message = user_message[1:]

    try:
        response: str = await get_response(user_message)  # This function is now asynchronous
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


async def start_game(player, rounds):
    global game_in_progress
    score = 0
    wins = 0
    lives = 3
    for round_number in range(1, rounds + 1):
        country_name, capital, currency, languages = await get_country_data()
        guess = 1
        while guess <= 3:
            await player.send(f"Round : {round_number} Guess: {guess} Lives left: {lives}")
            won = False
            if guess == 1:
                await player.send(f"The offical languages for this country are {languages} ")
                user_input = await client.wait_for('message', check=lambda m: m.author == player)
            elif guess == 2:
                await player.send(f"The currency of this country is {currency}")
                user_input = await client.wait_for('message', check=lambda m: m.author == player)
            elif guess == 3:
                await player.send(f"The capital of this country is: {capital}")
                user_input = await client.wait_for('message', check=lambda m: m.author == player)
            if user_input.content.lower() == "exit":
                await player.send("Goodbye")
                game_in_progress = False
                return
            if user_input.content.lower() != country_name.lower() and guess < 3:
                await player.send("Incorrect Country, please try again with a new hint!")
                guess += 1
            elif user_input.content.lower() == country_name.lower() and guess <= 3:
                await player.send("Congratulations! You win this round!")
                score += (-guess + 4)*2
                wins += 1
                won = True
                break
            elif user_input.content.lower() != country_name.lower() and guess >= 3:
                guess += 1

        if not won and round_number <= rounds + 1:
            await player.send(f"Bummer! The country was {country_name}. Better luck next round")
            lives -= 1
        elif not won and round_number > rounds + 1:
            await player.send(f"Bummer! The country was {country_name}")
        if lives == 0:
            break

    await player.send(f"Game over! Your score is #{score}. You won {wins} round/s")  # End of the game
    await submit_player(player, score, wins, rounds)


async def get_country_data():
    rand = randint(1, 112)
    total_query = f"SELECT * FROM country WHERE country_id = {rand}"
    cursor.execute(total_query)
    row = cursor.fetchone()
    print(row)
    country_name = row[1]  # Index 1 gives the second element (country_name)
    capital = row[2]  # Index 2 gives the third element (capital)
    currency = row[3]  # Index 3 gives the fourth element (currency)
    languages = row[4]
    return country_name, capital, currency, languages


async def submit_player(username, score, wins, rounds):
    cursor.execute("Insert INTO player_data (username, score, wins, rounds) VALUES (%s, %s, %s, %s)",
                   (str(username), score, wins, rounds))
    db.commit()


async def leaderboard():
    cursor.execute("SELECT * FROM player_data ORDER BY score DESC LIMIT 5")
    rows = cursor.fetchall()
    return rows


# Step 3: Handle the startup of the bot
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')


# Step 4:  Let's handle the messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:  # The bot wrote the message, or the bot talks to itself
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


async def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if 'hi' in lowered or 'hello' in lowered or 'hey' in lowered:
        return f'**Hi**, I am **CountryBot**! I\'m a geography based game bot for Discord! \n' \
               f'Just tell me if you need **\'help\'** and I will provide you with some guidance.'
    elif 'help' in lowered:
        return f'If you would like to play a game, just say so! \n' \
               f'Type **\'game\'** to start a DM between us where you will get more instructions.'
    elif 'roll dice' in lowered:
        return f'You rolled a {randint(1, 6)}'
    else:
        return f'**Hi**, I am **CountryBot**! I\'m a geography based game bot for Discord! \n' \
               f'Just tell me if you need **\'help\'** and I will provide you with some guidance.'


# Step 5 Main Starting point
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()

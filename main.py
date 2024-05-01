import os
import asyncio
import sys
import logging

from dotenv import load_dotenv
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from telethon import TelegramClient

# Load environment variables from .env file
load_dotenv()

# Define environment variables
BOT_TOKEN = os.environ['BOT_TOKEN']  # Telegram bot token
TT_API_ID = os.environ['API_ID']  # Telegram API ID
TT_API_HASH = os.environ['API_HASH']  # Telegram API hash

# Create a dispatcher for handling incoming messages
dp = Dispatcher()

# Initialize TelegramClient instance for interacting with Telegram
client = TelegramClient('usernameToid', api_id=TT_API_ID, api_hash=TT_API_HASH)


# Function to retrieve the user ID for a given username
async def get_user_id(username):
    """
    Asynchronously retrieves the Telegram user ID for the specified username.

    Args:
        username (str): The Telegram username to lookup.

    Returns:
        int: The user ID if found; None otherwise.
    """
    try:
        user = await client.get_entity(username)
        return user.id
    except ValueError:
        return None


# Handler for the '/start' command
@dp.message(CommandStart())
async def cmd_start(message: Message):
    """
    Responds to the '/start' command by instructing the user to enter a username.

    Args:
        message (Message): The incoming Telegram message.
    """
    await message.answer('Enter the username, please.')


# Handler for any message received by the bot (excluding '/start' commands)
@dp.message()
async def cmd_username(message: Message):
    """
    Handles incoming messages, retrieves the user ID for the provided username,
    and informs the user of the retrieved ID or an error message if not found.

    Args:
        message (Message): The incoming Telegram message.
    """
    username = message.text  # Extract the username from the message text

    await message.answer('Wait...')  # Indicate processing

    user_id = await get_user_id(username)  # Retrieve user ID

    if user_id:
        await message.answer(f"User ID: {user_id}")  # Inform user of ID
    else:
        await message.answer("User not found.")  # Inform user of error


# Main function to start the bot and polling process
async def main():
    """
    Starts the TelegramClient, creates a Bot instance, and initiates polling for messages.
    """
    await client.start()  # Start TelegramClient

    bot = Bot(BOT_TOKEN)  # Create Bot instance

    await dp.start_polling(bot)  # Start polling for incoming messages


if __name__ == "__main__":
    """
    Configures logging and attempts to run the main function. Handles KeyboardInterrupt.
    """
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print('Was stoped a script by button')

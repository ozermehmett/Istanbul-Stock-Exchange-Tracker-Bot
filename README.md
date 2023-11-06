# Istanbul Stock Exchange Tracker Bot

This Telegram bot is designed to help users track and manage their stock portfolios on the Istanbul Stock Exchange. With a simple command interface, users can easily add new stocks to their watchlist, remove them, or receive live updates on their current stock prices.

## Features

- **Track Stocks**: Add and track specific stocks from the Istanbul Stock Exchange.
- **Live Updates**: Receive scheduled updates on the latest stock prices.
- **Manage Watchlist**: Users can manage their watchlist by adding new stocks or removing existing ones.

## Installation

To set up the bot for development or personal use, follow these steps:

1. Clone the repository:
   `git clone https://github.com/ozermehmett/Istanbul-Stock-Exchange-Tracker-Bot.git`
   
2. Install the required dependencies:
   `pip install -r requirements.txt`
   
3. Create an .env file to store your Telegram Bot Token and Collect API Key:
   `TOKEN = your_telegram_bot_token
   API = your_collectapi_key`
   

## Usage

To start and interact with the bot, follow these steps:

+ To start the bot, run:
  + `python main.py`

+ Commands
  + `/start`: Initialize the bot and set up user file for tracking.
  + `/new_stock`: Add a new stock to your watchlist.
  + `/delete <stock_name>`: Remove a stock from your watchlist.
  + `/send_stocks`: Receive the latest prices for your tracked stocks.

## Scheduled Jobs
+ The bot is configured to fetch the latest stock prices at 10:02, 13:00, and 18:00 every day. You can modify these times in `telegram_bot.py`

## Did you find this repository helpful?
+ Do not forget to give a start

## Didn't you?
+ Then fork this repo, make it BETTER and do not forget to give a STAR

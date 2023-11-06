from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import schedule
import time
from get_data import get
from main import TOKEN


user_requests = {}


def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Welcome, this bot tracks Istanbul Stock Exchange stocks.")
    create_user_symbols_file(chat_id)


def new_stock_name(update, context):
    chat_id = update.effective_chat.id
    user_requests[chat_id] = True
    context.bot.send_message(chat_id=chat_id, text="You can now enter the name of the new stock you want to track.")


def handle_new_stock(update, context):
    chat_id = update.effective_chat.id
    if chat_id in user_requests and user_requests[chat_id]:
        stock_name = update.message.text

        with open('all_symbols.txt', 'r') as all_file, open(f'{chat_id}_symbols.txt', 'r') as user_file:
            all_symbols = [line.strip() for line in all_file]
            user_symbols = [line.strip() for line in user_file]

        if stock_name in all_symbols:
            if stock_name in user_symbols:
                context.bot.send_message(chat_id=chat_id, text="This stock is already registered")
            else:
                with open('users.txt', 'r+') as users_file:
                    existing_users = [line.strip() for line in users_file]
                    if str(chat_id) not in existing_users:
                        users_file.write(str(chat_id) + "\n")

                user_symbols_file = f"{chat_id}_symbols.txt"
                with open(user_symbols_file, "a") as user_file:
                    user_file.write(stock_name + "\n")
                context.bot.send_message(chat_id=chat_id, text=f"{stock_name} added to your stock list")
            del user_requests[chat_id]
        else:
            context.bot.send_message(chat_id=chat_id, text="Such a stock name couldn't be found, please try again.")
    else:
        context.bot.send_message(chat_id=chat_id, text="Please start with /new_stock command to add a new stock.")


def create_user_symbols_file(chat_id):
    # user_symbols_file = f"{chat_id}_symbols.txt"
    # with open(user_symbols_file, "w"):
    #     pass

    user_symbols_file = f"{chat_id}_symbols.txt"

    try:
        with open(user_symbols_file, "x"):
            pass
    except FileExistsError:
        print(f"{user_symbols_file} already exists. It couldn't be created.")


def send_stocks(update, context):
    chat_id = update.effective_chat.id

    with open('stock_last_prices.txt', 'r') as stock_file, open(f'{chat_id}_symbols.txt', 'r') as user_file:
        user_stocks = [line.strip() for line in user_file]
        stocks = [line.strip() for line in stock_file]

    stock_prices = {}

    message = ""

    for user_stock in user_stocks:
        for line in stocks:
            parts = line.strip().split('-')
            stock_name, price = parts
            stock_prices[stock_name] = price

            if stock_name == user_stock:
                message += stock_name + "\t" + price + "\n"
    context.bot.send_message(chat_id=chat_id, text=message)


def delete(update, context):
    chat_id = update.effective_chat.id
    stock_name = context.args[0]

    with open(f'{chat_id}_symbols.txt', 'r') as user_file:
        user_symbols = [line.strip() for line in user_file]

    if stock_name in user_symbols:
        user_symbols.remove(stock_name)

        with open(f'{chat_id}_symbols.txt', 'w') as file:
            for item in user_symbols:
                file.write(item + "\n")

        if not user_symbols:
            with open('users.txt', 'r') as users:
                lines = users.readlines()
            with open('users.txt', 'w') as users:
                for line in lines:
                    if line.strip() != str(chat_id):
                        users.write(line)

        context.bot.send_message(chat_id=chat_id, text=f"{stock_name} has been removed from your stock list")
    else:
        message = "You haven't saved such a stock. You can see your saved stocks below:\n"
        for item in user_symbols:
            message += item + "\n"
        context.bot.send_message(chat_id=chat_id, text=message)


def get_stock_last_price_by_id(bot, chat_id):
    with open('stock_last_prices.txt', 'r') as stock_file, open(f'{chat_id}_symbols.txt', 'r') as user_file:
        user_stocks = [line.strip() for line in user_file]
        stocks = [line.strip() for line in stock_file]

    stock_prices = {}
    message = ""

    for user_stock in user_stocks:
        for line in stocks:
            parts = line.split('-')
            stock_name, price = parts
            stock_prices[stock_name] = price

            if stock_name == user_stock:
                message += f"{stock_name}\t{price}\n"

    if message:
        bot.send_message(chat_id=chat_id, text=message)
    else:
        bot.send_message(chat_id=chat_id, text="You don't have any stocks on your list.")


def scheduled_job():
    get()
    bot = Updater(token=TOKEN, use_context=True).bot

    with open("users.txt", 'r') as users_file:
        user_ids = [line.strip() for line in users_file]

    for user_id in user_ids:
        get_stock_last_price_by_id(bot, user_id)


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("new_stock", new_stock_name))
    dp.add_handler(CommandHandler("delete", delete))
    dp.add_handler(CommandHandler("send_stocks", send_stocks))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_new_stock))
    updater.start_polling()
    updater.idle()

    schedule.every().day.at("10:02").do(scheduled_job)
    schedule.every().day.at("13:00").do(scheduled_job)
    schedule.every().day.at("18:00").do(scheduled_job)

    while True:
        schedule.run_pending()
        time.sleep(1)

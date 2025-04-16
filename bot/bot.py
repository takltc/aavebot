import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import credentials
import telebot
import utils
from telebot import types

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
try:
    bot = telebot.TeleBot(credentials.bot_token)
except Exception as e:
    logging.error(f"Connect Telegram API Exception: {e}", exc_info=True)


def construct_apy_result(reserves, output, is_stable=False):
    for i in range(len(reserves)):
        network = "(" + reserves[i].network + ")" if is_stable else ""
        deposit_apy = (
            "<0.01" if reserves[i].deposit_apy < 0.01 else str(reserves[i].deposit_apy)
        )
        variable_borrow_apy = (
            "<0.01"
            if reserves[i].variable_borrow_apy < 0.01
            else str(reserves[i].variable_borrow_apy)
        )
        output += (
            reserves[i].symbol
            + network
            + ": \t"
            + "deposit APY: \t"
            + deposit_apy
            + "%"
            + " borrow APY: \t"
            + variable_borrow_apy
            + "%"
        )
        if i != len(reserves) - 1:
            output += "\n"
    return output


def make_application_button():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_stable = types.KeyboardButton("StableCoins")
    btn_networks = types.KeyboardButton("Networks")
    markup.add(btn_stable, btn_networks)
    return markup


@bot.message_handler(commands=["start"])
def send_welcome(message):
    try:
        bot.send_message(
            message.chat.id,
            "Welcome to the Aave APY Monitor Bot! Input /apy to get deposit/borrow APYs from aave markets.",
            reply_markup=make_application_button(),
        )
    except Exception as e:
        logging.error(f"Catch an exception: {e}", exc_info=True)


@bot.message_handler(commands=["apy"])
def send_welcome(message):
    try:
        bot.send_message(
            message.chat.id,
            "Choose your option",
            reply_markup=make_application_button(),
        )
    except Exception as e:
        logging.error(f"Catch an exception: {e}", exc_info=True)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    options = [
        "Ethereum",
        "Base",
        "Arbitrum",
        "Avalanche",
        "Fantom",
        "Harmony",
        "Optimism",
        "Polygon",
        "Metis",
        "Gnosis",
        "BNB Chain",
        "Scroll",
    ]
    try:
        if message.text == "Networks":
            network_markup = types.ReplyKeyboardMarkup(
                row_width=2, one_time_keyboard=True
            )
            btn1 = types.KeyboardButton("Ethereum")
            btn2 = types.KeyboardButton("Base")
            btn3 = types.KeyboardButton("Arbitrum")
            btn4 = types.KeyboardButton("Avalanche")
            btn5 = types.KeyboardButton("Fantom")
            btn6 = types.KeyboardButton("Harmony")
            btn7 = types.KeyboardButton("Optimism")
            btn8 = types.KeyboardButton("Polygon")
            btn9 = types.KeyboardButton("Metis")
            btn10 = types.KeyboardButton("Gnosis")
            btn11 = types.KeyboardButton("BNB Chain")
            btn12 = types.KeyboardButton("Scroll")
            network_markup.add(
                btn1,
                btn2,
                btn3,
                btn4,
                btn5,
                btn6,
                btn7,
                btn8,
                btn9,
                btn10,
                btn11,
                btn12,
            )
            bot.send_message(
                message.chat.id,
                text=f"Please choose the network: ",
                reply_markup=network_markup,
            )
        elif message.text == "StableCoins":
            stable_coins = []
            with ThreadPoolExecutor(max_workers=12) as executor:
                futures = [
                    executor.submit(utils.fetch_apy, option) for option in options
                ]
                for future in as_completed(futures):
                    reserves = future.result()
                    for reserve in reserves:
                        if (
                            "usd" in reserve.symbol.lower()
                            or "dai" in reserve.symbol.lower()
                        ):
                            stable_coins.append(reserve)
            stable_coins = sorted(
                stable_coins, key=lambda x: x.deposit_apy, reverse=True
            )
            output = (
                f"These are all the APYs of stable coins, decreased by deposit APY: \n"
            )
            output = construct_apy_result(stable_coins, output, True)
            bot.send_message(
                message.chat.id, text=output, reply_markup=make_application_button()
            )
        elif message.text in options:
            reserves = utils.fetch_apy(message.text)
            if reserves:
                reserves = sorted(reserves, key=lambda x: x.deposit_apy, reverse=True)
                output = f"These are all the APYs on {message.text}, decreased by deposit APY: \n"
                output = construct_apy_result(reserves, output)
            else:
                output = f"Sorry, we cannot find the APYs on {message.text}."
            bot.send_message(
                message.chat.id, text=output, reply_markup=make_application_button()
            )
        else:
            bot.send_message(
                message.chat.id,
                "Please input a valid option.",
                reply_markup=make_application_button(),
            )
    except Exception as e:
        logging.error(f"Catch an exception: {e}", exc_info=True)


if __name__ == "__main__":
    bot.infinity_polling()

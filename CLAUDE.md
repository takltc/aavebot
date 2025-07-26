# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project is a Telegram bot that provides Aave APY (Annual Percentage Yield) information to users. It's built with Python, using Flask for the web server to handle Telegram webhooks and the `pyTelegramBotAPI` library for interacting with the Telegram Bot API.

The bot fetches APY data from Aave's subgraphs on The Graph using GraphQL queries.

## Key Files

-   `app.py`: The main Flask application that receives webhook notifications from Telegram. It has been deprecated.
-   `bot/bot.py`: The core logic for the Telegram bot, including command handlers and message processing. This is the entry point for the bot.
-   `bot/utils.py`: Contains functions for fetching and calculating APY data from the Aave subgraphs.
-   `bot/model.py`: Defines the `Aave` data model for storing reserve information.
-   `bot/credentials.py`: Stores the Telegram bot token. This file is not checked into version control.
-   `bot/credentials.py.example`: An example credentials file. Copy this to `bot/credentials.py` and add your credentials.

## How to run the bot

To run the bot, execute the following command:

```bash
python bot/bot.py
```

## Architecture

The bot's architecture is straightforward:

1.  `bot/bot.py` initializes the Telegram bot and defines handlers for different commands (`/start`, `/apy`) and messages.
2.  When a user interacts with the bot, the corresponding handler in `bot.py` is triggered.
3.  To fetch APY data, the bot calls the `fetch_apy` function in `bot/utils.py`.
4.  `bot/utils.py` constructs a GraphQL query and sends it to the appropriate Aave subgraph URL for the selected network.
5.  The subgraph URLs are defined in a dictionary in `bot/utils.py`.
6.  The received data is processed, APYs are calculated, and the results are formatted into a message that is sent back to the user.
7. The `Aave` class in `bot/model.py` is used as a data structure to hold the information for each reserve.

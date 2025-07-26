# Aave APY Monitor Bot

This is a Telegram bot that provides Aave APY (Annual Percentage Yield) information to users.

## Features

-   Get deposit and borrow APYs from various Aave markets.
-   Supports multiple networks including Ethereum, Arbitrum, Polygon, and more.
-   Provides a simple interface to query APYs for stablecoins or specific networks.

## How to Use

1.  Start a chat with the bot on Telegram.
2.  Use the `/start` or `/apy` command to see the options.
3.  Choose to view APYs for "StableCoins" or select a specific "Network".

## How to Run Your Own Instance

1.  Clone this repository:
    ```bash
    git clone https://github.com/takltc/aavebot.git
    cd aavebot
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You may need to create a `requirements.txt` file first. See the `pyproject.toml` or `Pipfile` for dependencies, or install them manually: `pip install pyTelegramBotAPI Flask gql requests`)*

3.  Set up your credentials:
    -   Copy `bot/credentials.py.example` to `bot/credentials.py`.
    -   Edit `bot/credentials.py` and fill in your actual Telegram bot token, bot username, and The Graph API key.

4.  Run the bot:
    ```bash
    python bot/bot.py
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

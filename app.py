import json
import logging
import os
import re
import signal
import sys
import time
from datetime import datetime
from decimal import Decimal

from binance.client import Client
from dotenv import load_dotenv
from telethon import TelegramClient, events

import modules.dumper as dumper
import modules.env_loader as env_loader
from modules.asset import Asset, AssetEncoder
from modules.coin_data import CoinData
import modules.trader as trader

# ============================================================================= #
# =============================== BEGIN INPUTS ================================ #
# ============================================================================= #

# Pairing coin in your wallet
PAIRING = 'BTC'
# Pairing coin amount in your wallet
BALANCE = 1
# Testing mode to test the bot
TESTNET = True
# Set to True to use 75% of your balance
SAFE_MODE = True
# Seconds to wait between each buy and sell
TIME_TO_WAIT = 10
# Stoploss percentage. Set to 0 to disable
STOPLOSS = 0.9
# Pump channel Telegram chat ID
CHAT_ID = -1001448562668
# Message template to detect pump signal
MESSAGE_TEMPLATE = 'The coin we have picked to pump today is'

# ============================================================================= #
# ================================ END INPUTS ================================= #
# ============================================================================= #


env_loader.load_env(debug=True)
trader.init_trader(TESTNET)

if SAFE_MODE:
    BALANCE = BALANCE * 0.75

ASSETS = {}


def main():
    signal.signal(signal.SIGINT, signal_handler)
    logging.basicConfig(
        level=logging.INFO,
        filename=f'logs/log_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log',
        filemode='w',
        format="%(asctime)-15s %(levelname)-8s %(message)s"
    )
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info('Starting bot...')
    with TelegramClient('logs/telegram', os.getenv('TELEGRAM_API_ID'), os.getenv('TELEGRAM_API_HASH')) as telegramClient:

        @telegramClient.on(events.NewMessage(incoming=True, pattern=MESSAGE_TEMPLATE, chats=CHAT_ID))
        async def handler(event):
            handle_pump_signal(event.message.text)

        logging.info('Bot started!')
        telegramClient.run_until_disconnected()


def signal_handler(signal, frame):
    logging.info('Exiting...')
    dumper.dump_all_assets(ASSETS)
    logging.info('Exited!')
    sys.exit(0)


def handle_pump_signal(message):
    try:
        coin = re.search('[#]\w+', message).group(0)[1:].upper()
        logging.info(f'Pump detected on {coin}!')
        buy(coin)
        logging.info(f'Waiting {TIME_TO_WAIT} seconds...')
        time.sleep(TIME_TO_WAIT)
        sell(coin)
        logging.info(f'Pump finished on {coin}!')
        dumper.dump_asset(ASSETS[coin])
    except Exception as e:
        logging.critical(f'Unexpected error occured: {e}')


def compute_coin_data(coin):
    logging.info(f'Getting {coin} data...')
    try:
        price = trader.get_symbol_ticker(symbol=coin, pairing=PAIRING)['price']
        return CoinData(coin, Decimal(price), round(BALANCE / float(price)))
    except Exception as e:
        raise Exception(f'Error getting {coin} data: {e}')


def buy(coin):
    try:
        coin_data = compute_coin_data(coin)
        logging.info(f'Data retrieved for {coin}')
    except Exception as e:
        logging.error(f'Failed to buy {coin}. Reason: {e}')
        return
    try:
        logging.info(
            f'Buying {coin_data.amount} {coin} at {coin_data.price} {PAIRING}...')
        buy_order = trader.create_market_order(
            symbol=coin,
            pairing=PAIRING,
            side="BUY",
            quantity=coin_data.amount
        )
        if coin in ASSETS:
            ASSETS[coin].amount += coin_data.amount
            ASSETS[coin].orders.append(buy_order)
        else:
            ASSETS[coin] = Asset(
                coin,
                coin_data.amount,
                [buy_order],
                None
            )
        if STOPLOSS > 0:
            try:
                logging.info(f'Placing {coin} stoploss order...')
                stoploss_order = trader.create_limit_order(
                    symbol=coin,
                    pairing=PAIRING,
                    side="SELL",
                    quantity=coin_data.amount,
                    price=Decimal(round(coin_data.price*Decimal(STOPLOSS), 6))
                )
                ASSETS[coin].stoploss_order = stoploss_order
                logging.info(f'{coin} stoploss order placed')
            except Exception as e:
                raise Exception(f'Error placing {coin} stoploss order: {e}')
        logging.info(f'Successfully bought {coin_data.amount} {coin}')
    except Exception as e:
        logging.error(f'Failed to buy {coin}. Reason: {e}')


def sell(coin):
    if coin in ASSETS and ASSETS[coin].amount > 0:
        try:
            logging.info(
                f'Selling {ASSETS[coin].amount} {coin} to {PAIRING}...')
            sell_oder = trader.create_market_order(
                symbol=coin,
                pairing=PAIRING,
                side="SELL",
                quantity=ASSETS[coin].amount
            )
            logging.info(f'Successfully sold {ASSETS[coin].amount} {coin}')
            ASSETS[coin].amount = 0
            ASSETS[coin].orders.append(sell_order)
            if ASSETS[coin].stoploss_order is not None:
                try:
                    logging.info(f'Cancelling {coin} stoploss order...')
                    trader.cancel_order(
                        symbol=coin,
                        pairing=PAIRING,
                        order_id=ASSETS[coin].stoploss_order['orderId'],
                    )
                    logging.info(f'{coin} stoploss order cancelled')
                except Exception as e:
                    logging.warning(
                        f'Failed to cancel {coin} stoploss order. Reason: {e}')
        except Exception as e:
            logging.error(f'Failed to sell {coin} Reason: {e}')
    else:
        logging.warning(f'No {coin} to sell')


if __name__ == "__main__":
    main()
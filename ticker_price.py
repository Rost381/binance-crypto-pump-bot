import logging
import datetime
from binance.cm_futures import CMFutures
from binance.lib.utils import config_logging

config_logging(logging, logging.DEBUG)

cm_futures_client = CMFutures()
vv= cm_futures_client.ticker_price("BTCUSD_PERP")
logging.info(vv)
print(vv[0])
date_time = datetime.datetime.fromtimestamp(vv[0]["time"]/1000)
print(date_time)
# logging.info(cm_futures_client.pm_exchange_info())
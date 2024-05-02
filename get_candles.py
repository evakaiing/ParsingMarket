from tinkoff.invest import Candle, CandleInterval, Client, HistoricCandle, GetCandlesResponse
from pandas import DataFrame

from datetime import datetime, timezone, timedelta
import logging

import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

logging.basicConfig(filename="get_candles.log")

token = "t.IEa99GPRoD0m0Z3MH_M2BUMIAVsqYMCpcmJhQFIKDw8rg3tk7CpENgicqyVpOMSTK1ubCt1ZB7SQCXTcEy0Dcw"


def get_history_of_current_currency(figi, start_date, end_date, interval=CandleInterval.CANDLE_INTERVAL_DAY):
    with Client(token) as client:
        try:
            candles_responce = client.market_data.get_candles(
                figi='BBG004730N88',
                from_=start_date,
                to=end_date,
                interval=interval
            )

            df = create_df(candles_responce)
            print(df.tail(30))
            df.plot(x='time', y='close')
            plt.show()

        except Exception as e:
            logging.error(f" Error in get_history_of_current_currency for FIGI {figi}': {e}")
            return None


def create_df(candles_responce: [HistoricCandle]):
    candles = candles_responce.candles
    df = DataFrame([{
        'time': c.time,
        'volume': c.volume,
        'open': cast_money(c.open),
        'close': cast_money(c.close),
        'high': cast_money(c.high),
        'low': cast_money(c.low),
    } for c in candles])

    return df


def cast_money(v):
    return v.units + v.nano / 1e9  # nano - 9 нулей


if __name__ == "__main__":
    figi = 'BBG004730N88'
    get_history_of_current_currency(figi, datetime.utcnow() - timedelta(days=7), datetime.utcnow())

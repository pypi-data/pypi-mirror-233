import logging, time, os
import pandas as pd
import numpy as np
import datetime as dt
from core.report.calc_features.CalculateStats import CalculateStats

pd.set_option('display.width', 1000, 'display.max_columns', 1000)

def setup_trade_data(chunk):
    trade_data = pd.read_pickle('../../../data/BuyOnlyBreakevenRetest/trade_data.p')
    data = CalculateStats(trade_data=trade_data, chunk=chunk)
    return data

obj = setup_trade_data(chunk=20)

print(obj.pnl_data)
print(obj.stat_data)
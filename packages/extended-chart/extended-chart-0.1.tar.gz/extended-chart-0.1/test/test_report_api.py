from core.report import CalculatePnLStats
import logging, time, os
import pandas as pd
import numpy as np
import datetime as dt

pd.set_option('display.width', 1000, 'display.max_columns', 1000)

def setup_trade_data():
    trade_data = pd.read_pickle('../data/BuyOnlyBreakevenRetest/trade_data.p')
    return trade_data

def create_features_data():
    df = pd.read_pickle('../data/2019_ES.p')

    return df

trade_data = setup_trade_data()

def test_no_features_data_no_stats():
    data = CalculatePnLStats(trade_data=trade_data)

    print(data.pnl_data)
    print(data.stats_data)
    # print(data.get_features)

def test_no_features_data_with_full_stats(chunk):
    data = CalculatePnLStats(trade_data=trade_data, stats_chunk=chunk)

    print(data.pnl_data)
    print(data.stats_data)

    print(data.get_pnl(212))
    print(data.get_pnl(300))

    pnl = data.get_pnl(212)
    features = data.get_feature(212)

    print(features)



# run the following test
# test_no_features_data_no_stats()
# test_no_features_data_with_full_stats(chunk=0)
# test_no_features_data_with_full_stats(chunk=100)
test_no_features_data_with_full_stats(chunk='90D')

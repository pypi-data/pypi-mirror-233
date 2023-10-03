import logging, time, os
import pandas as pd
import numpy as np
import datetime as dt
from core.report.calc_features.GenerateFeatures import GenerateFeatures

pd.set_option('display.width', 1000, 'display.max_columns', 1000)

def setup_features_and_pnl_data():
    features = pd.read_pickle('../../../data/2019_ES.p')
    pnl_data = pd.read_pickle('../../../data/pnl_data_with_mae_mfe.p')
    data = GenerateFeatures(pnl_data=pnl_data, features_data=features, columns=['open_p', 'high_p'], leading_seconds=60 * 5,
                            trailing_seconds=60 * 5)
    return data


data = setup_features_and_pnl_data()

for trade in [10, 20, 30, 300]:
    t = data.get_feature_set(trade)
    print(t.pnl)
    print(t.pnl.entry_price, t.pnl.entry_time)
    print(t.feature)
    print('\n\n')

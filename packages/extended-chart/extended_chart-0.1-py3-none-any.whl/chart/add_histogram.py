from types import NoneType
from pandas import DataFrame, Series
from chart.add_overlay import add_overlay


# TODO: I would like to use histograms into my charts for rendering equity curves and indicator histograms
#  but tradingview lightweight chart does not support y-axis for histograms so I can't use this method

def add_histogram(chart, data, label: str | None = None, color='#2596be', price_line: bool = False, price_label: bool = False):

    if isinstance(data, Series):
        data = data.to_frame()

    if len(data.columns) == 1:
        if isinstance(label, NoneType):
            rename_label = data.columns[0]
        else:
            rename_label = label
        data.columns = [rename_label]
        data['color'] = color

    elif len(data.columns) == 2 and 'color' in data.columns:
        rename_label = label
        label = set(data.columns) - set(['color'])
        label = list(label)[0]

        if not rename_label:
            rename_label = label

        data = data.rename(columns={label: rename_label})

    else:
        raise Exception('Histogram only accepts one value; and optional column color')

    # TODO: Not possible by tradingview lightweight api - https://github.com/louisnw01/lightweight-charts-python/issues/124
    # add_overlay(chart, data=data.drop('color', axis=1, errors='ignore'), color='rgba(0,0,0,0)')
    hist_chart = chart.create_histogram(name=rename_label, price_label=price_label, price_line=price_line)
    hist_chart.set(data)

    return hist_chart

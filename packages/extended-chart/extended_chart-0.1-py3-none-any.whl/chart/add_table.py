import pandas as pd
import datetime as dt
from chart import ExtendedChart

# TODO: This needs to be provided from chart.style so that it is consistent
color_style = {'background_style': {'background_color': '#171B26'}}


def row_click_event(e):
    print(e)


def row_move_to_chart(chart: ExtendedChart, e):
    chart.set_visible_range(start_time=e.get('ENTRY TIME'), end_time=e.get('EXIT TIME'))
    print(e)


def _formate_value(x):
    if isinstance(x, dt.timedelta):
        x = x.components
        hours = x.days * 24 + x.hours
        minutes = x.minutes
        seconds = x.seconds

        return f'{hours}:{minutes}:{seconds}'

    return x


rename_stats_col = dict(
    net_profit=dict(title='Net Profit', format='{: >10,.0f}'),
    gross_profit=dict(title='Gross Profit', format='{:,.0f}'),
    gross_loss=dict(title='Gross Loss', format='{:,.0f}'),
    total_commission=dict(title='Commission', format='{:,.0f}'),
    max_drawdown=dict(title='Drawdown', format='{:,.0f}'),
    number_of_winning_trades=dict(title='Win Count', format='{:,.0f}'),
    number_of_losing_trades=dict(title='Loss Count', format='{:,.0f}'),
    total_trade_count=dict(title='Total Trades', format='{:,.0f}'),
    largest_winning_trade=dict(title='Largest Win', format='{:,.0f}'),
    largest_losing_trade=dict(title='Largest Loss', format='{:,.0f}'),
    average_winning_trade=dict(title='Average Win', format='{:,.0f}'),
    average_losing_trade=dict(title='Average Loss', format='{:,.0f}'),
    average_mfe=dict(title='Average MFE', format='{:,.2f}'),
    average_mae=dict(title='Average MAE', format='{:,.2f}'),
    average_winning_percentage=dict(title='Win Pct.', format='{:,.3f}'),
    average_losing_percentage=dict(title='Losing Pct.', format='{:,.3f}'),
    profit_factor=dict(title='Profit Factor', format='{:,.2f}'),
    sharpe_ratio=dict(title='Sharpe Ratio', format='{:,.2f}'),
    consecutive_winners=dict(title='Consecutive Wins', format='{:,.2f}'),
    consecutive_losers=dict(title='Consecutive Losses', format='{:,.2f}'),
    average_trade_time=dict(title='Average Trade Time', format='{:}'),
    average_winning_time=dict(title='Average Winning Time', format='{:}'),
    average_losing_time=dict(title='Average Losing Time', format='{:}'),
    average_time_between_trades=dict(title='Average Flat Time', format='{:}'),
    max_flat_time=dict(title='Max Flat Time', format='{:}'),
)

columns = ['entry_time', 'exit_time', 'direction', 'entry_price', 'exit_price', 'quantity', 'pnl_with_commission', 'mfe',
           'mae', 'time_to_live']
heading = ['#', 'ENTRY TIME', 'EXIT TIME', 'DIRECTION', 'ENTRY PX', 'EXIT PX', 'QTY.', 'PNL', 'MFE', 'MAE', 'TTL']

rename_pnl_col = dict(
    entry_time=dict(title='ENTRY TIME', format='{:}'),
    exit_time=dict(title='EXIT TIME', format='{:}'),
    direction=dict(title='DIRECTION', format='{:}'),
    entry_price=dict(title='ENTRY PX', format='{:,.2f}'),
    exit_price=dict(title='EXIT PX', format='{:,.2f}'),
    quantity=dict(title='QTY.', format='{:,.0f}'),
    pnl_with_commission=dict(title='PNL', format='{:,.2f}'),
    mfe=dict(title='MFE', format='{:,.2f}'),
    mae=dict(title='MAE', format='{:,.2f}'),
    time_to_live=dict(title='TTL', format='{:}'),
)


def add_stats_table(chart, data, height=1, width=0.4, position='right', color_style=color_style):
    # TODO: I need to address this becasue the stats chunk for NONE is not working
    print(data)
    data = data.droplevel(level='chunk')
    data = data.T.reset_index()
    data.index = data.index + 1

    table = chart.create_table(position=position, height=height, width=width, headings=['#', 'STAT', 'BOTH', 'LONG', 'SHORT'],
                               func=row_click_event, alignments=('center', 'left', 'right', 'right', 'right'))

    for x in data.itertuples():
        _stat = rename_stats_col.get(x.index, {'title': x.index, 'format': '{:}'})

        _stat_both = _stat.get('format').format(_formate_value(x.BOTH)) if not (pd.isna(x.BOTH) or x.BOTH == 0) else '-'
        _stat_long = _stat.get('format').format(_formate_value(x.LONG)) if not (pd.isna(x.LONG) or x.LONG == 0) else '-'
        _stat_short = _stat.get('format').format(_formate_value(x.SHORT)) if not (pd.isna(x.SHORT) or x.SHORT == 0) else '-'

        row = table.new_row(x.Index, _stat.get('title'), _stat_both, _stat_long, _stat_short)

        row.background_color(column='#', color=color_style.get('background_style').get('background_color'))
        row.background_color(column='STAT', color=color_style.get('background_style').get('background_color'))
        row.background_color(column='BOTH', color=color_style.get('background_style').get('background_color'))
        row.background_color(column='LONG', color=color_style.get('background_style').get('background_color'))
        row.background_color(column='SHORT', color=color_style.get('background_style').get('background_color'))

    return table


def add_pnl_table(chart, data, height, width=1, position='bottom', color_style=color_style):
    data.index = data.index + 1

    columns = ['entry_time', 'exit_time', 'direction', 'entry_price', 'exit_price', 'quantity', 'pnl_with_commission', 'mfe',
               'mae', 'time_to_live']

    alignments = ('center', 'center', 'center', 'center', 'right', 'right', 'center', 'right', 'right', 'right', 'right')

    data = data[columns]
    for col in data:
        data[col] = data[col].apply(lambda x: rename_pnl_col.get(col).get('format').format(x))

    heading = [rename_pnl_col.get(col).get('title') for col in data.columns]

    table = chart.create_table(position=position, height=height, width=width, headings=['#'] + heading,
                               func=lambda e: row_move_to_chart(chart=chart, e=e),
                               alignments=alignments)

    for x in data.itertuples():

        row = table.new_row(x.Index, x.entry_time, x.exit_time, x.direction, x.entry_price, x.exit_price, x.quantity,
                            x.pnl_with_commission, x.mfe,
                            x.mae, x.time_to_live)

        for column in heading:
            row.background_color(column=column, color=color_style.get('background_style').get('background_color'))

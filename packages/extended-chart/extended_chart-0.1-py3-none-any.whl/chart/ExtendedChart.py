from lightweight_charts import Chart
from lightweight_charts.util import LINE_STYLE
from pandas import DataFrame
from chart.add_overlay import add_overlay
from chart.add_marker import add_marker
from chart.add_trade_marker import add_trade_marker
from chart.add_histogram import add_histogram
from chart.add_background_color import add_background_color
from chart.add_table import add_stats_table, add_pnl_table
from lightweight_charts.table import Table


# TODO: Convert this into a package
# TODO: Need the ability to remove indicators easily ("Sicking for now because not important for strategy discovery)
# TODO: Streamline the style, so that it is applied at top-level and you don't need to keep re-applying it

class ExtendedChart(Chart):
    def __init__(self, *args, **kwargs):
        super(ExtendedChart, self).__init__(*args, **kwargs)

    def add_overlay(self, data: DataFrame(), color: str | list[str] | None = None,
                    style: LINE_STYLE | list[LINE_STYLE] = 'solid',
                    label: str | None | list = None, width: int | list[int] = 1, price_line: bool = False,
                    price_label: bool = False):
        return add_overlay(self, data=data, color=color, style=style, label=label, width=width, price_label=price_label,
                           price_line=price_line)

    def add_subplot(self, height, sync=True, position='bottom', *args, **kwargs) -> 'ExtendedChart':
        chart = self.create_subchart(position=position, height=height, width=kwargs.get('width', 1), sync=sync, *args,
                                     **kwargs)

        return chart

    def add_marker(self, data, marker='circle', color='#7858c4', label='', position='below'):
        return add_marker(self, data=data, marker=marker, color=color, label=label, position=position)

    def add_trade_marker(self, data, label=''):
        return add_trade_marker(self, data=data, label=label)

    def add_histogram(self, data: DataFrame(), label: str | None | list = None, color: str | list[str] | None = None,
                      price_line: bool = False, price_label: bool = False, ):
        return add_histogram(self, data=data, label=label, color=color, price_line=price_line, price_label=price_label)

    def add_background_color(self, data: DataFrame = None, start_time=None, end_time=None, color='rgba(252, 219, 3, 0.1)',
                             **kwargs):
        return add_background_color(self, data=data, start_time=start_time, end_time=end_time, color=color, **kwargs)

    def add_stats_table(self, data: DataFrame(), height=1, width=1) -> Table:
        ''' Renders stats table, requires the following dataframe:

         muli-index: [direction, chunk]
         columns: [net_profit gross_profit gross_loss total_commission max_drawdown number_of_winning_trades
         number_of_losing_trades total_trade_count largest_winning_trade largest_losing_trade average_winning_trade
         average_losing_trade average_mfe average_mae average_winning_percentage average_losing_percentage profit_factor
         sharpe_ratio consecutive_winners consecutive_losers, average_trade_time average_winning_time average_losing_time
         average_time_between_trades max_flat_time] '''

        return add_stats_table(self, data=data, height=height, width=width)

    def add_pnl_table(self, data: DataFrame(), height, width=1) -> Table:
        ''' Renders pnl table, requires the following dataframe:

        columns: [entry_time exit_time direction entry_price exit_price quantity pnl_with_commission mfe mae time_to_live]
        '''
        return add_pnl_table(self, data=data, height=height, width=width)

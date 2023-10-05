from extended_chart import ExtendedChart


def white_background(chart: ExtendedChart ) -> ExtendedChart:
    background_style = dict(background_color='#FFFFFF', text_color='#000000')
    volume_style = dict(up_color='#CCCCCC', down_color='#CCCCCC')
    grid_style = dict(style='sparse_dotted', color='#D9D9D9')
    candle_style = dict(up_color='#FFFFFF', down_color='#000000', border_up_color='#000000', border_down_color='#000000',
                        wick_up_color='#000000', wick_down_color='#000000')
    crosshair_style = dict(mode='normal', vert_color='#AAAAAA', vert_style='dashed', horz_color='#AAAAAA', horz_style='dashed')
    indicator_legend_style = dict(visible=True, ohlc=False, percent=False, lines=True, color='rgb(191, 195, 203)',
                                  font_size=12, font_family='Courier')
    price_line_style = dict(line_visible=False)

    chart.volume_config(**volume_style)
    chart.layout(**background_style)
    chart.grid(**grid_style)
    chart.crosshair(**crosshair_style)
    chart.legend(**indicator_legend_style)
    chart.candle_style(**candle_style)
    chart.price_line(**price_line_style)

    return chart



def black_background(chart: ExtendedChart) -> ExtendedChart:
    background_style = dict(background_color='#171B26', text_color='#ADB0B9')
    volume_style = dict(up_color='#2E323C', down_color='#2E323C')
    grid_style = dict(style='sparse_dotted', color='#373B45')
    candle_style = dict(up_color='#2196F3', down_color='#C2185B', border_up_color='#2196F3', border_down_color='#C2185B',
                        wick_up_color='#2196F3', wick_down_color='#C2185B')
    crosshair_style = dict(mode='normal', vert_color='#55585F', vert_style='dashed', horz_color='#55585F', horz_style='dashed')
    indicator_legend_style = dict(visible=True, ohlc=False, percent=False, lines=True, color='rgb(191, 195, 203)',
                                  font_size=12, font_family='Courier')
    price_line_style = dict(line_visible=False)

    chart.layout(**background_style)
    chart.volume_config(**volume_style)
    chart.grid(**grid_style)
    chart.crosshair(**crosshair_style)
    chart.legend(**indicator_legend_style)
    chart.candle_style(**candle_style)
    chart.price_line(**price_line_style)

    return chart

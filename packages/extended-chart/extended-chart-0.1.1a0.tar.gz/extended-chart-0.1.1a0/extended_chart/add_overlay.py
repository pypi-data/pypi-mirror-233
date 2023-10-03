from types import NoneType
from pandas import DataFrame, Series
from lightweight_charts.util import LINE_STYLE
from itertools import cycle


def color_wheel(columns=[]):
    color = ['#2596be', '#9925be', '#be4d25', '#49be25', '#bea925', '#be2540']
    cycled = cycle(color)
    return [next(cycled) for _ in range(len(columns))]


# TODO: It is possible to provide a line indicator with various colors using a color column
def add_overlay(chart, data: DataFrame | Series, color: str | list[str] | None = None,
                style: LINE_STYLE | list[LINE_STYLE] = 'solid',
                label: str | None | list = None, width: int | list[int] = 1, price_line: bool = False,
                price_label: bool = False):
    if isinstance(data, Series):
        data = data.to_frame()

    if len(data.columns) == 1:
        if isinstance(label, NoneType):
            label = data.columns[0]
        data.columns = [label] if label else data.columns
        data = data[[data.columns[0]]].dropna()

        overlay = chart.create_line(name=label, color=color_wheel(data.columns)[0], style=style, width=width,
                                    price_line=price_line, price_label=price_label)

        overlay.set(data)
        return overlay

    elif 'color' in data.columns:
        assert len(data.columns) == 2, 'Line overlay only supports one color per overlay line...'

        if label:
            rename_label = label[0] if isinstance(label, list) else label
            label = [x for x in data.columns if x != 'color'][0]
            data = data.rename(columns={label: rename_label})
        else:
            rename_label = [x for x in data.columns if x != 'color'][0]

        overlay = chart.create_line(name=rename_label, style=style, width=width, price_line=price_line,
                                    price_label=price_label)
        overlay.set(data)
        return overlay

    else:
        list_of_overlays = []
        if isinstance(label, NoneType):
            label = data.columns
        elif isinstance(label, str):
            label = [label]

        assert len(label) <= len(data.columns), "label needs to be the same length or less"
        label = [label[i] if i < len(label) else elem for i, elem in enumerate(data.columns)]

        if isinstance(color, NoneType):
            color = color_wheel(data.columns)
        elif isinstance(color, str):
            color = [color]

        assert len(color) <= len(data.columns), "color needs to be the same length or less"
        color = [color[i] if i < len(color) else elem for i, elem in enumerate(color_wheel(data.columns))]

        if isinstance(width, NoneType | int):
            width = width if width else 1
            width = [width for _ in range(len(data.columns))]
        elif isinstance(width, list):
            width = [width[i] if i < len(width) else 1 for i, _ in enumerate(data.columns)]

        if isinstance(style, NoneType):
            style = ['solid' for _ in range(len(data.columns))]
        elif isinstance(style, str):
            style = [style for _ in range(len(data.columns))]
        elif isinstance(width, list):
            style = [style[i] if i < len(style) else 'solid' for i, _ in enumerate(data.columns)]

        for i, col in enumerate(data.columns, 0):
            _data = data[[col]]

            _data.columns = [label[i]] if label[i] else _data.columns
            _data = _data[[_data.columns[0]]].dropna()

            overlay = chart.create_line(name=label[i], color=color[i], style=style[i], width=width[i],
                                        price_line=price_line, price_label=price_label)

            overlay.set(_data)
            list_of_overlays.append(overlay)

        return list_of_overlays

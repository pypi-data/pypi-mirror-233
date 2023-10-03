import numpy as np
import pandas as pd
from lightweight_charts import Chart
from lightweight_charts.util import MARKER_SHAPE, MARKER_POSITION
from datetime import datetime

def add_marker(chart: Chart, data: list[datetime], marker: MARKER_SHAPE = 'circle', color='#7858c4', label='',
               position: list[MARKER_POSITION] = 'below'):
    if isinstance(data, datetime):
        data = [data]
    if isinstance(data, np.ndarray):
        data = [x.astype(datetime) for x in data]
    if isinstance(data, pd.DataFrame):
        data = data.index.values
        data = [x.astype(datetime) for x in data]
    if isinstance(position, str):
        default_position = position
        position = [position]
    if isinstance(label, str):
        label = [label for _ in data]
    if isinstance(color, str):
        color = [color for _ in data]

    label = [label[i] if i < len(label) else '' for i, _ in enumerate(data)]
    color = [color[i] if i < len(color) else '' for i, _ in enumerate(data)]
    position = [position[i] if i < len(position) else default_position for i, _ in enumerate(data)]

    data = sorted(data)

    for i, m in enumerate(data, 0):
        chart.marker(time=m, position=position[i], shape=marker, color=color[i], text=label[i])

# plotters.py

# Plots a time-series

import os

from pathlib import Path
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.io import output_file
from bokeh.layouts import column


def generic_time_series(x, y, filename='', **kwargs):
    """ Plots a time-series. """

    # plot data and canvas settings
    p = figure(plot_width=1440, plot_height=650, x_axis_type='datetime')
    p.line(x, y, color='orange', line_width=4.0, legend_label=kwargs.get('main_legend_label', filename))
    if 'mean' in kwargs:
        mean = kwargs['mean']
        mean_series = [mean for _ in range(len(y))]
        p.line(x, mean_series, color='blue', line_width=1.5, legend_label='Mean')
    if 'multi' in kwargs:
        if kwargs['multi']:
            source = ColumnDataSource(data=dict(
                x=kwargs['extra_x'],
                y_1 = kwargs['extra_y_1'],
                y_2 = kwargs['extra_y_2'],
                extra_y_1_hover_tool=kwargs['extra_y_1_hover_tool'],
                extra_y_2_hover_tool=kwargs['extra_y_2_hover_tool']
            ))

            extra_figure = figure(plot_width=1440, plot_height=150, x_axis_type='datetime')
            extra_figure.line(
                'x',
                'y_1',
                source=source,
                color='darkred',
                line_width=4.0,
                legend_label=kwargs.get('extra_y_1_legend_label', 'Extra 1')
            )
            extra_figure.line(
                'x',
                'y_2',
                source=source,
                color='navy',
                line_width=4.0,
                legend_label=kwargs.get('extra_y_2_legend_label', 'Extra 2')
            )
            # styling
            extra_figure.toolbar_location = None
            extra_figure.left[0].formatter.use_scientific = False
            extra_figure.legend.location = 'center_left'
            hover = HoverTool(
                tooltips=[
                    ('Date', '@x{%d-%m-%Y}'),
                    ('Speculators long', '@{extra_y_1_hover_tool}'),
                    ('Speculators short', '@{extra_y_2_hover_tool}'),
                ],
                formatters={
                    'x': 'datetime'
                }
            )
            extra_figure.tools = [hover]

    # plot styling
    p.title.text = kwargs.get('plot_title', filename)
    p.title.align = 'center'
    p.toolbar_location = None
    p.outline_line_color = None
    # p.xgrid[0].ticker.desired_num_ticks = 10
    p.xgrid.grid_line_color = None
    hover = HoverTool(
        tooltips=[
            ('Date', '@x{%d-%m-%Y}'),
            ('Rate:', '@y'),
        ],
        formatters={
            'x': 'datetime'
        }
    )
    p.tools = [hover]
    p.legend.location = 'top_right'
    p.legend.border_line_color = 'navy'
    p.legend.border_line_alpha = 0.4
    p.legend.border_line_width = 2

    # save plot to file and render
    output_dir = Path.cwd() / 'plots'
    os.makedirs(output_dir, exist_ok=True)
    output_file('plots/{}.html'.format(filename))
    if 'multi' in kwargs:
        if kwargs['multi']:
            show(column(p, extra_figure))
    else:
        show(p)
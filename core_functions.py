import requests
import pandas
from bokeh.embed import components
from bokeh.plotting import figure, gridplot
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.models import ColumnDataSource
from bokeh.charts import Histogram

BASE_URL = 'https://www.quandl.com/api/v3/datasets/WIKI/'
API_KEY = {'api_key' : 'zxWzLABZi1kY_XvMCJys'}


def get_data_subset():
    data_frame = pandas.read_pickle('final_data_clean.p')
    return data_frame


def generate_grid_scatter_plot(data_frame):
    y = data_frame['Diabetes_Pct'].values
    x1 = data_frame['Black_Pct'].values
    x2 = data_frame['Hispanic_Pct'].values
    x3 = data_frame['LowAccess_Pct'].values
    x4 = data_frame['HouseholdIncome'].values

    source = ColumnDataSource(data=dict(y=y, x1=x1, x2=x2, x3=x3, x4=x4))

    TOOLS = "crosshair,wheel_zoom,reset,tap,pan,box_select"

    p1 = figure(tools=TOOLS, width=300, plot_height=250, x_range=(-.04, 1.08), y_range=(0, 0.21))
    p1.scatter('x1', 'y', source=source, fill_alpha=0.8, line_color=None)
    p1.xaxis.axis_label = 'Percent Black'
    p1.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")
    p1.xaxis[0].formatter = NumeralTickFormatter(format="0.0%")

    p2 = figure(tools=TOOLS, width=300, plot_height=250, x_range=(-.04, 1.08), y_range=(0, 0.21))
    p2.scatter('x2', 'y', source=source, fill_alpha=0.8, line_color=None)
    p2.xaxis.axis_label = 'Percent Hispanic'
    p2.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")
    p2.xaxis[0].formatter = NumeralTickFormatter(format="0.0%")

    p3 = figure(tools=TOOLS, width=300, plot_height=250, x_range=(-.04, 1.08), y_range=(0, 0.21))
    p3.scatter('x3', 'y', source=source, fill_alpha=0.8, line_color=None)
    p3.xaxis.axis_label = 'Low Access Population'
    p3.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")
    p3.xaxis[0].formatter = NumeralTickFormatter(format="0.0%")

    p4 = figure(tools=TOOLS, width=300, plot_height=250, x_range=(9.8, 11.8), y_range=(0, 0.21))
    p4.scatter('x4', 'y', source=source, fill_alpha=0.8, line_color=None)
    p4.xaxis.axis_label = 'Household Income (log scale)'
    p4.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")

    plot_quad = gridplot([[p1, p2], [p3, p4]])

    script, dev = components(plot_quad)
    return script, dev


def generate_histogram_grid(data_frame):
    high_access = data_frame[data_frame['LowAccess_Pct'] <= data_frame['LowAccess_Pct'].quantile(0.65)]

    upper = high_access[high_access['Diabetes_Pct'] >= high_access['Diabetes_Pct'].quantile(0.50)]
    lower = high_access[high_access['Diabetes_Pct'] < high_access['Diabetes_Pct'].quantile(0.50)]

    p2 = Histogram(lower, 'SpecialtyStores_PP', bins=100, width=600, plot_height=250)
    p2.xaxis.axis_label = ''
    p2.yaxis.axis_label = 'Low Diabetes Incidence'

    p4 = Histogram(upper, 'SpecialtyStores_PP', bins=100, width=600, plot_height=250)
    p4.xaxis.axis_label = 'Specialty Stores'
    p4.yaxis.axis_label = 'High Diabetes Incidence'

    plot_list = gridplot([[p2], [p4]])

    script, dev = components(plot_list)
    return script, dev
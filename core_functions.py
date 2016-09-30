import requests
import pandas
from bokeh.palettes import BrBG9
from bokeh.plotting import figure, show
from bokeh.embed import components

BASE_URL = 'https://www.quandl.com/api/v3/datasets/WIKI/'
API_KEY = {'api_key' : 'zxWzLABZi1kY_XvMCJys'}


def form_inputs_are_valid(ticker, features):
    if ticker and len(features) > 0:
        return True

    return False


def query_quandl_database(ticker):
    request_url = BASE_URL + ticker + '.json'
    session = requests.Session()
    session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
    response = session.get(request_url, params=API_KEY)
    json_response = response.json()

    return json_response


def quandl_result_is_valid(json_response):
    response_key = json_response.keys()
    if not response_key:
        return False

    first_key = response_key[0]
    if first_key == 'dataset':
        return True

    return False

def get_data_subset(json_response, features):
    headers = json_response['dataset']['column_names']
    data_table = json_response['dataset']['data']
    data_frame = pandas.DataFrame(data_table, columns=headers)
    data_frame = data_frame.set_index('Date')
    data_frame = data_frame[features]
    return data_frame


def generate_plot_components(data_frame):
    TOOLS = 'pan,wheel_zoom,box_zoom,reset,resize,save'
    plot = figure(x_axis_type ='datetime', tools=TOOLS)
    plot.title.text = 'Data from Quandle WIKI set'
    plot.grid.grid_line_alpha=0.3
    plot.xaxis.axis_label = 'Date'
    plot.yaxis.axis_label = 'Price'
    my_palette = BrBG9[0:len(data_frame.columns)]
    i = 0
    dates = pandas.to_datetime(data_frame.index.values)
    for column in data_frame:
        plot.line(dates, data_frame[column], line_color = my_palette[i], legend=column)
        i+= 1

    script, dev = components(plot)
    return script, dev
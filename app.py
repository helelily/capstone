from flask import Flask, render_template, redirect, request
import core_functions as fn

app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        ticker = request.form['ticker']
        features = request.form.getlist('features')

        if  fn.form_inputs_are_valid(ticker, features):
            json_response = fn.query_quandl_database(ticker)

            if fn.quandl_result_is_valid(json_response):
                data_frame = fn.get_data_subset(json_response, features)
                script, div = fn.generate_plot_components(data_frame)
                return render_template('graph.html', script=script, div=div, ticker=ticker)
            else:
                return render_template('error.html')
        else:
            return render_template('error.html')

if __name__ == '__main__':
    app.run(port=33507)

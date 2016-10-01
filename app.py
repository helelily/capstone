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
        return render_template('error.html')


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'GET':
        data_frame = fn.get_data_subset()
        script1, div1 = fn.generate_grid_scatter_plot(data_frame)
        script2, div2 = fn.generate_histogram_grid(data_frame)
        return render_template('graph.html', script1=script1, div1=div1, script2=script2, div2=div2)

if __name__ == '__main__':
    app.run()

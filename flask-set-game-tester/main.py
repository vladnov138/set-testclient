from modules.testing_stages.stages import process_ip_stage
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/run_test', methods=['POST'])
def run_test():
    input_data = request.form['input_data']
    input_port = request.form['input_port']
    result, status = process_ip_stage(input_data, input_port)
    return result


if __name__ == '__main__':
    app.run(debug=True)

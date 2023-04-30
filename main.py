from modules.testing_stages.stages import process_all
from modules.connection_utils.connection_utils import set_full_ip
from modules.connection_utils.connection_utils import get_full_ip
from flask import Flask, render_template, request
import os

app = Flask(__name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def form():
    return render_template('form.html')


@app.route('/run_test', methods=['POST'])
def run_test():
    input_data = request.form['input_data']
    input_port = request.form['input_port']

    server_mode = 1 if request.form['mode'] == 'global' else 0
    room_mode = 1 if request.form['room'] == 'multiple' else 0
    set_full_ip(input_data, input_port)
    result = process_all(input_data, input_port, server_mode, room_mode)
    return result


if __name__ == '__main__':
    app.run(debug=True)

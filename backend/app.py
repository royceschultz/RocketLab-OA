from flask import Flask, request, abort
from flask_cors import CORS
import os
from modules import dao, dev

STAGE = os.environ['STAGE']

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/measurement/submit', methods=['POST'])
def submit():
    data = request.get_json()
    dao.Measurement().create(data)
    return data

@app.route('/measurement/fetch/<_id>')
def fetch(_id):
    obj = dao.Measurement().read(_id)
    return obj

@app.route('/measurement/lookup')
def lookup():
    measurement = request.args.get('measurement')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    results = dao.Measurement().lookup(
        measurement, start_time, end_time, page, page_size)
    return {
        'success': True,
        'n_results': len(results),
        'results': results,
    }

@app.route('/measurement/delete/<_id>', methods=['DELETE'])
def delete(_id):
    dao.Measurement().delete(_id)
    return {
        'success': True,
    }

@app.route('/dev/load_mock_data')
def load_mock_data():
    mock_data = dev.get_mock_data()
    for document in mock_data:
        try:
            dao.Measurement().create(document)
        except: pass  # ignore duplicate key error
    return 'Done'

@app.route('/dev/drop_table')
def drop_table():
    for document in dao.Measurement().lookup(page_size=-1):
        dao.Measurement().delete(document['_id'])
    return 'Done'
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

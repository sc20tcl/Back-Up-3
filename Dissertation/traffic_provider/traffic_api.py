from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load CSV data into DataFrame
data = pd.read_csv("ValidateData.csv", parse_dates=['period'], index_col='period')

# Initialize a counter to keep track of the row index
counter = 0

@app.route('/traffic', methods=['GET'])
def get_traffic():
    global counter
    try:
        result = data.iloc[counter]
        counter += 1  # Increment the counter to the next row
        return jsonify({'traffic': result['count'].item()}), 200
    except IndexError:
        return jsonify({'error': 'No more data available'}), 404

@app.route('/set', methods=['POST'])
def set_counter():
    global counter
    timestamp = request.json.get('timestamp')  # Get timestamp from the POST request body
    if not timestamp:
        return jsonify({'error': 'Missing timestamp'}), 400
    
    try:
        # Convert the timestamp string to datetime and find the corresponding index
        datetime_index = pd.to_datetime(timestamp)
        if datetime_index in data.index:
            counter = data.index.get_loc(datetime_index)
            return jsonify({'status': 'Counter set to index of {}'.format(datetime_index)}), 200
        else:
            return jsonify({'error': 'Timestamp not found in data'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

from flask import Flask, request, jsonify
import numpy as np
# import tensorflow as tf
from tensorflow.keras.models import load_model
from joblib import load

app = Flask(__name__)

model = load_model('lstm_model.keras')
scaler = load('scaler.joblib')

traffic_history = []

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    new_value = data['current_traffic']

    if len(traffic_history) >= 15:
        traffic_history.pop(0)  
    traffic_history.append(new_value)
    
    if len(traffic_history) < 15:
        return jsonify({'error': 'Insufficient data. Need 15 numbers, have {}'.format(len(traffic_history))}), 400
    
    current_sequence = np.array(traffic_history).reshape(-1, 1)
    current_sequence_scaled = scaler.transform(current_sequence)
    input_sequence = current_sequence_scaled.reshape((1, 15, 1))
    
    predicted_rpm_scaled = model.predict(input_sequence)
    predicted_rpm = scaler.inverse_transform(predicted_rpm_scaled)
    
    return jsonify({'forecast': predicted_rpm.flatten().tolist()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

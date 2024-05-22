from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/optimum_pods', methods=['GET'])
def optimum_pods():
    qps = request.args.get('qps', type=float)
    
    if qps is None:
        return jsonify({'error': 'Missing qps parameter'}), 400
    
    # Calculate the optimum number of pods using the polynomial formula
    intercept = 1.66
    coef1 = 0.00148257
    coef2 = 0.00001051
    
    pods = round(intercept + coef1 * qps + coef2 * qps**2)
    
    return jsonify({'qps': qps, 'optimum_pods': pods})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
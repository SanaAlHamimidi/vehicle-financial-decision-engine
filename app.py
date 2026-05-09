from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# load model and encoders
model = joblib.load('xgboost_model.pkl')
label_encoders = joblib.load('label_encoders.pkl')
demand_lookup = pd.read_csv('demand_lookup.csv')

def get_demand_score(region, manufacturer, fuel):
    match = demand_lookup[
        (demand_lookup['region'] == region) &
        (demand_lookup['make'] == manufacturer) &
        (demand_lookup['fuel'] == fuel)
    ]
    return float(match['demand_score'].values[0]) if len(match) > 0 else 0.0

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    region = data['region']
    manufacturer = data['manufacturer']
    year = int(data['year'])
    odometer = float(data['odometer'])
    condition = data['condition']
    fuel = data['fuel']
    vehicle_type = data['type']

    fuel_map = {
        'gas': 'gasoline',
        'diesel': 'diesel and diesel hybrid',
        'electric': 'battery electric',
        'hybrid': 'hybrid gasoline',
        'other': 'other'
    }
    fuel_lookup = fuel_map.get(fuel, fuel)
    
    demand_score = get_demand_score(region, manufacturer, fuel_lookup)
    
    region_encoded = label_encoders['region'].transform([region])[0]
    manufacturer_encoded = label_encoders['manufacturer'].transform([manufacturer])[0]
    condition_encoded = label_encoders['condition'].transform([condition])[0]
    fuel_encoded = label_encoders['fuel'].transform([fuel])[0]
    type_encoded = label_encoders['type'].transform([vehicle_type])[0]
    
    features = np.array([[
        region_encoded,
        year,
        manufacturer_encoded,
        condition_encoded,
        fuel_encoded,
        odometer,
        type_encoded,
        demand_score
    ]])
    
    predicted_price = model.predict(features)[0]
    
    return jsonify({
        'predicted_price': round(float(predicted_price), 2),
        'demand_score': round(demand_score, 4)
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
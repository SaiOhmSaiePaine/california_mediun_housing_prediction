import os
import pickle
from pathlib import Path

from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
FEATURE_COLUMNS = [
    'MedInc',
    'HouseAge',
    'AveRooms',
    'AveBedrms',
    'Population',
    'AveOccup',
    'Latitude',
    'Longitude',
]

# Load model artifacts using absolute paths so startup is robust across working directories.
with open(BASE_DIR / 'randomforest.pkl', 'rb') as model_file:
    randomforestmodel = pickle.load(model_file)

with open(BASE_DIR / 'scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)


def _coerce_feature_frame(raw_data):
    missing_fields = [name for name in FEATURE_COLUMNS if name not in raw_data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    try:
        row = [float(raw_data[name]) for name in FEATURE_COLUMNS]
    except (TypeError, ValueError) as exc:
        raise ValueError('All fields must be numeric.') from exc

    return pd.DataFrame([row], columns=FEATURE_COLUMNS)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict_api', methods=['POST'])
def predict_api():
    payload = request.get_json(silent=True) or {}
    data = payload.get('data')
    if not isinstance(data, dict):
        return jsonify({'error': "Request body must include a 'data' object."}), 400

    try:
        feature_frame = _coerce_feature_frame(data)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    scaled_data = scaler.transform(feature_frame)
    output = float(randomforestmodel.predict(scaled_data)[0])
    return jsonify(output)


@app.route('/predict', methods=['POST'])
def predict():
    form_data = {name: request.form.get(name) for name in FEATURE_COLUMNS}

    try:
        feature_frame = _coerce_feature_frame(form_data)
    except ValueError as exc:
        return render_template('home.html', prediction_text=f'Invalid input: {exc}')

    final_input = scaler.transform(feature_frame)
    output = float(randomforestmodel.predict(final_input)[0])
    return render_template("home.html", prediction_text='The predicted price of the house is ${:,.2f}'.format(output))


if __name__ == "__main__":
    port = int(os.getenv('PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', '0') == '1')
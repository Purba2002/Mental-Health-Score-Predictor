import joblib  # or import pickle
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Prevents cross-origin browser blocking

# 1. Load your saved machine learning model
model = joblib.load('model.pkl')  # Update with your model's actual filename


# 2. Serve your main frontend HTML page
@app.route('/')
def home():
    return render_template('index.html')  # Ensures backend serves index.html


# 3. Your /predict route code
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)

        age = int(data.get('age', 0))
        screen_time = float(data.get('screen_time', 0))
        unlocks = int(data.get('unlocks', 0))
        study_hours = float(data.get('study_hours', 0))
        sleep = float(data.get('sleep', 0))

        gender = 1 if data.get('gender') == 'Male' else 0

        stress_mapping = {
            'Low': 0,
            'Medium': 1,
            'High': 2,
            'Very High': 3,
        }
        stress = stress_mapping.get(data.get('stress'), 1)

        features = [
            [age, gender, screen_time, unlocks, study_hours, sleep, stress]
        ]
        prediction = model.predict(features)[0]

        return (
            jsonify({'success': True, 'prediction': float(prediction)}),
            200,
        )

    except Exception as e:
        print(f'Error during prediction: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
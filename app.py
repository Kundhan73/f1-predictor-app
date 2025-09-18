from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  

DATA_FILE = 'f1_race_data.json' 

@app.route('/api/racedata', methods=['GET'])
def get_race_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Data file 'f1_race_data.json' not found in the project folder."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid data file. Please check the JSON format."}), 500

@app.route('/api/predict', methods=['POST'])
def predict_winner():
    data = request.get_json()
    selected_track = data.get('track')

    if not selected_track:
        return jsonify({"error": "Track not specified"}), 400

    try:
        with open(DATA_FILE, 'r') as f:
            races = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    
    
    driver_scores = {}
    
    
    track_races = [r for r in races if r.get('raceName') == selected_track]

    for race in races:
        
        winner = race.get('winnerDriver')
        season = int(race.get('season', '2010'))

        if not winner:
            continue 
        driver_scores.setdefault(winner, {'total': 0, 'track_wins': 0})
        
        
        recency_bonus = (season - 2009) * 0.1
        
        
        driver_scores[winner]['total'] += (1 + recency_bonus)

    
    for race in track_races:
        winner = race.get('winnerDriver')
        if winner in driver_scores:
            driver_scores[winner]['total'] += 3 
            driver_scores[winner]['track_wins'] += 1
    
    if not driver_scores:
        return jsonify({"winner": "N/A", "analysis": "No historical data for this track."})

    
    predicted_winner = max(driver_scores, key=lambda d: driver_scores[d]['total'])
    winner_stats = driver_scores[predicted_winner]

    
    analysis = (
        f"Prediction for {predicted_winner} is based on a high performance score, "
        f"factoring in strong recency weighting and {winner_stats['track_wins']} previous win(s) at this Grand Prix."
    )

    return jsonify({"winner": predicted_winner, "analysis": analysis})

if __name__ == '__main__':
    app.run(debug=True, port=5001)


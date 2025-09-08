from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Allow requests from your HTML file

DATA_FILE = 'f1_race_data.json' # The server will look for this file

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
    
    # --- Updated Prediction Logic ---
    driver_scores = {}
    
    # Filter races for the selected track using the new 'raceName' key
    track_races = [r for r in races if r.get('raceName') == selected_track]

    for race in races:
        # Use the new keys from your JSON file
        winner = race.get('winnerDriver')
        season = int(race.get('season', '2010'))

        if not winner:
            continue # Skip if there's no winner data for a row

        driver_scores.setdefault(winner, {'total': 0, 'track_wins': 0})
        
        # Recency bonus based on 'season'
        recency_bonus = (season - 2009) * 0.1
        
        # Base score for any win
        driver_scores[winner]['total'] += (1 + recency_bonus)

    # Track-specific bonus
    for race in track_races:
        winner = race.get('winnerDriver')
        if winner in driver_scores:
            driver_scores[winner]['total'] += 3 # Significant bonus for winning at this specific track
            driver_scores[winner]['track_wins'] += 1
    
    if not driver_scores:
        return jsonify({"winner": "N/A", "analysis": "No historical data for this track."})

    # Find the winner
    predicted_winner = max(driver_scores, key=lambda d: driver_scores[d]['total'])
    winner_stats = driver_scores[predicted_winner]

    # Updated analysis text
    analysis = (
        f"Prediction for {predicted_winner} is based on a high performance score, "
        f"factoring in strong recency weighting and {winner_stats['track_wins']} previous win(s) at this Grand Prix."
    )

    return jsonify({"winner": predicted_winner, "analysis": analysis})

if __name__ == '__main__':
    app.run(debug=True, port=5001)


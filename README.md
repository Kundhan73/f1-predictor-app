F1 Race Winner Predictor
A sleek, self-contained web application that predicts Formula 1 race winners based on historical data. This project uses a Python Flask backend to serve the data and prediction logic, and a vanilla HTML/CSS/JavaScript frontend for the user interface.

This version reads from a local f1_race_data.json file, making it fast, reliable, and independent of external websites.

Features
Local Data Source: Reads all race data from a local f1_race_data.json file.

Advanced Prediction Algorithm: Calculates a winner based on a scoring system that factors in track history, driver momentum, and recency of wins.

Clean, F1-Themed UI: A modern and responsive interface built with Tailwind CSS.

Lightweight Backend: A simple and efficient Flask server to handle API requests.

Prerequisites
Python 3.6+

pip for installing packages

A virtual environment tool like venv (recommended)

How to Run This Project
1. Setup
Download Files: Place all project files (app.py, index.html, requirements.txt) into a single folder.

Provide Race Data: Create or place your own race data file in the same folder. It must be named f1_race_data.json. The file should be an array of JSON objects, with each object having keys like "raceName", "winnerDriver", and "season".

Create a Virtual Environment: Open your terminal in the project folder and run:

# Create the environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

Install Dependencies: Install the required Python packages.

pip install -r requirements.txt

2. Running the Application
Start the Backend Server: With your virtual environment still active, run:

python app.py

Your terminal will show that the server is running on http://127.0.0.1:5001. Leave this terminal window open.

Open the Frontend: In your file explorer, find and open the index.html file in your web browser.

The application will load, and you can now select a Grand Prix to get a prediction!
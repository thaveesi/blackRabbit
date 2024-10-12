# Flask App

This is a simple Flask application set up using Rye.

## Setup

1. Make sure you have Rye installed.
2. Clone this repository.
3. Navigate to the project directory.
4. Run `rye sync` to install dependencies.

## Running the app

1. Activate the virtual environment:
   ```
   rye shell
   ```
2. Run the Flask app:
   ```
   python src/app.py
   ```
3. Open your browser and go to `http://localhost:5000` to see the app running.

## Environment Variables

Make sure to set up your `.env` file with the necessary environment variables:

- MONGODB_URL
- MONGODB_PASSWORD
- KINDO_API_KEY
- FLASK_SECRET_KEY

from flask import Flask, render_template
import requests

# Create the Flask app
app = Flask(__name__)

# API details
api_url = "https://api.cricapi.com/v1/currentMatches"
api_key = "2b50724f-4f36-43ee-93aa-2d6850898612"

# Function to fetch cricket data from API
def fetch_cricket_data():
    params = {
        "apikey": api_key
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Route for the home page
@app.route('/')
def index():
    data = fetch_cricket_data()
    matches = []

    if data and "data" in data:
        for match in data["data"]:
            match_info = {
                "name": match.get("name", ""),
                "matchType": match.get("matchType", ""),
                "status": match.get("status", ""),
                "venue": match.get("venue", ""),
                "teams": " vs ".join(match.get("teams", [])),
                "score": format_score(match.get("score", "")),
            }

            # Handling teamInfo if available
            if "teamInfo" in match:
                team_info = match["teamInfo"]
                match_info["team_1"] = team_info[0].get("name", "N/A")
                match_info["team_2"] = team_info[1].get("name", "N/A")
                match_info["team_1_img"] = team_info[0].get("img", "")
                match_info["team_2_img"] = team_info[1].get("img", "")
            else:
                match_info["team_1"] = "N/A"
                match_info["team_2"] = "N/A"
                match_info["team_1_img"] = ""
                match_info["team_2_img"] = ""
            
            matches.append(match_info)

    return render_template('ui.html', matches=matches)

# Function to format the score in a readable way
def format_score(score):
    # Check if score is a list and contains dictionaries
    if isinstance(score, list) and all(isinstance(i, dict) for i in score):
        formatted_score = ", ".join(
            f"{inning['inning']} - {inning['r']} runs, {inning['w']} wickets, {inning['o']} overs"
            for inning in score
        )
        return formatted_score
    return score if score else "Score not available"

if __name__ == '__main__':
    app.run(debug=True)

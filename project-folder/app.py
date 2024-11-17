from flask import Flask, render_template, request
import requests

# Create the Flask app
app = Flask(__name__)

# API details for cricket data
api_url = "https://api.cricapi.com/v1/currentMatches"
api_key = "2b50724f-4f36-43ee-93aa-2d6850898612"

# Function to fetch cricket data from the API
def fetch_cricket_data():
    params = {
        "apikey": api_key
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON data if the request is successful
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None  # Return None if an error occurs

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
            if "teamInfo" in match and len(match["teamInfo"]) >= 2:
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

# Route for the Series List page
@app.route('/series')
def series():
    return render_template('serieslist.html')

# Route for the Player List page
@app.route('/player-list')
def player_list():
    # Player API URL
    player_api_url = "https://api.cricapi.com/v1/players"
    params = {
        "apikey": "afdeb337-f767-4c92-92db-c0240dac575b",  # Your API key
        "offset": 0  # Set the offset for pagination if needed
    }

    players = []

    try:
        response = requests.get(player_api_url, params=params)
        response.raise_for_status()  # Raise error for bad responses
        data = response.json()

        # Check if player data exists in the response
        if data and "data" in data:
            players = data["data"]  # Assuming 'data' contains player info
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player data: {e}")

    return render_template('playerlist.html', players=players)

# Route for the Player Search page
@app.route('/player-search', methods=['GET', 'POST'])
def player_search():
    query = request.form.get('query', '')  # Get the search query from the form
    players = []

    if query:
        player_api_url = "https://api.cricapi.com/v1/players"
        params = {
            "apikey": "afdeb337-f767-4c92-92db-c0240dac575b",  # Your API key
            "query": query,  # Use the query to search players
        }

        try:
            response = requests.get(player_api_url, params=params)
            response.raise_for_status()  # Raise error for bad responses
            data = response.json()

            # Check if player data exists in the response
            if data and "data" in data:
                players = data["data"]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching player data: {e}")

    return render_template('playersearch.html', players=players)

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

// scriptplaylist.js

// API details for fetching players
const apiUrl = "https://api.cricapi.com/v1/players";
const apiKey = "afdeb337-f767-4c92-92db-c0240dac575b";

// Fetch player data from the API
function fetchPlayerData() {
    fetch(`${apiUrl}?apikey=${apiKey}`)
        .then(response => response.json())
        .then(data => {
            if (data && data.data) {
                displayPlayers(data.data);
            } else {
                document.getElementById("player-list").innerHTML = "No players available";
            }
        })
        .catch(error => {
            console.error('Error fetching player data:', error);
            document.getElementById("player-list").innerHTML = "Failed to load player data.";
        });
}

// Function to display players in the UI
function displayPlayers(players) {
    const playerList = document.getElementById("player-list");
    playerList.innerHTML = ""; // Clear any existing content

    players.forEach(player => {
        const playerItem = document.createElement("div");
        playerItem.classList.add("player-item");
        playerItem.innerHTML = `
            <div class="player-name">${player.name}</div>
            <div class="player-country">${player.country}</div>
        `;
        playerList.appendChild(playerItem);
    });
}

// Call fetchPlayerData on page load
document.addEventListener("DOMContentLoaded", fetchPlayerData);

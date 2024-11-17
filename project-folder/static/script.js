document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = "https://api.cricapi.com/v1/series?apikey=afdeb337-f767-4c92-92db-c0240dac575b&offset=0";
    const seriesContainer = document.getElementById('series-container');

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const series = data.data;

            series.forEach(item => {
                const card = document.createElement('div');
                card.classList.add('card');

                card.innerHTML = `
                    <div class="card-body">
                        <h3>${item.name}</h3>
                        <p><strong>Start Date:</strong> ${item.startDate}</p>
                        <p><strong>End Date:</strong> ${item.endDate}</p>
                        <p><strong>Matches:</strong> ${item.matches}</p>
                        <p><strong>ODIs:</strong> ${item.odi}</p>
                        <p><strong>T20s:</strong> ${item.t20}</p>
                        <p><strong>Tests:</strong> ${item.test}</p>
                    </div>
                `;

                seriesContainer.appendChild(card);
            });
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
});

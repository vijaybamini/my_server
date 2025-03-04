
async function fetchFlaskData() {
    try {
        const response = await fetch("/get-data");  // Flask endpoint
        const data = await response.json();
        
        if (data.distance) {
            document.getElementById("sensorData").innerText = `Distance: ${data.distance} cm`;
        } else {
            document.getElementById("sensorData").innerText = "No distance data available";
        }
    } catch (error) {
        console.error("Error fetching from Flask:", error);
        document.getElementById("sensorData").innerText = "Error fetching data";
    }
}

// ✅ Fetch from Flask every 5 seconds
setInterval(fetchFlaskData, 5000);

// ✅ Fetch data when page loads
fetchFlaskData();

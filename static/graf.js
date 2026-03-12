/**
 * Dashboard Frontend JavaScript
 *
 * Handles all interactive functionality on the temperature dashboard page:
 * - Fetching and displaying the most recent temperature reading
 * - Populating the temperature data table with configurable record count
 * - Rendering a Chart.js line chart of temperature over time
 * - Responding to slider input to adjust how many data points are shown
 * - Re-rendering the chart on window resize for responsiveness
 *
 * All data is fetched asynchronously from the Flask REST API endpoints.
 */

/**
 * Initialize the dashboard when the DOM is fully loaded.
 * Draws the chart, populates the table, shows the latest temperature,
 * and attaches event listeners to the data count slider.
 */
document.addEventListener("DOMContentLoaded", function() {
    editGraph();
    updateTable()
    changeLastTemp()
    document.getElementById("dataCountSlider").addEventListener("input", editGraph)
    document.getElementById("dataCountSlider").addEventListener("input", updateTable);
    document.getElementById("dataCountSlider").addEventListener("input", changeLastTemp)
    // document.getElementById("data_delete_button").addEventListener("click",delete_data)
})

/** Re-render the chart when the browser window is resized. */
window.addEventListener("resize",editGraph)


/**
 * Fetches the most recent temperature reading from the API and updates
 * the "last_temp" element on the page with the timestamp and value.
 */
async function changeLastTemp(){
    var response= await fetch(`http://127.0.0.1:5000/api/last_data_value`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then()
    var data=await response.json()
    console.log(data.timestamp)
    document.getElementById("last_temp").innerHTML="Last measuring was at "+ data.timestamp+" with value "+ data.temp +" °C"
}


/**
 * Fetches temperature records from the API. The number of records returned
 * is controlled by the value of the "dataCountSlider" input element.
 *
 * @returns {Promise<Array>} Array of objects with 'temp' and 'timestamp' fields.
 */
async function getData() {
    const dataCount = document.getElementById("dataCountSlider").value
    let data= await fetch(`http://127.0.0.1:5000/api/data?count=${dataCount}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then()
    return data.json()
}

// function delete_data(e){
//     e.preventF
// }


/**
 * Fetches temperature data and populates the HTML table on the dashboard.
 * The data is displayed in reverse chronological order (newest first).
 * Each row shows a row number, timestamp, and temperature value.
 */
async function updateTable() {
    var values=await getData()
    values.reverse()
    const dataCount = document.getElementById("dataCountSlider").value
    const tableBody = document.getElementById("tableBody");
    const tableContent = [];
    tableBody.innerHTML=''
     for (let i = 0; i < dataCount; i++) {
        const t = values[i];
        if(t!=null){
            const newRow = tableBody.insertRow();
            newRow.insertCell().textContent = i + 1; // Row number
            newRow.insertCell().textContent = t.timestamp; // Timestamp
            newRow.insertCell().textContent = t.temp; // Temperature
        }
    }

    document.getElementById("dataCountValue").textContent = dataCount;
}

/**
 * Fetches temperature data and renders a Chart.js line chart on the dashboard.
 * The X-axis shows timestamps and the Y-axis shows temperature values in Celsius.
 * Also updates the displayed data count value from the slider.
 */
async function editGraph() {
    var ctxL = document.getElementById("lineChart").getContext('2d');
    var values= await getData();
    const timestamps = values.map(item => item.timestamp);
    const temperatures = values.map(item => item.temp);

    var myLineChart = new Chart(ctxL, {
        type: 'line',
        data: {
            labels: timestamps,
            datasets: [{
                label: "Temperature",
                data: temperatures,
                backgroundColor: [
                    'rgba(105, 0, 132, .2)',
                ],
                borderColor: [
                    'rgba(200, 99, 132, .7)',
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true
        }
    });

document.getElementById("dataCountValue").textContent = document.getElementById("dataCountSlider").value;
}


document.addEventListener("DOMContentLoaded", function() {
    editGraph();
    updateTable()
    changeLastTemp()
    document.getElementById("dataCountSlider").addEventListener("input", editGraph)
    document.getElementById("dataCountSlider").addEventListener("input", updateTable);
    document.getElementById("dataCountSlider").addEventListener("input", changeLastTemp)
    // document.getElementById("data_delete_button").addEventListener("click",delete_data)
})
window.addEventListener("resize",editGraph)



async function changeLastTemp(){
    var response= await fetch(`http://127.0.0.1:5000/api/last_data_value`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then()
    data=await response.json()
    document.getElementById("last_temp").innerHTML="Last measuring was at "+ data.timestamp+" with value "+ data.temp +" °C"
}



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
            newRow.insertCell().textContent = i + 1; // Číslo řádku
            newRow.insertCell().textContent = t.timestamp; // Timestamp
            newRow.insertCell().textContent = t.temp; // Teplota
        }
    }

    document.getElementById("dataCountValue").textContent = dataCount;
}

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

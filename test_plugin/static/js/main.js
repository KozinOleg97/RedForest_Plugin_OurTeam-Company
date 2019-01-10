var chartData = {
    labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",], //["January", "February", "March", "April", "May", "June"],
    datasets: [
        {
            fillColor: "#79D1CF",
            strokeColor: "#d127a9",
            data: JSON.parse(appData.budget_data)
        }
    ]
};
var ctx = document.getElementById("myChart1").getContext("2d");
var myBar1 = new Chart(ctx, {
    type: 'bar',
    data: chartData
});



var chartData = {
    labels: (appData.users_labels).split(","),
    datasets: [
        {
            fillColor:"#00ff13",
            data: JSON.parse(appData.users_data)
        }
    ]
};
var ctx = document.getElementById("myChart2").getContext("2d");
var myBar2 = new Chart(ctx, {
    type: 'doughnut',
    data: chartData
});
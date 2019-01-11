//======budgetChart==================================================
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
var budgetChart = new Chart(ctx, {
    type: 'bar',
    data: chartData
});

//======UsersRolesChart==================================================
var chartData = {
    labels: (appData.users_labels).replace(/&#39;/g, "").slice(1,-1).split(","),
    datasets: [
        {
            fillColor:"#00ff13",
            data: JSON.parse(appData.users_data)
        }
    ]
};
var ctx = document.getElementById("myChart2").getContext("2d");
var UsersRolesChart = new Chart(ctx, {
    type: 'doughnut',
    data: chartData
});

//======UsersNumberChart==================================================
var chartData = {
    labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",],
    datasets: [
        {
            fillColor:"#00ff13",
            data: JSON.parse(appData.users_numbers)
        }
    ]
};
var ctx = document.getElementById("myChart3").getContext("2d");
var UsersNumberChart = new Chart(ctx, {
    type: 'line',
    data: chartData
});
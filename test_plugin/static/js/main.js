var chartData = {
    labels: ["January", "February", "March", "April", "May", "June"],
    datasets: [
        {
            fillColor: "#79D1CF",
            strokeColor: "#79D1CF",
            data: appData.budget_data
        }
    ]
};
var ctx = document.getElementById("myChart1").getContext("2d");
var myBar = new Chart(ctx, {
    type: 'bar',
    data: chartData
});
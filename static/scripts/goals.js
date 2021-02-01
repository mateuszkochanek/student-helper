let goals_achieved_amount = parseInt(document.getElementById("goals_achieved_amount").value);
let goals_not_achieved_amount = parseInt(document.getElementById("goals_not_achieved_amount").value);
let goals_expired_amount = parseInt(document.getElementById("goals_expired_amount").value);

window.onload = function() {
    areGoalsToShow() ? createChart() : hideChart();
};

let mainChartConfig = {
    type: 'pie',
    data: {
        datasets: [{
            data: [goals_not_achieved_amount, goals_achieved_amount, goals_expired_amount],
            backgroundColor: ['#9bdcfa', '#5b80b2', '#123456']
        }],
        labels: ['w trakcie', 'osiagniete', 'przedawnione']
    },
    options: {
        responsive: true
    }
};

function areGoalsToShow() {
    return goals_achieved_amount + goals_not_achieved_amount + goals_expired_amount !== 0;
}

function createChart() {
    let ctx = document.getElementById('mainChart').getContext('2d');
    window.myPie = new Chart(ctx, mainChartConfig);
}

function hideChart() {
    document.getElementById('chart_div').style.visibility = 'hidden';
}

let goals_achieved_amount = document.getElementById("goals_achieved_amount").value;
let goals_not_achieved_amount = document.getElementById("goals_not_achieved_amount").value;

let mainChartConfig = {
    type: 'pie',
    data: {
        datasets: [{
            data: [goals_not_achieved_amount, goals_achieved_amount],
            backgroundColor: ['#9bdcfa', '#5b80b2']
        }],
        labels: ['w trakcie', 'osiagniete']
    },
    options: {
        responsive: true
    }
};

window.onload = function() {
    let ctx = document.getElementById('mainChart').getContext('2d');
    window.myPie = new Chart(ctx, mainChartConfig);
};

function createDaysChart(daysInSemester, daysToEndOfSemester) {
    let ctx = document.getElementById('daysChart').getContext('2d');
    let daysChart = new Chart(ctx, {
        type: 'pie',
        data: {
            datasets: [{
                data: [daysInSemester - daysToEndOfSemester, daysToEndOfSemester],
                backgroundColor: ['#9bdcfa', '#5b80b2']
            }],
            labels: ['dni za nami', 'pozostałe dni']
        },
        options: {
            responsive: true
        }
    });
}

function createSpendTimeChart(courseNames, timeSpendOnCourses) {
    console.log(courseNames)
    let ctx = document.getElementById('spendTimeChart').getContext('2d');
    let spendTime = new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                data: timeSpendOnCourses,
                borderWidth: 1,
                borderColor: ['#5b80b2']
            }],
            labels: courseNames
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

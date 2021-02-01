function createDaysChart(daysInSemester, daysToEndOfSemester) {
    let ctx = document.getElementById('chart').getContext('2d');
    let chart = new Chart(ctx, {
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
    let ctx = document.getElementById('chart').getContext('2d');
    let chart = new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                data: timeSpendOnCourses,
                borderWidth: 1,
                backgroundColor: '#5b80b2'
            }],
            labels: courseNames
        },
        options: {
            legend: {
                display: false
             },
             tooltips: {
                enabled: false
             },
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

function createRatiosChart(courseNames, ratios) {
    let ctx = document.getElementById('chart').getContext('2d');
    let chart = new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                data: ratios,
                borderWidth: 1,
                backgroundColor: '#5b80b2'
            }],
            labels: courseNames
        },
        options: {
            legend: {
                display: false
             },
             tooltips: {
                enabled: false
             },
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

function createFormsChart(forms, times) {
    let ctx = document.getElementById('chart').getContext('2d');
    let chart = new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                data: ratios,
                borderWidth: 1,
                backgroundColor: '#5b80b2'
            }],
            labels: times
        },
        options: {
            legend: {
                display: false
             },
             tooltips: {
                enabled: false
             },
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

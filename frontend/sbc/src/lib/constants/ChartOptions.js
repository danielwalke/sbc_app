export const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: false,
            position: 'top',
            labels: {
                color: 'white', // Set font color for legend labels
            },
        },
    },
    scales: {
        x: {
            ticks: {
                color: 'white', // Set font color for x-axis labels
            },
            grid: {
                color: 'rgba(255,255,255, 0.3)', // Set font color for x-axis grid lines
            },
        },
        y: {
            beginAtZero: true,
            ticks: {
                color: 'white', // Set font color for y-axis labels
            },
            grid: {
                color: 'rgba(255,255,255, 0.3)', // Set font color for x-axis grid lines
            },
            /*min: -1,
            max: 1*/
        },
    },
}

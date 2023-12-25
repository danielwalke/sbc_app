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
        title: {
            display: true,
            text: 'SHAP-values',
            font: {
                size: 14, // Set font size for the title
                weight: 'bold',
            },
            color: 'white', // Set font color for the title
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
        },
    },
}
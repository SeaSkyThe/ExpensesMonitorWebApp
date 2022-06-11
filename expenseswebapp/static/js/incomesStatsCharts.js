var textColor = getComputedStyle(document.documentElement)
.getPropertyValue('--chart-text-color');

const renderChart = (data, labels) => {
    const ctx = document.getElementById('myChart').getContext('2d');
    ctx.canvas.width  = window.innerWidth;
    ctx.canvas.style.marginTop = '3%';
    ctx.canvas.height = document.querySelector('.home').clientHeight;
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Last 6 months',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.35)',
                    'rgba(54, 162, 235, 0.35)',
                    'rgba(255, 206, 86, 0.35)',
                    'rgba(75, 192, 192, 0.35)',
                    'rgba(153, 102, 255, 0.35)',
                    'rgba(255, 159, 64, 0.35)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x:{
                    beginAtZero: true,
                },
                y: {
                    beginAtZero: true,
                    
                }
            },
            plugins: {
                legend:{
                    display: false
                },
                title:{
                    display: true,
                    text: 'Incomes in the last 6 months',
                    padding: {
                        top: 10,
                        bottom: 30
                    },
                    font: {
                        family: 'sans-serif',
                        size: 15,
                    }

                }
            },
           
            
        }
    });
}

const getChartData = () =>{
    fetch('/income/incomes_source_summary').then(res=>res.json()).then(results=>{
        console.log('results', results)
        var source_data = results.income_source_data; 
        var [labels, data] = [Object.keys(source_data), Object.values(source_data)] 
        renderChart(data, labels);
    })
}
document.onload=getChartData();

<script>
    import { Pie } from 'svelte-chartjs';
    import ChartDataLabels from 'chartjs-plugin-datalabels'
  
    import {
      Chart,
      Title,
      Tooltip,
      Legend,
      ArcElement,
      CategoryScale,
    } from 'chart.js';
  
    Chart.register(Title, Tooltip, Legend, ArcElement, CategoryScale, ChartDataLabels);

    export let labels = []
    export let chartData = []

  </script>
  
  <Pie data={{
    labels,
    datasets: [
    {
      data: chartData,
      backgroundColor: [
        '#F7464A',
        '#FDB45C',
        '#67c952',
      ],
    },
  ],
}}
options={{
    responsive:true,
    plugins:{
        datalabels:{
            color: '#FFF',
            formatter: ((value,ctx)=>{
                const totalSum = ctx.dataset.data.reduce((acc, current)=>{
                    return acc+current
                }, 0)
                const percentage = value/totalSum*100
                return `${percentage.toFixed(2)}%`
            })
        },
        legend:{
            position:'bottom'
        }
    },
    layout:{
        padding: 5
    },
    events:[]
}}
plugins={[ChartDataLabels]}
/>
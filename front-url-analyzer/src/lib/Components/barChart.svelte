<script>
    import { Bar } from 'svelte-chartjs'
    import {
    Chart,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
  } from 'chart.js';
  Chart.register(
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
  );
    export let labels = []
    export let chartData = []
    export let label = ''

    export let barColor1 = ''
    export let barColor2 = ''
    export let barColor3 = ''

</script>
<Bar data={{
    labels,
    datasets: [
    {
      label: label,
      data: chartData,
      backgroundColor: [
        barColor1 || '#F7464A',
        barColor2 || '#FDB45C',
        barColor3 ||'#67c952',
      ],
      borderWidth: 2,
      borderColor: [
        barColor1 || '#F7464A',
        barColor2 || '#FDB45C',
        barColor3 || '#67c952',
      ],
    },
  ]
}}

options={{
  responsive:true,
  plugins:{
      datalabels:{
          color: '#FFF',
      },
      legend:{
        position:'bottom'
      }
  },
  layout:{
      padding: 5
  },
  events:[]
}} />
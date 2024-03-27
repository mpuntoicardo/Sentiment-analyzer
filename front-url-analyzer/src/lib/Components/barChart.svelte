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



</script>
<Bar data={{
    labels,
    datasets: [
    {
      label: label,
      data: chartData,
      backgroundColor: [
        'rgba(255, 134,159)',
        'rgba(98,  182, 239)',
        'rgba(255, 218, 128)',
      ],
      borderWidth: 2,
      borderColor: [
        'rgba(255, 134, 159, 1)',
        'rgba(98,  182, 239, 1)',
        'rgba(255, 218, 128, 1)',
      ],
    },
  ]
}}
/>
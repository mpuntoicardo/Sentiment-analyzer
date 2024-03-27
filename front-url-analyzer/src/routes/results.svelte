<script>
        import BarChart from '../lib/Components/barChart.svelte';
        import { store } from './store.js'

       
</script>

<section>
    <h1>Search results:</h1>
    <p>{$store.summary}</p>
    <h2>Global results</h2>
    <BarChart labels={Object.keys($store.globalResults)} label='Phrases count' chartData={Object.values($store.globalResults)}/>
</section>
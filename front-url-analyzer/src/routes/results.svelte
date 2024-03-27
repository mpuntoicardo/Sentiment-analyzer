<script>
        import BarChart from '../lib/Components/barChart.svelte';
        import PieChart from '../lib/Components/pieChart.svelte';
        import { store } from './store.js'

       
</script>

<section id='results-section'>
    <div class="p-10">
        <div class="flex flex-col items-center gap-y-2">
            <h1 class="text-5xl">Search results</h1>
            <div class="w-4/12 flex justify-center">
                <PieChart labels={Object.keys($store.globalResults)} chartData={Object.values($store.globalResults)}/>
            </div>
            <div class="p-3">
                <h2>The most repeated sentyment throughout the urls is: <b>{$store.overallSent}</b></h2>
            </div>
        </div>
        <div class="px-9">
            <p class="summary pt-4"><b>Content summary:</b> {$store.summary}</p>
        </div>
    </div>
    <div class="w-full p-10 flex justify-center">
            <div class>
                <div>
                    <h2>Overall result:</h2>
                    <p></p>
                </div>
                <BarChart labels={Object.keys($store.globalResults)} label='Phrases count' chartData={Object.values($store.globalResults)}/>
            </div>
    </div>
</section>

<style>
    .summary {
        text-align: justify;
        text-justify: inter-word;
    }
</style>
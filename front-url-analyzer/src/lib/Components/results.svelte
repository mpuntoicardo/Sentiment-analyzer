<script>
        import BarChart from '$lib/Components/barChart.svelte';
        import ErrorMessage from './errorMessage.svelte';
        import PieChart from './pieChart.svelte';
        import ErrorResult from '../../routes/errorResult.svelte';
        import { store } from '../../routes/store.js'
        import { scale } from "svelte/transition";

        let showFailedUrls = false

        function handeleShowFailedUrls(){
            showFailedUrls = !showFailedUrls
        }

</script>

<section id='results-section'>
    {#if $store.overallSent}
        <div class="md:p-10 pt-10 pb-5">
            <div class="flex flex-col items-center gap-y-2">
                <h1 class="text-5xl text-center">Search results</h1>
                <div class="md:w-4/12 flex justify-center">
                    <PieChart labels={Object.keys($store.globalResults)} chartData={Object.values($store.globalResults)}/>
                </div>
                <div class="md:p-3 px-5">
                    <p>The most repeated sentiment throughout the phrases in the urls is: <b>{$store.overallSent}</b><p>
                </div>
                {#if $store.failedUrls.length > 0}
                    <ErrorMessage msg={'Failed to retrieve info from ' + $store.failedUrls.length + " " + ($store.failedUrls.length > 1? "urls" : "url")}></ErrorMessage>
                    <button class="bg-red-600 text-white rounded-full p-3 mt-3" on:click={handeleShowFailedUrls}>{showFailedUrls?"Hide": "Show"} url{$store.failedUrls.length == 1? "":"s"}<i class={"fa-solid fa-arrow-down px-2 "+(showFailedUrls? "open":"")}></i></button>
                {/if}
            </div>
        </div>
        {#if showFailedUrls}
            <div class="w-full bg-red-200 flex flex-col items-center justify-center py-3 mt-2 gap-y-3" transition:scale>
                <h2 class="text-3xl">Failed Url{$store.failedUrls.length == 1? "":"s"}:</h2>
                <ol>
                    {#each $store.failedUrls as failedUrl }
                            <li>{failedUrl}</li>
                    {/each}
                </ol>
            </div>
        {/if}
        {#if $store.summary}
        <div class="flex flex-col bg-[#Dde2fd] pb-10 items-center">
            <h2 class="text-3xl pt-10 pb-4">Urls content's summary</h2>
            <div class="md:px-32 px-5">
                <p class="pt-4 summary">{$store.summary}</p>
            </div>
        </div>
        {/if}
        <div class="grid grid-cols-2 pb-10 px-5 md:px-0">
            <div class="col-span-2 pt-10 pb-4">
                <h2 class="text-3xl text-center">In depth results</h2>
            </div>
            <div class="md:pl-32 md:pr-10 pt-4 col-span-2 md:col-span-1">
                <p class="summary">The following bar chart breaks down the frequency of phrases categorized as <b>Negative(Neg), Neutral(Neu) and Positive(Pos)</b> found within the analyzed URLs. Analyzing the distribution of these phrases can help you gain insights into the specific focus you have. This information can be valuable in these examples: e.g., understanding user interest in a particular aspect, identifying areas for improvement in content related to the category, or analyzing the comprehensiveness of the information provided.</p>
            </div>
            <div class="md:pr-32 pt-4 col-span-2 md:col-span-1">
                <BarChart labels={Object.keys($store.globalResults)} label='Phrases count' chartData={Object.values($store.globalResults)}/>
            </div>
        </div>
        <div class="grid grid-cols-2 pb-10 bg-[#Dde2fd] px-5 md:px-0">
            <div class="col-span-2 pt-10 pb-4 order-first">
                <h2 class="text-3xl text-center">Keyword analysis: {$store.keyword}</h2>
            </div>
            <div class="md:pl-32 md:pr-10 pt-4 col-span-2 md:col-span-1 md:order-1 order-2">
                <BarChart labels={Object.keys($store.phraseContainsKeyword.count)} label='Phrases count' chartData={Object.values($store.phraseContainsKeyword.count)} barColor1={'#0f367b'} barColor2={'#0f367b'}/>
            </div>
            <div class="md:pr-32 pt-4 col-span-2 md:col-span-1 md:order-2 order-1">
                <p class="summary">The following bar chart breaks down the frequency of phrases which include the keyword, marked as <b>YES</b> and those who doesn't, labeled as <b>NO</b>. <br/> The bar charts included below show the sentiment analysis for the phrases with keyword, left chart, and without, right chart.</p>
            </div>
            <div class="md:pl-32 md:pr-10 pt-4 col-span-2 md:col-span-1 order-3">
                <h2 class="text-xl text-center pb-4">With keyword</h2>
                <BarChart labels={Object.keys($store.phraseContainsKeyword.yes)} label='Phrases count' chartData={Object.values($store.phraseContainsKeyword.yes)} />
            </div>
            <div class="md:pr-32 pt-4 col-span-2 md:col-span-1 order-4">
                <h2 class="text-xl text-center pb-4">Without keyword</h2>
                <BarChart labels={Object.keys($store.phraseContainsKeyword.no)} label='Phrases count' chartData={Object.values($store.phraseContainsKeyword.no)}/>
            </div>
        </div>
        <div class="grid grid-cols-2 pb-10 px-5 md:px-0 justify-items-stretch">
            <div class="col-span-2 pt-10 pb-4">
                <h2 class="text-3xl text-center">Entities spotted</h2>
            </div>
            <div class="md:pl-32 md:pr-10 pt-4 col-span-2 md:col-span-1">
                <p class="summary">Next you can find the frequency of different entities spotted in the urls provided. A named entity is a “real-world object” that’s assigned a name – for example, a person, a country, a product or a book title. They are categorized as follow:</p>
                <ul class="list-disc pt-3 pl-4">
                    <li><b>MISC: </b>Various</li>
                    <li><b>LOC: </b>Geopolitical entity, i.e. countries, cities, states.</li>
                    <li><b>ORG: </b>Companies, agencies, institutions.</li>
                    <li><b>PER: </b>People including fictional </li>
                </ul>
            </div>
            <div class="md:pr-32 pt-4 col-span-2 md:col-span-1 ">
                <BarChart labels={Object.keys($store.entitiesSpotted)} label='Entities count' chartData={Object.values($store.entitiesSpotted)} barColor1="#39bcf4" barColor2="#39bcf4" barColor3="#39bcf4" datalabelColor="#000000"/>
            </div>
        </div>
    {:else}
        <ErrorResult></ErrorResult>
    {/if}
</section>

<style>
    .summary{
        text-align: justify;
        text-justify: inter-word;
    }
    .fa-arrow-down{
        transform: rotate(0deg);
        transition: transform 0.4s linear;
    }
    .fa-arrow-down.open{
        transform: rotate(180deg);
        transition: transform 0.4s linear;
    }
</style>
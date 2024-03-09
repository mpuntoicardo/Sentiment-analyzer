<script>
    import '../app.css'
    export let urls = []
    let url = ''
    function onUrlChange({target: t}){
        url = t.value
    }
    function handleClick(){
        urls = [...urls, url]
        url = ''
    }
</script>


<div class="min-h-screen flex justify-center items-center background">
    <div class="backdrop-blur-sm p-5 bg-white/30 rounded-md">
        <div class="flex justify-center mb-3">
            <h1>Sentiment analysis</h1>
        </div>
        <div class>
            <input on:input={onUrlChange} bind:value={url} placeholder="Insert url" class="p-3 rounded-full">
            <button on:click={handleClick}>Add</button>
        </div>
        {#each urls as url, index}
            <p>{index+1} - {url}</p>
        {/each}
    </div>
</div>

<style lang="postcss">
    .background{
        background: rgb(63,94,251);
        background: radial-gradient(circle, rgba(63,94,251,0.9458377100840336) 11%, rgba(70,252,227,1) 100%);
    }
</style>
<script>
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


<div class="min-h-screen bg-gradient-to-b flex from-cyan-300 to-cyan-50 justify-center items-center">
    <div>
        <h1>Sentyment analysis</h1>
        <div>
            <input on:input={onUrlChange} bind:value={url} placeholder="Insert url" class="p-3 rounded-full">
            <button on:click={handleClick}>Add</button>
        </div>
        {#each urls as url, index}
            <p>{index+1} - {url}</p>
        {/each}
    </div>
</div>
  
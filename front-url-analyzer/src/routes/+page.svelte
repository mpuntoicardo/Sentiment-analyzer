<script>
    import image from '$lib/assets/Scenes05.svg'

    import Input from './Input.svelte'
    import Url from './url.svelte';


    export let urls = []
    let url = ''
    function handleClickUrlInput(){
        url = url.trim()
        if(url !== ''){
            urls = [...urls, url]
        }
        url = ''
    }

    let keyWord = ''
    function handleClickKeyWord(){

    }

</script>


<div class="min-h-screen flex flex-col justify-start items-center background pt-[50vh] static">
    <div class="backdrop-blur-sm p-6 bg-white/50 rounded-md z-10 w-2/4 mt-[-25vh] mb-24 shadow-lg flex flex-col ">
        <div class="flex justify-center mb-3">
            <h1 class="text-6xl text-cyan-800"><strong>Sentiment Analysis</strong></h1>
        </div>
        <div class="flex flex-col">
            <Input label="Urls" placeholder="e.g. www.example.com" bind:inputValue={url} handleClick={handleClickUrlInput}/>
            <Input label="Keyword" placeholder="e.g. Apple, Zara ..." bind:inputValue={keyWord} handleClick={handleClickKeyWord}/>
        </div>
        {#if urls.length}
        <div class="max-h-48 overflow-auto px-8 shadow-inner">
            {#each urls as url, index}
               <Url url={url} index={index}/>
            {/each}
        </div>
        {/if}
    </div>
    <div class="absolute bottom-0 -left-32 z-0 w-3/5 h-100">
        <img src={image} alt="alt" class="object-contain"/>
    </div>
</div>

<style lang="postcss">
    .background{
        background: rgb(63,94,251);
        background: radial-gradient(circle, rgba(63,94,251,0.9458377100840336) 11%, rgba(70,252,227,1) 100%);
    }
    h1{
        color:rgb(63,94,251)
    }
</style>
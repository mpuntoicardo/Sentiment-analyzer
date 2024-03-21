<script>
    import image from '$lib/assets/Scenes05.svg'

    import Input from './Input.svelte'
    import Url from './url.svelte';

    
    
    export let urls = []
    let url = ''
    let showErrorUrl = false
    function handleClickUrlInput(){
        url = url.trim()
        if(url.split(' ').length>1){
            showErrorUrl = true
        }else{
            if(url !== ''){
                urls = [...urls, url]
            }
            url = ''
            showErrorUrl = false
        }
    }
    function handleKeyUpUrl(){
        if (event.code == 'Enter') {
            event.preventDefault()
            handleClickUrlInput()
			return false
		}
    }
    
    let keyWord = ''
    let disableKeyWord = false
    function handleClickKeyWord(){
        keyWord = keyWord.trim()
        if(keyWord!=''){
            disableKeyWord = !disableKeyWord
        }
    }
    function handleKeyUpKeyWord(){
        if (event.code == 'Enter' || event.code == 'Space') {
            event.preventDefault()
            handleClickKeyWord()
			return false
		}
    }
    
    function handleDeleteUrl({target: t}){
        const urlToDelete = t.parentNode.children[1].innerHTML
        urls = urls.filter((el)=>{
            return el !== urlToDelete
        })
    }

    function handleSubmit(){
        const body={
            urls,
            keyWord
        }
        console.log(JSON.stringify(body))
    }
    
</script>


<div class="min-h-screen flex flex-col justify-start items-center background pt-[50vh] static">
    <div class="backdrop-blur-sm p-6 bg-white/50 rounded-md z-10 w-2/4 mt-[-25vh] mb-24 shadow-lg flex flex-col ">
        <div class="flex justify-center mb-3">
            <h1 class="text-5xl text-cyan-800"><strong>Sentiment Analysis</strong></h1>
        </div>
        <div class="flex flex-col">
            <Input label="Urls" placeholder="e.g. www.example.com" bind:inputValue={url} handleClick={handleClickUrlInput} showErrorUrl={showErrorUrl} handleKeyUp={handleKeyUpUrl}/>
            <Input label="Keyword" placeholder="e.g. Apple, Zara ..." bind:inputValue={keyWord} handleClick={handleClickKeyWord} disabled={disableKeyWord} buttonValue={disableKeyWord? "Edit":"Add"} handleKeyUp={handleKeyUpKeyWord}/>
        </div>
        {#if urls.length}
        <div class="max-h-40 overflow-auto px-8 shadow-inner">
            {#each urls as url, index}
               <Url url={url} index={index} handleDeleteUrl={handleDeleteUrl}/>
            {/each}
        </div>
        <div class="flex justify-center w-full mt-3">
            <button on:click={handleSubmit} class="bg-blue-500 rounded-full text-white w-6/12 p-3 hover:bg-blue-800">Compute</button>
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
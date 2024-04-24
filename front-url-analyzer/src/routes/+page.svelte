<script>
    import image from '$lib/assets/Scenes05.svg'

    import Input from './Input.svelte'
    import LoadingSpinner from './loadingSpinner.svelte';
    import Url from './url.svelte';
    import ErrorMessage from '../lib/Components/errorMessage.svelte';

    import { store } from './store.js'
    import Results from './results.svelte';  

    export let data
    console.log(data)

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
    
    let keyword = ''
    let disableKeyWord = false
    function handleClickKeyWord(){
        keyword = keyword.trim()
        if(keyword!=''){
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
    
    function handleDeleteUrl(index){
        urls = urls.filter((el, i)=>{
            return  i !== index
        })

    }

    let showLoadingSpinner = false
    let showErrorApi = false
    let showResults = false
    async function handleSubmit(){
        const body={
            urls,
            keyword
        }
        showLoadingSpinner = true
        showErrorApi = false
        try{
           const response = await fetch('http://127.0.0.1:5000/urlsAnalyzer',{
                method: "POST",
                mode: "cors",
                headers:{
                    "Content-Type": "application/json",
                    "Authorization": "Token " + (data.token || "")
                },
                body: JSON.stringify(body)
            })
            const res = await response.json()
            store.set({...res, keyword: keyword})
            showLoadingSpinner = false
            showResults = true
            await new Promise(resolve => requestAnimationFrame(resolve));
            document.querySelector('#results-section').scrollIntoView({
                behavior: 'smooth'
            });
        }catch(Error){
            showLoadingSpinner = false
            showErrorApi = true
            console.log(Error)
        }
    }
    
</script>


<div class="min-h-screen flex flex-col justify-start items-center background pt-[50vh] static">
    <div class="backdrop-blur-sm p-3 sm:p-6 bg-white/50 rounded-md z-10 w-2/4 mt-[-30vh] mb-24 shadow-lg flex flex-col w-full md:w-9/12 lg:w-6/12 ">
        <div class="flex justify-center mb-3">
            <h1 class="text-5xl text-center text-cyan-800"><strong>Sentiment Analysis</strong></h1>
        </div>
        <div class="flex flex-col">
            <Input label="Urls" placeholder="e.g. www.example.com" bind:inputValue={url} handleClick={handleClickUrlInput} showErrorUrl={showErrorUrl} handleKeyUp={handleKeyUpUrl}/>
            <Input label="Keyword" placeholder="e.g. Apple, Zara ..." bind:inputValue={keyword} handleClick={handleClickKeyWord} disabled={disableKeyWord} buttonValue={disableKeyWord? "Edit":"Add"} handleKeyUp={handleKeyUpKeyWord}/>
        </div>
        {#if data.loggedIn}
            <p class="infoP text-center pb-3">In your  <a href="/home" class="underline">dashboard</a> you can see your search history.</p>
        {:else}  
            <p class="infoP text-center pb-3">Consider <a href="/signup" class="underline">creating</a> an account or <a href="/login" class="underline">login</a> to automatically save your searchs</p>
        {/if}
        {#if urls.length}
        <div class="max-h-40 overflow-auto px-4 sm:px-8 shadow-inner">
            {#each urls as url, index}
               <Url url={url} index={index} handleDeleteUrl={handleDeleteUrl}/>
            {/each}
        </div>
        <div class="flex flex-col justify-center items-center w-full mt-3">
            <button on:click={handleSubmit} class="bg-blue-500 rounded-full text-white w-6/12 p-3 hover:bg-blue-800">Compute</button>
            {#if showLoadingSpinner}
                <div class="mt-2">
                    <LoadingSpinner/>
                </div>
            {/if}
            {#if showErrorApi}
                <ErrorMessage msg={'Error connecting to server'}/>
            {/if}
        </div>
        {/if}
    </div>
    <div class="absolute bottom-0 -left-32 z-0 md:w-3/5 h-100">
        <img src={image} alt="alt" class="object-contain"/>
    </div>
</div>
{#if showResults}
    <Results/>
{/if}

<style lang="postcss">
    .background{
        background: rgb(63,94,251);
        background: radial-gradient(circle, rgba(63,94,251,0.9458377100840336) 11%, rgba(70,252,227,1) 100%);
    }
    h1, .infoP{
        color:rgb(63,94,251)
    }
</style>
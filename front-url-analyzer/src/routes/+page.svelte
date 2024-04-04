<script>
    import image from '$lib/assets/Scenes05.svg'

    import Input from './Input.svelte'
    import LoadingSpinner from './loadingSpinner.svelte';
    import Url from './url.svelte';
    import ErrorMessage from '../lib/Components/errorMessage.svelte';

    import { store } from './store.js'
    import Results from './results.svelte';  

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
    
    function handleDeleteUrl({target: t}){
        const urlToDelete = t.parentNode.children[1].innerHTML
        urls = urls.filter((el)=>{
            return el !== urlToDelete
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
           /* const response = await fetch('http://127.0.0.1:5000/urlsAnalyzer',{
                method: "POST",
                mode: "cors",
                headers:{
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(body)
            })
            const data = await response.json()*/
            const data = {
    entitiesSpotted: {
        "LOC": 38,
        "MISC": 359,
        "ORG": 57,
        "PER": 42
    },
    failedUrls: [],
    globalResults: {
        "NEG": 66,
        "NEU": 326,
        "POS": 31
    },
    overallSent: "POS",
    phraseContainsKeyword: {
        count: {
            "NO": 387,
            "YES": 36
        },
        no: {
            "NEG": 56,
            "NEU": 302,
            "POS": 29
        },
        yes: {
            "NEG": 10,
            "NEU": 24,
            "POS": 2
        }
    },
    summary: "** Análisis de los iPhone 15 y iPhone 15 Plus: un resumen  en detalle**\n\n**Diseño:**\n* Mismos diseños que el iPhone  14\n* Ligera mejora en la comodidad\n* Resistencia al agua IP68\n* USB-C reemplaza a Lightning\n\n**Pantalla:** \n* OLED de 6,1\" (iPhone 15) y 6,7\" (iPhone 15 Plus)\n* Dynamic Island  con notificaciones mejoradas\n* Alta calidad con brillo de hasta 2000 nits\n* Sin ProMotion (refresco de pantalla a 60 Hz)\n\n**Sonido:**\n* Altavoces estéreo potentes\n * USB-C permite salida de audio\n* Sin puerto de auriculares\n\n**Potencia:**\n* Procesador Apple A16 Bionic\n* Rendimiento de primera línea comparable al iPhone 14 Pro\n* Buena gestión del calor \n\n**Batería:**\n* Mayor duración de la batería que el iPhone 14\n* Hasta tres días de uso con el iPhone 15 Plus\n* Carga rápida de hasta 30 W\n\n**Fotografía:**\n* Cámaras traseras duales (principal de 48 MP, ultra gran  angular de 12 MP)\n* Sensor principal mejorado con alta nitidez y rango dinámico\n* Modo Retrato automático\n* Sin teleobjetivo, pero zoom óptico de 2x\n\n**Puntos destacados:**\n* USB-C para carga y conectividad\n* Dynamic Island para notificaciones mejoradas\n*  Mayor duración de la batería\n* Cámaras traseras mejoradas\n\n**Puntos débiles:**\n* Pantalla sin ProMotion (refresco de pantalla a 60 Hz)\n* Sin teleobjetivo\n* Altavoz principal más débil que el iPhone 14 Pro"
}
            store.set(data)
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
    h1{
        color:rgb(63,94,251)
    }
</style>
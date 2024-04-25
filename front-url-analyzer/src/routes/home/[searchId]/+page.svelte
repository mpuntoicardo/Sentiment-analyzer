<script>
    import { tick } from 'svelte';
    import {delete_search, set_favorite, updateName} from '../api'
    import ErrorMessage from '../../../lib/Components/errorMessage.svelte';
    import Results from '../../results.svelte';
    import { store } from '../../store';
    import Modal from '../../../lib/Components/modal.svelte';
    import {goto} from '$app/navigation'

    export let data
    console.log(data)

    let showErrorMessage = false

    let inputDisabled = true
    let input
    let initialName = data.data?.search.name
    async function onPencilClick(e){
        inputDisabled = false
        await tick()
        input.focus()
        document.addEventListener('click', handleClick, true)
    }
    //Handle click outside input
    async function handleClick(event){
        if (inputDisabled !== true) {
                let isOutside = true;
                if (input && input.contains(event.target)) {
                    isOutside = false;
                }
            if (isOutside) {
                if(data.data.search.name === ""){
                    showErrorMessage = true
                    data.data.search.name = initialName
                }else{
                    const newSearch = await updateName(data.data.search.name, data.data.search.id, data.token)
                    showErrorMessage = false
                    inputDisabled = true
                    document.removeEventListener('click', handleClick, true);
                }
            }
        }
    }

    async function handleStarClick(){
        data.data.search.is_favorite =  !data.data.search.is_favorite
        await set_favorite(data.data.search.id, data.token)
    }

    let showResults = false

    async function handleButtonClick(){
        const result_id = data.data.search.result_id 
        const result = await fetch(`http://127.0.0.1:5000/getResult/${result_id}`,{
            method: "GET",
            mode: "cors",
        })
        const resultData = await result.json()
        store.set({...resultData, keyword: data.data.keyword.word})
        showResults = true
        await tick()
        document.querySelector('#results-section').scrollIntoView({
                behavior: 'smooth'
        });
    }

    let showModal = false
    const handleModal = ()=>{
        showModal = !showModal
    }

    async function handleDeleteClick(){
        await delete_search(data.data.search.id, data.token)
        goto('/home')
    }
</script>


{#if showModal}
    <Modal closeModal={handleModal} onDelete={handleDeleteClick}></Modal>
{/if}
{#if data.success}
<div class="min-h-screen background flex justify-center items-start py-16 static">
    <div class="w-10/12 min-h-96 backdrop-blur-sm bg-white p-4 shadow-md rounded-md">
        <div class="flex flex-wrap items-center justify-between">
            <input disabled={inputDisabled} bind:value={data.data.search.name} class="text-3xl font-bold bg-white pl-4 w-2/3" bind:this={input}>
            <div>
                <i class="fa-solid fa-pencil p-2 pencil" role="button" tabindex="0" on:click={onPencilClick}></i>
                <i class={"fa-solid p-2 fa-star " + (data.data.search.is_favorite? "fa-star_active ": "fa-star_inactive")} role="button" tabindex="0" on:click={handleStarClick}></i>
                <i class="p-2 fa-solid trash fa-trash" role="button" tabindex="0" on:click={handleModal}></i>
            </div>
        </div>
        {#if showErrorMessage}
            <ErrorMessage msg='Name can not be blank' css=' block '></ErrorMessage>
        {/if}
        <h2 class="text-xl font-semibold pl-4 my-3">Created at: {data.data.search.created_at.replace('T',' ').replace(/\.\d+Z$/, '')}</h2>
        <h2 class="text-xl font-semibold pl-4 mt-5">Urls:</h2>
        <ul class="divide-y divide-slate-300 p-1" role='list'>
            {#each data.data.urls as url}
                <li class="hover:bg-slate-200 rounded-md" role="button">
                    <a href={url.domain_name} class="w-100 h-100 block p-3" target="_blank">
                        {url.domain_name}
                    </a>
                </li>
            {/each}
        </ul>
        <div class="pl-4">
            {#if data.data.keyword.word}
            <h2 class="text-xl font-semibold block py-1">Keyword:</h2>
            <p class="pt-2">{data.data.keyword.word}</p>
            {/if}
            <div class="flex w-100 justify-center pt-9">
                <button class="bg-blue-500 rounded-full text-white w-6/12 sm:w-4/12 p-3 hover:bg-blue-800" on:click={handleButtonClick}>Show results</button>
            </div>
        </div>
    </div>
</div>
{#if showResults}
    <Results/>
{/if}
{:else}
    <div class="min-h-screen flex  items-center justify-center background">
        <h1 class="text-white font-bold text-5xl">Page not found 404</h1>
    </div>
{/if}

<style lang="postcss">
    .background{
        background: rgb(63,94,251);
        background: radial-gradient(circle, rgba(63,94,251,0.9458377100840336) 11%, rgba(70,252,227,1) 100%);
    }
    .fa-star_active:hover{
        color: #000000;
        transition: 0.2s
    }
    .fa-star_active{
        color: #FFD43B;
    }
    .fa-star_inactive:hover{
        color: #FFD43B;
        transition: 0.2s
    }
    .fa-trash{
        color: #f95353;
    }
    .fa-trash:hover{
        color: #ba1414;
        transition: 0.2s
    }
    .pencil{
        color: rgb(59 130 246);;
    }
    .pencil:hover{
        color: rgb(30 64 175);
        transition: 0.2s;
    }
</style>
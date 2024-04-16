<script>
    import { tick, onDestroy } from 'svelte';
    import {createSearchStore, searchHandler} from '$lib/stores/search'
    import {goto} from '$app/navigation'

    import {updateName, set_favorite, delete_search} from './api'
  import ErrorMessage from '../../lib/Components/errorMessage.svelte';

    export let data;

    const {user} = data
    let searchProducts  = data.searchs.map((search)=>({
        ...search,
        searchTerms: `${search.name}`
    }))

    const searchStore = createSearchStore(searchProducts)

    const unsubscribe = searchStore.subscribe((model)=>searchHandler(model))

    onDestroy(()=>{
        unsubscribe()
    })

    //Allows to keep track of the different inputs and focus and defocus the correct one
    let inputs = []

    //Turns a search from favorite to non-favorite or viceversa when star is clicked
    const handleStarClick = async(e)=>{
        e.stopPropagation();
        const searchObject = await set_favorite(e.target.id, data.token)
        updateStoreWithNewSearch(searchObject)
    }

    //This function takes a search which name or is_favorite has been updated and insert it into store
    const updateStoreWithNewSearch = (searchObject)=>{
        searchObject.search['searchTerms'] = searchObject.search.name
            searchStore.update((storeData)=>{
                const filteredData = storeData.data.map((element)=>{
                    return element.id != searchObject.search.id? element: searchObject.search
                })
                return { ...storeData, data:filteredData, filtered: filteredData}
            })
    }

    let editableId = null
    let editableIndex = null
    let showErrorEmptyEdit = false
    const handleEditClick = async(event,search,index)=>{
        event.stopPropagation();
        editableId = search.id
        editableIndex = index
        await tick()
        inputs[index].focus()
        document.addEventListener('click', handleClick, true)
    }
    async function handleClick(event){
            event.stopPropagation();
            if (editableId !== null) {
                let isOutside = true;
                inputs.forEach(input => {
                    if (input && input.contains(event.target)) {
                        isOutside = false;
                    }
                });
            if (isOutside) {
                if(inputs[editableIndex].value === ""){
                    showErrorEmptyEdit = true
                    inputs[editableIndex].focus()
                }else{
                    const newSearch = await updateName(inputs[editableIndex].value, editableId, data.token)
                    showErrorEmptyEdit =false
                    updateStoreWithNewSearch(newSearch)
                    editableId = null;
                    editableIndex = null
                    document.removeEventListener('click', handleClick, true);
                }
            }
        }
    }

    async function handleDeleteClick(event, id){
        event.stopPropagation();
        try{
            const deletedSearch = await delete_search(id, data.token)
            searchStore.update((storeData)=>{
                    const filteredData = storeData.data.filter((element)=>{
                        return element.id != id 
                    })
                    return { ...storeData, data:filteredData, filtered: filteredData}
                })
        }catch(error){
            alert('Error deleting search')
        }
    }
    //Handle input being clicked on disabled
    function handleClickOnDisabled(e,id){
        e.stopPropagation()
        goto(`/home/${id}`)
    }

    function handleListClick(search){
        goto(`/home/${search.id}`)
    }
</script>

<div class="background min-h-screen">
    <h1 class="text-3xl text-center py-4 text-white font-bold">Welcome back {user.name || ""}!</h1>
    <div class="flex w-full justify-center">
        <div class="w-10/12 sm:w-9/12 md:w-8/12 lg:w-6/12">
            <div class="flex justify-center items-center p-2 bg-white w-full shadow-md rounded focus-within:bg-gray-100">
                <input bind:value={$searchStore.search} class="p-2 focus:outline-none flex-grow focus:bg-gray-100" type="text" placeholder="Search..."/>
                <i class="fa-solid fa-magnifying-glass"></i>       
            </div>
            {#if showErrorEmptyEdit}
                <ErrorMessage msg='Search name can not be empty'></ErrorMessage>
            {/if}
            <div>
                <h3 class="block text-white">Show</h3>
                <select bind:value={$searchStore.filter} class="block appearance-none w-1/6 bg-white border border-gray-300 hover:border-gray-500 p-2 rounded shadow leading-tight focus:outline-none focus:shadow-outline">
                    <option value='All'>All</option>
                    <option value='Favorite'>Favorite</option>
                  </select>
            </div>
            <div class="w-full bg-white flex rounded-t-md mt-3 border-b-4 border-slate-300">
                <h2 class="w-3/6 border-r-4 border-slate-300 p-3">Name</h2>
                <h2 class="w-2/6 p-3">Creation date</h2>
            </div>
            {#if $searchStore.filtered.length}
            <ul role="list" class="w-full divide-y divide-slate-200 bg-white p-3 rounded-b-md"> 
                {#each $searchStore.filtered as search, index}
                    <li class="w-full bg-white flex p-3 items-center hover:bg-slate-200 group rounded-md" on:click={()=>handleListClick(search)} role="button">
                        <div class='relative inline-block w-3/6'>
                            <input class="w-full group-hover:bg-slate-200 disabled:bg-white px-2 focus:border-b-2" disabled={editableId!==search.id} type="text" value={search.name} bind:this={inputs[index]}/>
                            {#if editableId !== search.id}
                                <div class="absolute top-0 bottom-0 left-0 right-0 cursor-pointer" on:click={(e) => handleClickOnDisabled(e,search.id)}></div>
                            {/if}
                        </div>
                        <p class="w-2/6 pl-4">{search.created_at.replace('T',' ').replace(/\.\d+Z$/, '')}</p>
                        <div class="flex flex-col sm:flex-row">
                            <i class="fa-solid fa-pencil pencil p-2" on:click={(event) => handleEditClick(event,search, index)}></i>
                            <i class={"fa-solid p-2 fa-star " + (search.is_favorite? "fa-star_active ": "fa-star_inactive")} role="button" tabindex="0" on:click={handleStarClick} id={search.id}></i>
                            <i class="p-2 fa-solid trash fa-trash" on:click={(event)=>handleDeleteClick(event, search.id)}></i>
                        </div>
                    </li>
                {/each} 
            </ul>
            {:else}
                <div class="w-full rounded-b-md bg-white flex justify-center py-5">
                    <p class="text-slate-500">No results</p>
                </div>
            {/if}
        </div>
    </div>
</div>

<style>
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
    .background{
        background: rgb(63,94,251);
        background: radial-gradient(circle, rgba(63,94,251,0.9458377100840336) 11%, rgba(70,252,227,1) 100%);
    }
    .pencil{
        color: rgb(59 130 246);;
    }
    .pencil:hover{
        color: rgb(30 64 175);
        transition: 0.2s;
    }
</style>
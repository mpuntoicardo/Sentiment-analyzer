<script>
    import { tick, onDestroy } from 'svelte';
    import {createSearchStore, searchHandler} from '$lib/stores/search'

    import {updateName, set_favorite} from './api'

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
        const searchObject = await set_favorite(e, data.token)
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
            console.log($searchStore)
    }

    let editableId = null
    let editableIndex = null
    const handleEditClick = async(search,index)=>{
        editableId = search.id
        editableIndex = index
        await tick()
        inputs[index].focus()
        document.addEventListener('click', handleClick, true)
    }
    async function handleClick(event){
            if (editableId !== null) {
                let isOutside = true;
                inputs.forEach(input => {
                    if (input && input.contains(event.target)) {
                        isOutside = false;
                    }
                });
            if (isOutside) {
                const newSearch = await updateName(inputs[editableIndex].value, editableId, data.token)
                updateStoreWithNewSearch(newSearch)
                editableId = null;
                editableIndex = null
                document.removeEventListener('click', handleClick, true);
            }
        }
    }
</script>

<div class="bg-[#Dde2fd] min-h-screen">
    <h1 class="text-3xl text-center py-4">Welcome back {user.name || ""}!</h1>
    <div class="flex w-full justify-center">
        <div class="w-10/12 sm:w-7/12 md:w-5/12">
            <div class="flex justify-center items-center p-2 bg-white w-full shadow-md rounded focus-within:bg-gray-100">
                <input bind:value={$searchStore.search} class="p-2 focus:outline-none flex-grow focus:bg-gray-100" type="text" placeholder="Search..."/>
                <i class="fa-solid fa-magnifying-glass"></i>       
            </div>
            <div>
                <h3 class="block">Show</h3>
                <select bind:value={$searchStore.filter} class="block appearance-none w-1/6 bg-white border border-gray-300 hover:border-gray-500 p-2 rounded shadow leading-tight focus:outline-none focus:shadow-outline">
                    <option value='All'>All</option>
                    <option value='Favorite'>Favorite</option>
                  </select>
            </div>
            <div class="w-full bg-white p-3 flex mt-3">
                <h2 class="w-3/6">Name</h2>
                <h2 class="w-2/6">Creation date</h2>
            </div>
            <ul role="list" class="w-full divide-y divide-slate-200 bg-white p-3"> 
                {#each $searchStore.filtered as search, index}
                    <li class="w-full bg-white flex p-3 items-center hover:bg-slate-200 group">
                        <input class="w-3/6 group-hover:bg-slate-200 disabled:bg-white px-2 focus:border-b-2" disabled={editableId!==search.id} type="text" value={search.name} bind:this={inputs[index]}/>
                        <p class="w-2/6">{search.created_at.replace('T',' ').replace(/\.\d+Z$/, '')}</p>
                        <i class="fa-solid fa-pencil p-2" on:click={() => handleEditClick(search, index)}></i>
                        <i class={"fa-solid p-2 fa-star " + (search.is_favorite? "fa-star_active ": "fa-star_inactive")} role="button" tabindex="0" on:click={handleStarClick} id={search.id}></i>
                        <i class="p-2 fa-solid trash fa-trash"></i>
                    </li>
                {/each} 
            </ul>
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
</style>
<script>
    import { tick, onDestroy } from 'svelte';
    export let data;

    const {user} = data
    let {searchs}  = data

    //Allows to keep track of the different inputs and focus and defocus the correct one
    let inputs = []

    //Turns a search from favorite to non-favorite or viceversa when star is clicked
    const handleStarClick = async(e)=>{
        const response = await fetch(`http://127.0.0.1:8000/setSearchFavorite/${e.target.id}/`, {
        method: "PATCH",
        mode: "cors",
        headers:{
            "Authorization": "Token "+ data.token,
        },
        })
        if(!response.ok){
            alert('Error conectando con el servidor. Intentalo de nuevo más tarde')
        }else{
            const searchObject = await response.json()
            searchs = searchs.map((el)=>{
                return el.id !== searchObject.search.id? el: searchObject.search
            })
        }
    }

    let editableId = null

    const handleEditClick = async(search,index)=>{
        editableId = search.id
        await tick()
        inputs[index].focus()
        document.addEventListener('click', handleClick, true)
    }
    function handleClick(event){
            if (editableId !== null) {
                let isOutside = true;
                inputs.forEach(input => {
                    if (input && input.contains(event.target)) {
                        isOutside = false;
                    }
                });
            if (isOutside) {
                editableId = null;
                document.removeEventListener('click', handleClick, true);
            }
        }
    }

    let selectedOption = 'All'
    //To keep track of initial values
    let auxArr = []
    const handleOptionChange = ()=>{
        if(selectedOption =='All'){
            searchs = auxArr
        }else{
            auxArr = searchs
            searchs = searchs.filter((el)=>
                 el.is_favorite
            )
        }
    }
</script>

<div class="bg-[#Dde2fd] min-h-screen">
    <h1 class="text-3xl text-center py-4">Welcome back {user.name || ""}!</h1>
    <div class="flex w-full justify-center">
        <div class="w-10/12 sm:w-7/12 md:w-5/12">
            <div class="flex justify-center items-center p-2 bg-white w-full shadow-md rounded focus-within:bg-gray-100">
                <input class="p-2 focus:outline-none flex-grow focus:bg-gray-100" type="text" placeholder="Search..."/>
                <i class="fa-solid fa-magnifying-glass"></i>       
            </div>
            <div>
                <h3 class="block">Show</h3>
                <select bind:value={selectedOption} on:change={handleOptionChange} class="block appearance-none w-1/6 bg-white border border-gray-300 hover:border-gray-500 p-2 rounded shadow leading-tight focus:outline-none focus:shadow-outline">
                    <option value='All'>All</option>
                    <option value='Favorite'>Favorite</option>
                  </select>
            </div>
            <div class="w-full bg-white p-3 flex mt-3">
                <h2 class="w-3/6">Name</h2>
                <h2 class="w-2/6">Creation date</h2>
            </div>
            <ul role="list" class="w-full divide-y divide-slate-200 bg-white p-3"> 
                {#each searchs as search, index}
                    <li class="w-full bg-white flex p-3 items-center hover:bg-slate-200 group">
                        <input class="w-3/6 group-hover:bg-slate-200 disabled:bg-white bg-slate-400" disabled={editableId!==search.id} type="text" bind:value={search.name} bind:this={inputs[index]}/>
                        <p class="w-2/6">{search.created_at.replace('T',' ').replace(/\.\d+Z$/, '')}</p>
                        <i class="fa-solid fa-pencil pr-4" on:click={() => handleEditClick(search, index)}></i>
                        <i class={"fa-solid fa-star " + (search.is_favorite? "fa-star_active ": "fa-star_inactive")} role="button" tabindex="0" on:click={handleStarClick} id={search.id}></i>
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
</style>
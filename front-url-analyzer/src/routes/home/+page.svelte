<script>
    export let data;

    const {user} = data
    let {searchs}  = data


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

</script>

<div class="bg-[#Dde2fd] min-h-screen">
    <h1 class="text-3xl text-center mb-4">Welcome back {user.name || ""}!</h1>
    <div class="flex w-full justify-center">
        <div class="w-10/12 sm:w-7/12 md:w-5/12">
            <div class="flex justify-center items-center p-2 bg-white w-full shadow-md rounded focus-within:bg-gray-100">
                <input class="p-2 focus:outline-none flex-grow focus:bg-gray-100" type="text" placeholder="Search..."/>
                <i class="fa-solid fa-magnifying-glass"></i>       
            </div>
            <div>
                <h3 class="block">Show</h3>
                <select class="block appearance-none w-1/6 bg-white border border-gray-300 hover:border-gray-500 p-2 rounded shadow leading-tight focus:outline-none focus:shadow-outline">
                    <option>All</option>
                    <option>Favorite</option>
                  </select>
            </div>
            <div class="w-full bg-white p-3 flex mt-3">
                <h2 class="w-3/6">Name</h2>
                <h2 class="w-2/6">Creation date</h2>
            </div>
            <ul role="list" class="w-full divide-y divide-slate-200 bg-white p-3"> 
                {#each searchs as search}
                    <li class="w-full bg-white flex p-3 items-center hover:bg-slate-200">
                        <p class="w-3/6">{search.name}</p>
                        <p class="w-2/6">{search.created_at.replace('T',' ').replace(/\.\d+Z$/, '')}</p>
                        <i class="fa-solid fa-pencil pr-4"></i>
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
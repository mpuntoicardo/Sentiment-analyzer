<script>
    export let url
    export let index
    export let handleDeleteUrl


    const scroll = node => {
        node.scrollIntoView()
        window.scrollTo(0,0)
        }
</script>


<div class="w-full bg-white rounded-lg my-2 p-2 shadow-md hover:scale-105 hover:bg-gray-100 transition-all duration-200 flex items-center" use:scroll>
        <p class="p-2 w-1/12">{index+1}</p>
        <p class="grow p-2">{url}</p>
        <i class="fa-solid fa-trash mr-5 hover:animate-bounce" style="color: #f95353;" on:click={handleDeleteUrl}></i>
</div>
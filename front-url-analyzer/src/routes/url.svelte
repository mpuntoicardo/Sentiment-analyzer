<script>
    export let url
    export let index

    const scroll = node => {
        node.scrollIntoView()
    }
</script>


<div class="w-full bg-white rounded-lg mt-2 p-2 shadow-md hover:scale-105 hover:bg-gray-100 transition-all duration-200 flex" use:scroll>
        <p class="p-2 w-1/12">{index+1}</p>
        <p class="grow p-2">{url}</p>
</div>
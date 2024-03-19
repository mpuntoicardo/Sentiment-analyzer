<script>
    export let placeholder
    export let inputValue = ''
    export let handleClick
    export let label
    export let showErrorUrl
</script>

<div class="w-full">
    <div class="grid grid-cols-12 items-center p-3">
        <!-- Label -->
        <div class="col-span-2">
           <p class="text-md text-cyan-800">
            <strong >{label}</strong>
           </p> 
        </div>
        
        <!-- Input Field + Error Message -->
        <div class="col-span-8">
            <input bind:value={inputValue} placeholder={placeholder} class="p-4 rounded-l-full bg-white w-full focus:outline-none focus:ring focus:ring-cyan-500/50">
        </div>
        
        <!-- Button -->
        <div class="col-span-2">
            <button on:click={handleClick} class="rounded-r-full text-white rounded-l-lg p-4 text-md bg-blue-500">Add</button>
        </div>
        <div class="col-start-3 col-span-8 h-6">
            {#if showErrorUrl}
                <p class="mt-2 ml-3 errorMessage">Urls can't have spaces</p>
            {/if}
        </div>
    </div>
</div>



<style>
    p{
        color:rgb(63,94,251)
    }
    .errorMessage{
        color: rgba(220, 38, 38, 1);
    }
</style>
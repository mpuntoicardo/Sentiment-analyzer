<script>
    export let placeholder
    export let inputValue = ''
    export let handleClick
    export let handleKeyUp
    export let label
    export let showErrorUrl
    export let disabled = false
    export let buttonValue = "Add"

    import ErrorMessage from "../lib/Components/errorMessage.svelte";
</script>

<div class="w-full">
    <div class="grid grid-cols-12 items-center p-3 ">
        <!-- Label -->
        <div class="col-span-12 sm:col-span-2 pb-5 sm:pb-0">
           <p class="text-md text-cyan-800">
            <strong >{label}</strong>
           </p> 
        </div>
        
        <!-- Input Field + Error Message -->
        <div class="sm:col-span-8 col-span-10">
            <input disabled={disabled} bind:value={inputValue} on:keyup|preventDefault={handleKeyUp} placeholder={placeholder} class="p-4 rounded-l-full bg-white w-full focus:outline-none focus:ring focus:ring-cyan-500/50 border-white border disabled:bg-slate-200 disabled:text-slate-500 disabled:border-slate-200">
        </div>
        
        <!-- Button -->
        <div class="col-span-2">
            <button on:click={handleClick} class=" w-full sm:w-8/12 rounded-r-full text-white rounded-l-lg p-4 text-md bg-blue-500 hover:bg-blue-800 hover:border border border-blue-500 transition hover:border-blue-800">{buttonValue}</button>
        </div>
        <div class="sm:col-start-3 sm:col-span-8 col-span-10 h-6">
            {#if showErrorUrl}
                <ErrorMessage msg = {'Urls can not have spaces'}/>
            {/if}
        </div>
    </div>
</div>



<style>
    p{
        color:rgb(63,94,251)
    }
</style>
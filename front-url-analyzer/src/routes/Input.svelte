<script>
    export let placeholder
    export let inputValue = ''
    export let handleClick
    export let label
</script>


<div class="flex justify-center items-center w-full p-3">
    <p class="w-2/12 text-md text-cyan-800"><strong>{label}</strong></p>
    <input bind:value={inputValue} placeholder={placeholder} class="p-4 rounded-l-full w-8/12 bg-white">
    <button on:click={handleClick} class="rounded-r-full text-white rounded-l-lg p-4 text-md w-max bg-blue-500 h-4/6">Add</button>
</div>


<style>
    p{
        color:rgb(63,94,251)
    }
</style>
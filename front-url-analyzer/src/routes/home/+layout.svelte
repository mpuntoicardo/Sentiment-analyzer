<script>
    import { page } from '$app/stores';
    import { derived } from 'svelte/store';


    const isHomeIdPage = derived(page, $page => {
        const regex = /^\/home\/\d+$/; //Regex for /home/<int:id>
        const isMatch = regex.test($page.url.pathname);
        return isMatch;
    });
    const handleLogoutClick = ()=>{

    }
</script>

<div class="w-full flex px-5 py-3 items-center">
    <h1 class="text-md tracking-widest title w-1/3">Sentiment analysis</h1>
    <nav class="flex justify-center space-x-10 w-full">
        {#if $isHomeIdPage}
            <a href="/home" class="font-medium rounded-lg bg-blue-500 p-2 text-white hover:bg-blue-800">Home</a>
        {/if}
        <a href="/login" class="font-medium rounded-lg p-2 text-blue-500 border-2 border-blue-500 hover:bg-blue-500 hover:text-white" on:click={handleLogoutClick}>Logout</a>
    </nav>
</div>
<slot />

<style>
    .title{
        color:rgb(63,94,251)
    }
</style>
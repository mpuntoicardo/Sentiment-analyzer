<script>
    import { page } from '$app/stores';
    import { derived } from 'svelte/store';
    import {goto} from '$app/navigation'

    export let data

    const isHomeIdPage = derived(page, $page => {
        const regex = /^\/home\/\d+$/; //Regex for /home/<int:id>
        const isMatch = regex.test($page.url.pathname);
        return isMatch;
    });
    const handleLogoutClick = async()=>{
        await fetch('http://127.0.0.1:8000/logout',{
            method: 'DELETE',
            mode:'cors',
            headers: {
                "Authorization": 'Token ' + data.token
            }
        })
        goto('login')
    }
</script>

<div class="w-full flex px-5 py-3 items-center">
    <h1 class="text-md tracking-widest title w-1/3"><a href="/home">Sentiment Analysis</a></h1>
    <nav class="flex justify-between w-full">
        <div class="grow flex items-center justify-center gap-x-8 px-5">
            <a href="/" data-sveltekit-preload-data="tap" class="font-medium rounded-lg bg-blue-500 p-2 text-white hover:bg-blue-800 flex items-center h-full">+ Create Search</a>
            {#if $isHomeIdPage}
                <a href="/home" data-sveltekit-preload-data="tap" class="font-medium rounded-lg bg-blue-500 p-2 text-white hover:bg-blue-800 flex items-center h-full ">Home</a>
            {/if}
        </div>
        <a href="/login" data-sveltekit-preload-data="tap" class="font-medium rounded-lg p-2 text-blue-500 border-2 border-blue-500 hover:bg-blue-500 hover:text-white flex items-center" on:click={handleLogoutClick}>Logout</a>
    </nav>
</div>
<slot />

<style>
    .title{
        color:rgb(63,94,251)
    }
</style>
<script>
    import { scale } from "svelte/transition";
    
    export let onDelete

    export let closeModal

    function clickOutside(element){
        function handleClick(event){
            const targetElement = event.target

            if(element && !element.contains(targetElement)){
                const clickOutsideEvent = new CustomEvent('outside')
                element.dispatchEvent(clickOutsideEvent)
            }

        }
        document.addEventListener('click', handleClick, true)

        return {
            destroy() {
                document.removeEventListener('click', handleClick, true)
            }
        }
    }

</script>
<div class="fixed inset-0 bg-gray-600 bg-opacity-50 h-full w-full overflow-y-auto flex items-center justify-center z-10">
    <div class="bg-white p-5 rounded-md border-1 shadow-lg" on:outside={closeModal} use:clickOutside transition:scale>
        <h2 class="text-xl font-semibold">Are you sure you want to delete this search?</h2>
        <p class="text-slate-600 pt-2">This action is irreversible</p>
        <div class="flex w-full justify-center pt-5 gap-x-5">
            <button class="p-3 bg-white rounded-md border-2 border-red-600 text-red-600 hover:text-white hover:bg-red-600" on:click={onDelete}>Delete</button>
            <button class="p-3 rounded-md bg-blue-500 text-white border-2 border-blue-500 hover:text-blue-500 hover:bg-white" on:click={closeModal}>No</button>
        </div>
    </div>
</div>
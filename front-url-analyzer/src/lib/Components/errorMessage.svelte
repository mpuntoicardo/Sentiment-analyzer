<script>
    export let msg=''
    export let css =''
</script>

<div class={"flex items-center bg-red-200 p-1 rounded-md mt-2 px-5 "+css}>
    <i class="fa-solid fa-triangle-exclamation" style="color: #dc2626;"></i>
    <p class="ml-2">{msg}</p>
</div>

<style>
    p{
        color: rgba(220, 38, 38, 1);
    }
</style>
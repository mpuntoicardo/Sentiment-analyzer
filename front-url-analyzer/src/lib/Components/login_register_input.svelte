<script>
    export let width=''
    export let placeholder=''
    export let label=''
    export let type=''
    export let id =''
    export let padding =''
    export let handleInput
    export let error = false
</script>

<div class={width +" "+ padding}>
    <label class="block w-full mb-2 text-gray-700 font-bold" for={id}>{label}</label>
    <input on:input={handleInput} class={"block w-full border appearance-none  px-2 py-3 rounded shadow focus:outline-none focus:bg-gray-200 " + (error? "border-red-500":"")} type={type} placeholder={placeholder} id={id}>
</div>
<script>
        import image from '$lib/assets/Scenes02.svg'
        import LoginRegisterInput from '../../lib/Components/login_register_input.svelte';
        import ErrorMessage from '../../lib/Components/errorMessage.svelte';

        let errorEmail = false
        let errorPassword = false

        let userData = {
            email:'',
            password: ''
        }

        function handleInput(e){
            let target = e.target.id
           userData = {...userData, [target]:e.target.value}
        }

        async function handleSubmit(event){
            if(!userData.email.length && !userData.password.length){
                messageError = 'Email and password can not be blank'
                showError = true
                errorEmail = true
                errorPassword = true
            }else if(!userData.email.length){
                messageError = 'Email can not be blank'
                showError = true
                errorEmail = true
                errorPassword = false
            }else if(!userData.password.length){
                messageError = 'Password can not be blank'
                showError = true
                errorEmail = false
                errorPassword = true
            }else{
                showError = false
                errorEmail = false
                errorPassword = false
                return true
            }
            event.preventDefault();
            return false
        }

        export let form
</script>

<div class="max-h-screen h-screen flex">
    <div class="sm:w-2/3 w-0 h-full background">
        <img src={image} alt="alt" class="object-contain"/>
    </div>
    <div class="flex flex-col sm:w-1/3 w-full">
        <div class="flex flex-col w-full gap-3 pt-20">
            <h1 class="text-4xl text-center w-full font-bold">Login</h1>
            <h2 class="w-full text-md text-center tracking-widest">SENTIMENT ANALYSIS</h2>
        </div>
            <form class="w-full p-10" method="POST" action="?/login" on:submit={handleSubmit}>
                <LoginRegisterInput handleInput={handleInput} error={errorEmail} width="w-full" padding="pb-4" id="email" type="text" label="Email" placeholder="e.g: alumno@alumnos.upm.es"></LoginRegisterInput>
                <LoginRegisterInput handleInput={handleInput} error={errorPassword} width="w-full" padding="pb-3" id="password" type="password" label="Password" placeholder="*********"></LoginRegisterInput>
                <p class="text-sm text-blue-600 hover:text-blue-900 cursor-pointer">Forgot password?</p>
                <div class="max-h-12 h-full">
                    {#if form?.incorrect}
                        <ErrorMessage msg={form.messageError}/>    
                    {/if}
                </div>
                <div class="flex flex-col items-center w-full pt-5">
                    <button class="bg-blue-500 rounded text-white w-6/12 p-3 hover:bg-blue-800" type="submit">Login</button>
                    <p class="pt-3 text-sm underline text-blue-600 hover:text-blue-900 cursor-pointer"><a href="/signup">Don't have an account? Create one for free</a></p>
                </div>
            </form>
    </div>
</div>

<style lang="postcss">
    .background{
        background: rgb(63,94,251);
        background: radial-gradient(circle, rgba(63,94,251,0.9458377100840336) 11%, rgba(70,252,227,1) 100%);
    }
    h1,h2{
        color:rgb(63,94,251)
    }
</style>
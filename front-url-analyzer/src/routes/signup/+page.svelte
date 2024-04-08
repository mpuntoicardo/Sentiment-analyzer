<script>
    import image from '$lib/assets/Scenes02.svg'
    import LoginRegisterInput from '../../lib/Components/login_register_input.svelte';
    import ErrorMessage from '../../lib/Components/errorMessage.svelte';
    import {goto} from '$app/navigation'

    let messageError = ''
    let showError = false
    let errorEmail = false
    let errorPassword = false
    let errorUsername = false
    let errorFirstName = false
    let errorRepeatedPassword = false


    let userData = {
        email:'',
        password: '',
        repeated_password:'',
        username: '',
        first_name: '',

    }

    function handleInput(e){
        let target = e.target.id
       userData = {...userData, [target]:e.target.value}
    }

    function validateEmail(email){
        const re = new RegExp(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/g)
        return re.test(email)
    }
    function validatePassword(password, repeated_password){
         return repeated_password !== password? false:true
    }


    async function handleSubmit(){
        if(!userData.email.length || !userData.password.length || !userData.repeated_password.length || !userData.username.length){
            messageError = 'Please fill all the required fields'
            showError = true
            errorUsername = !userData.username.length
            errorEmail = !userData.email.length
            errorPassword = !userData.password.length
            errorRepeatedPassword = !userData.repeated_password.length
        }else{
            showError = false
            errorEmail = false
            errorPassword = false
            errorRepeatedPassword = false
            errorUsername = false
            errorFirstName = false
            const isValidEmail = validateEmail(userData.email)
            const isValidPassword = validatePassword(userData.password, userData.repeated_password)
            if(!isValidEmail && !isValidPassword){
                messageError = "Check invalid fields"
                showError = true
                errorPassword = true
                errorRepeatedPassword = true
                errorEmail =true
                return
            }
            if(!isValidPassword){
                messageError = "Passwords must be the same"
                showError = true
                errorPassword = true
                errorRepeatedPassword = true
                return
            }
            if(!isValidEmail){
                messageError = "Please fill a valid email"
                showError = true
                errorEmail = true
                return
            }
            try{
                const response = await fetch('http://127.0.0.1:8000/signup',{
                    method: "POST",
                    mode: "cors",
                    headers:{
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(userData)
                })
                const data = await response.json()
                if(response.ok){
                    console.log(data)
                    goto('/login')
                }else{
                    showError = true
                    let errors = Object.values(data.errors).map(err=> err[0]).join(" ")
                    messageError= errors
                }
            }catch(error){
                showError = true
                console.log(error)
                messageError='Error connecting to server'
            }
        }
    }

</script>

<div class="max-h-screen h-screen flex">
<div class="sm:w-2/3 w-0 h-full background">
    <img src={image} alt="alt" class="object-contain"/>
</div>
<div class="flex flex-col sm:w-1/3 w-full">
    <div class="flex flex-col w-full gap-2 pt-10">
        <h1 class="text-4xl text-center w-full font-bold">Sign up</h1>
        <h2 class="w-full text-md text-center tracking-widest">SENTIMENT ANALYSIS</h2>
    </div>
        <form class="w-full px-10 py-5" on:submit|preventDefault={handleSubmit}>
            <div class="flex justify-between flex-col md:flex-row">
                <LoginRegisterInput handleInput={handleInput} error={errorUsername} width="w-full md:w-[45%]" padding="pb-2" id="username" type="text" label="Username*" placeholder="e.g: alumno123"></LoginRegisterInput>
                <LoginRegisterInput handleInput={handleInput} error={errorFirstName} width="w-full md:w-[50%]" padding="pb-2" id="first_name" type="text" label="First name" placeholder="e.g: John Doe"></LoginRegisterInput>
            </div>
            <LoginRegisterInput handleInput={handleInput} error={errorEmail} width="w-full" padding="pb-2" id="email" type="text" label="Email*" placeholder="e.g: alumno@alumnos.upm.es"></LoginRegisterInput>
            <LoginRegisterInput handleInput={handleInput} error={errorPassword} width="w-full" padding="pb-2" id="password" type="password" label="Password*" placeholder="*********"></LoginRegisterInput>
            <LoginRegisterInput handleInput={handleInput} error={errorRepeatedPassword} width="w-full" padding="pb-2" id="repeated_password" type="password" label="Repeat password*" placeholder="*********"></LoginRegisterInput>
            <p class="text-sm text-gray-500">Required fields *</p>
            <div class="max-h-20 h-full">
                {#if showError}
                    <ErrorMessage msg={messageError}/>    
                {/if}
            </div>
            <div class="flex flex-col items-center w-full">
                <button class="bg-blue-500 rounded text-white w-6/12 p-3 hover:bg-blue-800" type="submit">Signup</button>
                <p class="pt-3 text-sm underline text-blue-600 hover:text-blue-900 cursor-pointer"><a href="/login">Already have an account? Login here!</a></p>
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
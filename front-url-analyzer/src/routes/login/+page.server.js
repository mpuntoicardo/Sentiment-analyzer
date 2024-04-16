import { fail, isRedirect, redirect } from "@sveltejs/kit"


export const actions = {
	login: async ({cookies, request, url}) => {
		let data = await request.formData()
        const user = {
            email: data.get('email'),
            password: data.get('password')
        }
        try{
            const response = await fetch('http://127.0.0.1:8000/login',{
                method: "POST",
                mode: "cors",
                headers:{
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(user)
            })
            if(response.ok){
                const data = await response.json()
                cookies.set("auth", data.token,{
                    path: '/',
                    maxAge: 60 * 60 * 24 * 31,
                    httpOnly:true
                })
                return redirect(303, '/home');
            }else{
                let messageError='Invalid username or password'
                return fail(404, {messageError, incorrect: true})
            }
        }catch(error){
            if (isRedirect(error)) throw error; //Comprobamos que venga de redirect
            let messageError='Error connecting to server'
            return fail(500, {messageError, incorrect: true})
        }
	},
}
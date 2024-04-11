import { redirect } from "@sveltejs/kit"

export const load = async ({locals, cookies})=>{
    if(!locals.user){
        throw redirect(303, '/login')
    }
    const auth_token = cookies.get('auth')
    const response = await fetch('http://127.0.0.1:8000/get_search_id', {
        method: "GET",
        mode: "cors",
        headers:{
            "Authorization": "Token "+auth_token,
        },
    })
    const data = await response.json() 
    const user = locals.user
   return {user, searchs: data.searchs, token: auth_token }
}
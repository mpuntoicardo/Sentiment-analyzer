import { redirect } from "@sveltejs/kit"

export const load = async({params, locals, cookies})=>{
    if(!locals.user){
        throw redirect(303, '/login')
    }

    const {searchId} = params
    const auth_token = cookies.get('auth')

    const response = await fetch(`http://127.0.0.1:8000/get_search_info/${searchId}/`,{
        method:'GET',
        mode: "cors",
        headers:{
            "Authorization": "Token "+auth_token,
        },
    })
    if(response.ok){
        const data = await response.json()
        return {success: true, data, token:auth_token}
    }else{
        return {success:false}
    }

}
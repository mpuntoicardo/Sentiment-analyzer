export const load =async({locals, cookies})=>{
    if(!locals.user){
        return {loggedIn: false}
    }
    const token = cookies.get('auth')
    return {token, loggedIn: true}
}
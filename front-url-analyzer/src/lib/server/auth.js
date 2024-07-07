export const authenticateUser = async(event)=>{
    const {cookies} = event
    const userToken = cookies.get('auth')
    try{
        const response = await fetch('http://127.0.0.1:8000/test_token',{
            method: "GET",
            mode: "cors",
            headers:{
                "Authorization": "Token "+userToken,
            },
        })
        
        if(response.ok){
            const data = await response.json()
            const {user} = data
            return user
        }else{
            return null
        }
    }catch(error){
        return null
    }
}
export const updateName = async(name, id, token)=>{
    try{
        const response = await fetch(`http://127.0.0.1:8000/updateSearchName/${id}/`, {
            method: "PATCH",
            mode: "cors",
            headers:{
                "Authorization": "Token "+ token,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({name: name})
        })
        const data = await response.json()
        return data
    }catch(error){
        return error
    }
}

export const set_favorite = async(e,token)=>{
    const response = await fetch(`http://127.0.0.1:8000/setSearchFavorite/${e.target.id}/`, {
        method: "PATCH",
        mode: "cors",
        headers:{
            "Authorization": "Token "+ token,
        },
        })
        if(!response.ok){
            alert('Error conectando con el servidor. Intentalo de nuevo más tarde')
        }else{
            const searchObject = await response.json()
            return searchObject
        }
}
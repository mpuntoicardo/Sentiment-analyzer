import { writable } from "svelte/store"


export const createSearchStore = (data) =>{
    const {subscribe , set, update} = writable({
        data,
        filtered: data,
        search: '',
        filter: 'All'
    })
    return {
        subscribe,
        set,
        update
    }
}

export const searchHandler = (store)=>{
    const searchTerm = store.search.toLowerCase() || ''
    store.filtered = store.data.filter((item)=>{
        if(store.filter === "Favorite"){
            return item.searchTerms.toLowerCase().includes(searchTerm) && item.is_favorite
        }else{
            return item.searchTerms.toLowerCase().includes(searchTerm)
        }
    })
}
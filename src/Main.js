import react , {useState} from "react";
import axios from "axios";

const Main=()=>{
    const [search,setSearch]=useState("");
    const [bookData,setData]=useState("");
    const searchBook=(evt)=>{
        if(evt.key=="Enter"){
            axios.get('https://www.googleapis.com/books/v1/volumes?q='+search+'&key=AIzaSyCuHdDuHmXyIuvAHZgdc94kl-W5Tek3lco')
            .then(res=>setData(res.data.items))
            .catch(err=>console.log(err))
        }
    }
}
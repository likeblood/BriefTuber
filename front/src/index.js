import React from "react";
import * as ReactDOMClient from 'react-dom/client';
import axios from "axios";

import NewVideoForm from "./components/form";

import "./css/index.css";

var video_data = []

const intervalBack = setInterval (() => {
    if (video_data.length > 0){
        axios({
            method: 'post',
            url: `http://localhost:8000/get_video_status/${video_data[0].video_id}`
        })
        .then(responce => {
            video_data[0].preprocess_status = JSON.stringify(responce.data.preprocess_status).slice(1, -1)
            video_data[0].ready_message = responce.data.ready_message
            app.render(<NewVideoForm />)
            if (video_data[0].status === 'finished') {
                clearInterval(intervalBack)
            }
        })
        .catch(error => console.log(error))
}
}, 10000)


const app = ReactDOMClient.createRoot(document.getElementById("main"))

app.render(<NewVideoForm />)

export default video_data

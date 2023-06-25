import React from "react";


const TextMessage = ({status, message}) => {
    if (status === 'in_progress' || status === 'uploaded') {
        return(
            <div className="spiner">
                <span className="spinner__animation"></span>
                <span className="spinner__info">Загрузка</span>
            </div>
            
        )
    }
    else if(status === 'failed') {
        return (
            <p className="error">TEST</p>
        )
    }
    else {
        return(
            <div>
            {message.map((val) => {
                return(
                    <div className="one_message">
                        <h2 className="title">[{JSON.stringify(val.timecode).slice(1, -1)}] {JSON.stringify(val.title).slice(1, -1)}</h2>
                        <p className="text">{JSON.stringify(val.text).slice(1, -1)}</p>
                        <img className='images' src={'data:image/png;base64,' + JSON.stringify(val.image).slice(3, -3)}  alt="PNG MISSED"/>
                    </div>
                )
            })}
            </div>
        
        )
    }
}

export default TextMessage

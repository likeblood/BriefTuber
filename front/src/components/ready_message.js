import React from "react";


const TextMessage = ({status, message}) => {
    if (status !== 'finished') {
        return(
            <p>{JSON.stringify(message[0]).slice(1, -1)}</p>
        )
    }
    else {
        return(
            <div>
            {message.map((val) => {
                return(
                    <div className="one_message">
                        <p className="article">[{JSON.stringify(val.timecode).slice(1, -1)}] {JSON.stringify(val.text).slice(1, -1)}</p>
                        <img className='images' src={JSON.stringify(val.image).slice(1, -1)} alt="PNG MISSED"/>
                    </div>
                )
            })}
            </div>
        
        )
    }
}

export default TextMessage
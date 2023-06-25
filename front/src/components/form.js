import React from "react"
import axios from "axios"
import video_data from ".."
import TextMessage from "./ready_message"


class NewVideoForm extends React.Component{
    
    constructor(props) {
        super(props)
        this.state = {
            timeRange: "ALL_VIDEO",
            lengthAnnotation: "NO_LIMITS",
            lengthArticle: "NO_LIMITS",
            
            textData: "",
            videoStartTime: "START",
            videoEndTime: "END",
            lengthAnnotationData: "ANY",
            lengthArticleData: "ANY"
        }
        this.inputClick = this.inputClick.bind(this)
    }


    inputClick(){
        if (this.state.textData.length > 0)
            axios({
                method: 'post',
                url: `http://localhost:8000/upload_video?video_link=${this.state.textData}&video_start_time=${this.state.videoStartTime}&video_end_time=${this.state.videoEndTime}&annotation_length=${this.state.lengthAnnotationData}&article_length=${this.state.lengthArticleData}`,
              })
              .then(response => {
                let temp = {}
                temp = {
                    video_id: JSON.stringify(response.data.id).slice(1, -1),
                    video_link: this.state.textData,
                    preprocess_status: JSON.stringify(response.data.preprocess_status).slice(1, -1),
                    ready_message: [JSON.stringify(response.data.ready_message[0]).slice(1, -1)]
                }
                this.setState({textData: ""})
                video_data.push(temp)
        })
              .catch(error => console.log(error))
        }        


    render(){
        if (video_data.length === 0) {
            return (
            <div className="new_form">
                <form className="main_form">
                    <p className="desription first_text">Вставьте ссылку на YouTube видео</p>
                    <input type="text" className="field" onChange={event => this.setState({textData: event.target.value})} placeholder="Введите ссылку на видео" value={this.state.textData}/>

                    <p className="desription">Выберите диапозон видео</p>
                    <select className="field" onChange={event => this.setState({timeRange: event.target.value})}>
                        <option className="test" value="ALL_VIDEO">Всё видео</option>
                        <option value="INTERVAL">Интервал</option>
                    </select>
                    {this.state.timeRange === "INTERVAL" 
                    ?
                    <div className="drop-down_list">
                        <input className="drop-down_list" onChange={event => this.setState({videoStartTime: event.target.value})} placeholder="Введите начало видео (чч:мм:сс)"></input>
                        <input className="drop-down_list" onChange={event => this.setState({videoEndTime: event.target.value})} placeholder="Введите конец видео (чч:мм:сс)"></input>
                    </div> 
                    :
                    <div></div>}

                    <p className="desription">Выберите длинну аннотации</p>
                    <select className="field" onChange={event => this.setState({lengthAnnotation: event.target.value})}>
                        <option value="NO_LIMITS">Без ограничений</option>
                        <option value="LENGTH">Ограниченная</option>
                    </select>
                    {this.state.lengthAnnotation === "LENGTH" 
                    ?
                    <input className="field" onChange={event => this.setState({lengthAnnotationData: event.target.value})} placeholder="Введите максимальное кол-во символов"></input>
                    :
                    <div></div>}

                    <p className="desription">Выберите длинну статьи</p>
                    <select className="field" onChange={event => this.setState({lengthArticle: event.target.value})}>
                        <option value="NO_LIMITS">Без ограничений</option>
                        <option value="LENGTH">Ограниченная</option>
                    </select>
                    {this.state.lengthArticle === "LENGTH" 
                    ?
                    <input className="field" onChange={event => this.setState({lengthArticleData: event.target.value})} placeholder="Введите максимальное кол-во символов"></input>
                    :
                    <div></div>}

                    <input type="button" className="field button" onClick={this.inputClick} value="Отправить" />
                </form>
            </div>
            )
        }
        else {
            return (
                <div className="ready_message">
                        <p className="links">Ссылка на видео - <a href={video_data[0].video_link} className="links">{video_data[0].video_link}</a></p>
                    <TextMessage status={video_data[0].preprocess_status} message={video_data[0].ready_message}/>
                </div>
            )
        }
    }
        
}


export default NewVideoForm

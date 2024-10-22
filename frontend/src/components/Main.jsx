import React, { useState } from 'react';
import Fileinput from './Fileinput';
import css from './Main.module.css';
function Main(props) {
    const [newChat, setnewChat] = useState();
    const newChatClicked = () =>{}
    const array = ["this is phani from hyderabad and india","this is phani from hyderabad and india","this is phani from hyderabad and india",
        "this is phani from hyderabad and india","this is phani from hyderabad and india","this is phani from hyderabad and india",
        "this is phani from hyderabad and india","this is phani from hyderabad and india","this is phani from hyderabad and india",
        9,10,11,12,13,14,15]
    const lengthCheck = (element) =>{
        if(element.length > 20){
            // we are going to pass the only characters
            return element.substring(0,30)
        }
        return element
    }
    return (
        <div className={css.main}>
            <nav>
                <div className={css.new}>
                    <button onClick={newChatClicked}> New Chat </button>
                </div>
                <div className={css.previous}>
                    {//* list of previous chats, we need to scroller and we are going to use map function over here
                    array.map(element => <div className={css.prev}> {
                        lengthCheck(element)
                    } </div>)
                    }
                </div>
            </nav>
            <body>
                <div className={css.images}> </div>
                <div className={css.input}>
                    <Fileinput />
                </div>
            </body>
        </div>
    );
}

export default Main;
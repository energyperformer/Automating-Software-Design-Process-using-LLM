import React, { useState } from 'react';
import css from './Fileinput.module.css';
function Fileinput(props) {
    const [file, setFile] = useState(null);
    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };
    const uploadFile = () => {
        //* write the logic for uploading the file
    }
    return (
        <div className={css.main}>
            <input type='file' placeholder='select file' onChange={handleFileChange}/>
            <button onClick={uploadFile}> upload </button>
        </div>
    );
}

export default Fileinput;
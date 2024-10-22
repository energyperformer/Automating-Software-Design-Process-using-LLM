import React, { useState } from 'react';
import css from './Fileinput.module.css';
function Fileinput(props) {
    const [file, setFile] = useState(null);
    const [prompt,changePrompt] = useState("Desi GPT , Girish is a gandu")
    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };
    const uploadFile = () => {
        //* write the logic for uploading the file
    }
    return (
        <div className={css.input}>
            <div class={css.file_input_wrapper}>
    <label for="file-upload" class={css.custom_file_label}>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21.44 11.05l-8.49 8.49a5.75 5.75 0 01-8.13-8.13l8.5-8.5a3.75 3.75 0 015.3 5.3l-8.5 8.5a1.75 1.75 0 01-2.48-2.48l8.5-8.5" />
      </svg>
    </label>
    <input type="file" id="file-upload" onChange={handleFileChange} />
  </div>
        <input type='text' placeholder='Enter prompt' value={prompt} onChange={(event) => changePrompt(event.target.value)} className={css.prompt}/>
            <button onClick={uploadFile} className={css.btn}> <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M5 10l7-7 7 7M12 3v18" />
</svg>
 </button>
        </div>
    );
}

export default Fileinput;
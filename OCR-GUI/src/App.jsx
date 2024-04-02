import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const OCRApp = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [ocrText, setOcrText] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', selectedFile);
  
    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      // Replace newline characters with <br> tags
      const formattedText = response.data.replace(/\n/g, '<br>');

      setOcrText(formattedText);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };
  
  return (
    <div>
      <h1>GUI FOR OCR</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <div>
        {ocrText && (
          <div>
            <h2>OCR Text:</h2>
            {/* Render HTML dangerously */}
            <p dangerouslySetInnerHTML={{ __html: ocrText }}></p>
          </div>
        )}
      </div>
    </div>
  );
};

export default OCRApp;

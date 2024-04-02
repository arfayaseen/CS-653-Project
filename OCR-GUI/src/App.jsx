import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const OCRApp = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [ocrText, setOcrText] = useState('');
  const [processedImages, setProcessedImages] = useState([]);

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
      const { ocr_text: ocrText, processed_images: encodedImages } = response.data;
      const images = encodedImages.map(encodedImage => `data:image/png;base64,${encodedImage}`);
      setProcessedImages(images);
      const formattedText = ocrText.replace(/\n/g, '<br>');
      setOcrText(formattedText);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };
  
  return (
    <div>
      <h1 className="title">GUI FOR OCR</h1>
      <div className="upload-container">
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload</button>
      </div>
      <div className="main-container">
        <div className="original-image-container">
          {processedImages.length > 0 && (
            <div>
              <h3>Original GrayScale Image</h3>
              <img src={processedImages[0]} alt="Original GrayScale" className="center-image" />
              {ocrText && (
                <div className="ocr-text-container">
                  <h2>OCR Text:</h2>
                  <p dangerouslySetInnerHTML={{ __html: ocrText }}></p>
                </div>
              )}
            </div>
          )}
        </div>
        <div className="processed-images-container">
          {processedImages.slice(1).map((image, index) => (
            <div key={index} className="image-wrapper">
              <h3>{index === 0 ? 'Sharpened Image' : index === 1 ? 'Denoised Image' : index === 2 ? 'Dilated Image' : index === 3 ? 'Erased Image' : 'Contrasted Image'}</h3>
              <img src={image} alt={`Processed Image ${index + 1}`} className="center-image" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default OCRApp;

import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const OCRApp = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [ocrText, setOcrText] = useState('');
  const [processedImages, setProcessedImages] = useState({});

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

      const data = response.data;
      setOcrText(data.sharpened_ocr_result);
      setProcessedImages({
        original: data.original_image,
        grayScale: data.gray_scale_image,
        sharpened: { image: data.sharpened_image, ocrText: data.sharpened_ocr_result, accuracy: data.sharpened_accuracy },
        // denoised: { image: data.denoised_image, ocrText: data.denoised_ocr_result, accuracy: data.denoised_accuracy },
        // eroded: { image: data.eroded_image, ocrText: data.eroded_ocr_result, accuracy: data.eroded_accuracy },
        // dilated: { image: data.dilated_image, ocrText: data.dilated_ocr_result, accuracy: data.dilated_accuracy }
      });
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
          {processedImages.original && (
            <div>
              <h3>Original Image</h3>
              <img src={`data:image/png;base64,${processedImages.original}`} alt="Original" className="center-image" style={{ maxWidth: '300px' }} />
            </div>
          )}
        </div>
        <div className="original-image-container">
          {processedImages.grayScale && (
            <div>
              <h3>Grayscale Image</h3>
              <img src={`data:image/png;base64,${processedImages.grayScale}`} alt="Grayscale" className="center-image" style={{ maxWidth: '300px' }} />
            </div>
          )}
        </div>
        <div className="processed-images-container">
          {Object.keys(processedImages).map((key, index) => (
            key !== 'original' && key !== 'grayScale' && (
              <div key={index} className="image-wrapper">
                <h3>{key.charAt(0).toUpperCase() + key.slice(1)} Image</h3>
                <img src={`data:image/png;base64,${processedImages[key].image}`} alt={`${key} Image`} className="center-image" />
                {processedImages[key].ocrText && (
                  <div className="ocr-text-container">
                    <h2>OCR Text:</h2>
                    <p dangerouslySetInnerHTML={{ __html: processedImages[key].ocrText.replace(/\n/g, '<br>') }}></p>
                    {processedImages[key].accuracy && (
                      <>
                        <p><strong>{processedImages[key].accuracy}</strong></p>
                        <hr className="accuracy-line" />
                      </>
                    )}
                  </div>
                )}
              </div>
            )
          ))}
        </div>

      </div>
    </div>
  );
};

export default OCRApp;

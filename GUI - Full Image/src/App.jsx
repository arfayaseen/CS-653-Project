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
        denoised: { image: data.denoised_image, ocrText: data.denoised_ocr_result, accuracy: data.denoised_accuracy },
        eroded: { image: data.eroded_image, ocrText: data.eroded_ocr_result, accuracy: data.eroded_accuracy },
        dilated: { image: data.dilated_image, ocrText: data.dilated_ocr_result, accuracy: data.dilated_accuracy }
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
        <div className="row">
          <div className="image-container">
            {processedImages.original && (
              <div>
                <h3>Original Image</h3>
                <img src={`data:image/png;base64,${processedImages.original}`} alt="Original" className="center-image" style={{ maxWidth: '300px' }} />
              </div>
            )}
          </div>
          <div className="image-container">
            {processedImages.grayScale && (
              <div>
                <h3>Grayscale Image</h3>
                <img src={`data:image/png;base64,${processedImages.grayScale}`} alt="Grayscale" className="center-image" style={{ maxWidth: '300px' }} />
              </div>
            )}
          </div>
          <div className="image-container">
            {processedImages.sharpened && (
              <div>
                <h3>Sharpened Image</h3>
                <img src={`data:image/png;base64,${processedImages.sharpened.image}`} alt="Sharpened" className="center-image" />
                {processedImages.sharpened.ocrText && (
                  <div className="ocr-text-container">
                    <h2>OCR Text:</h2>
                    <p dangerouslySetInnerHTML={{ __html: processedImages.sharpened.ocrText.replace(/\n/g, '<br>') }}></p>
                    {processedImages.sharpened.accuracy && (
                      <>
                        <p><strong>Accuracy:</strong> {processedImages.sharpened.accuracy} %</p>
                        <hr className="accuracy-line" />
                      </>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
        <div className="row">
          <div className="image-container">
            {processedImages.denoised && (
              <div>
                <h3>Denoised Image</h3>
                <img src={`data:image/png;base64,${processedImages.denoised.image}`} alt="Denoised" className="center-image" />
                {processedImages.denoised.ocrText && (
                  <div className="ocr-text-container">
                    <h2>OCR Text:</h2>
                    <p dangerouslySetInnerHTML={{ __html: processedImages.denoised.ocrText.replace(/\n/g, '<br>') }}></p>
                    {processedImages.denoised.accuracy && (
                      <>
                        <p><strong>Accuracy:</strong> {processedImages.denoised.accuracy} %</p>
                        <hr className="accuracy-line" />
                      </>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
          <div className="image-container">
            {processedImages.eroded && (
              <div>
                <h3>Eroded Image</h3>
                <img src={`data:image/png;base64,${processedImages.eroded.image}`} alt="Eroded" className="center-image" />
                {processedImages.eroded.ocrText && (
                  <div className="ocr-text-container">
                    <h2>OCR Text:</h2>
                    <p dangerouslySetInnerHTML={{ __html: processedImages.eroded.ocrText.replace(/\n/g, '<br>') }}></p>
                    {processedImages.eroded.accuracy && (
                      <>
                        <p><strong>Accuracy:</strong> {processedImages.eroded.accuracy} %</p>
                        <hr className="accuracy-line" />
                      </>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
          <div className="image-container">
            {processedImages.dilated && (
              <div>
                <h3>Dilated Image</h3>
                <img src={`data:image/png;base64,${processedImages.dilated.image}`} alt="Dilated" className="center-image" />
                {processedImages.dilated.ocrText && (
                  <div className="ocr-text-container">
                    <h2>OCR Text:</h2>
                    <p dangerouslySetInnerHTML={{ __html: processedImages.dilated.ocrText.replace(/\n/g, '<br>') }}></p>
                    {processedImages.dilated.accuracy && (
                      <>
                        <p><strong>Accuracy:</strong> {processedImages.dilated.accuracy} %</p>
                        <hr className="accuracy-line" />
                      </>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OCRApp;

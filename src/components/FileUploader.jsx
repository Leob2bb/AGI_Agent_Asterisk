import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { dreamService } from '../services/api';
import { authService } from '../services/api';

function FileUploader({ onFileSelect, title, date }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const allowedTypes = [
    'application/pdf',
    'text/plain'
  ];

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) {
      return;
    }
    // 파일 타입 검증
    if (!allowedTypes.includes(selectedFile.type)) {
      setError('PDF 또는 TXT 파일만 업로드 가능합니다.');
      setFile(null);
      return;
    }
    // 파일 크기 제한 (10MB)
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('파일 크기는 10MB 이하여야 합니다.');
      setFile(null);
      return;
    }
    setError('');
    setFile(selectedFile);
    onFileSelect(selectedFile);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const droppedFile = e.dataTransfer.files[0];
    if (!droppedFile) {
      return;
    }
    if (!allowedTypes.includes(droppedFile.type)) {
      setError('PDF 또는 TXT 파일만 업로드 가능합니다.');
      setFile(null);
      return;
    }
    // 파일 크기 제한 (10MB)
    if (droppedFile.size > 10 * 1024 * 1024) {
      setError('파일 크기는 10MB 이하여야 합니다.');
      setFile(null);
      return;
    }
    setError('');
    setFile(droppedFile);
    onFileSelect(droppedFile);
  };

  const resetFile = () => {
    setFile(null);
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    onFileSelect(null);
  };

  return (
    <div className="file-uploader">
      <div 
        className={`drop-area ${file ? 'has-file' : ''}`}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        {!file ? (
          <div className="upload-container">
            <p>PDF 또는 TXT 파일을 드래그하거나 클릭하여 선택하세요</p>
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept=".pdf,.txt"
              style={{ display: 'none' }}
            />
            <button 
              type="button" 
              onClick={() => fileInputRef.current.click()}
              className="upload-button"
            >
              파일 선택
            </button>
          </div>
        ) : (
          <div className="file-info">
            <p className="file-name">{file.name}</p>
            <p className="file-size">{(file.size / 1024).toFixed(1)} KB</p>
            <button 
              type="button" 
              onClick={resetFile}
              className="remove-button"
            >
              파일 제거
            </button>
          </div>
        )}
      </div>
      {error && <div className="error-message">{error}</div>}
    </div>
  );
}

export default FileUploader;
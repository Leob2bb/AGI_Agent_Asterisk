import React, { useState } from 'react';
import FileUploader from './FileUploader';
import { dreamService } from '../services/api';
import { useNavigate } from 'react-router-dom';

function DreamEntryForm({ onSuccess, userId }) {
  const [formData, setFormData] = useState({
    title: '',
    date: new Date().toISOString().slice(0, 10),
    content: '',
  });

  const [dreamFile, setDreamFile] = useState(null);
  const [isManualEntry, setIsManualEntry] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileSelect = (file) => {
    setDreamFile(file);

    // 파일이 선택되면 수동 입력 비활성화
    if (file) {
      setIsManualEntry(false);
    } else {
      setIsManualEntry(true);
    }
  };

  const toggleEntryMethod = () => {
    if (!dreamFile) {
      setIsManualEntry(!isManualEntry);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      let result;

      if (dreamFile) {
        // 파일 업로드 방식
        result = await dreamService.submitDreamFile(formData, dreamFile, userId);
      } else {
        // 텍스트 직접 입력 방식
        result = await dreamService.submitDreamText(formData, userId);
      }

      // 폼 초기화
      setFormData({
        title: '',
        date: new Date().toISOString().slice(0, 10),
        content: '',
      });
      setDreamFile(null);
      setIsManualEntry(true);

      // 성공 콜백 호출
      if (onSuccess) onSuccess(result);

      // 페이지 이동 - 백엔드가 반환하는 값 확인
      if (result && result.id) {
        navigate(`/user/${userId}/dream/${result.dreamId}/analysis`);
      }

    } catch (err) {
      console.error('API Error:', err);
      if (err.message) {
        setError(err.message);
      } else {
        setError('꿈 분석 과정에서 오류가 발생했습니다. 다시 시도해주세요.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dream-form-container">
      <div className="entry-method-toggle">
        <button 
          type="button"
          className={`toggle-button ${isManualEntry ? 'active' : ''}`}
          onClick={() => toggleEntryMethod()}
          disabled={dreamFile !== null}
        >
          직접 입력
        </button>
        <button 
          type="button"
          className={`toggle-button ${!isManualEntry ? 'active' : ''}`}
          onClick={() => toggleEntryMethod()}
          disabled={dreamFile !== null}
        >
          파일 업로드
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">꿈 제목</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="date">날짜</label>
          <input
            type="date"
            id="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            required
          />
        </div>

        {isManualEntry ? (
          <div className="form-group">
            <label htmlFor="content">꿈 내용</label>
            <textarea
              id="content"
              name="content"
              value={formData.content}
              onChange={handleChange}
              rows={6}
              required={isManualEntry}
              placeholder="당신의 꿈을 상세히 적어주세요..."
            />
          </div>
        ) : (
          <FileUploader onFileSelect={handleFileSelect} />
        )}

        <button 
          type="submit" 
          className="submit-button"
          disabled={loading || (isManualEntry && !formData.content) || (!isManualEntry && !dreamFile)}
        >
          {loading ? '처리 중...' : '꿈 분석하기'}
        </button>
      </form>
    </div>
  );
}

export default DreamEntryForm;
// src/pages/AnalysisPage.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DreamChatAnalysis from '../components/DreamChatAnalysis';
import { dreamService } from '../services/api';

function AnalysisPage() {
  const { userId, dreamId } = useParams();
  const [dream, setDream] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDream = async () => {
      try {
        const result = await dreamService.getDream(userId, dreamId);
        setDream(result);
      } catch (err) {
        setError('꿈 정보를 불러오는데 실패했습니다.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDream();
  }, [userId, dreamId]);

  const handleBackToHome = () => {
    navigate(`/user/${userId}`);
  };

  if (loading) {
    return <div className="loading">정보를 불러오는 중...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="analysis-page">
      <div className="page-header">
        <button onClick={handleBackToHome} className="back-button">
          &larr; 홈으로 돌아가기
        </button>
        <h1>꿈 분석: {dream?.title}</h1>
        <p className="dream-date">{dream?.date}</p>
      </div>

      <div className="analysis-container">
        {/* dream 객체를 통째로 전달하여 DreamChatAnalysis에서 필요한 정보 활용 */}
        <DreamChatAnalysis dreamId={dreamId} userId={userId} initialDream={dream} />
      </div>
    </div>
  );
}

export default AnalysisPage;
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DreamChatAnalysis from '../components/DreamChatAnalysis';
import { dreamService, authService } from '../services/api';

function AnalysisPage() {
  const { dreamId } = useParams();
  const [dream, setDream] = useState(null);
  const [currentUser, setCurrentUser] = useState(null); // ✅ 추가
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDream = async () => {
      try {
        const user = authService.getCurrentUser();
        if (!user) {
          navigate('/login');
          return;
        }

        setCurrentUser(user); // ✅ 저장
        const result = await dreamService.getDream(user.username, dreamId);
        setDream(result);
      } catch (err) {
        setError('꿈 정보를 불러오는데 실패했습니다.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDream();
  }, [dreamId, navigate]);

  const handleBackToHome = () => {
    if (currentUser) {
      navigate(`/user/${currentUser.username}`);
    }
  };

  if (loading) return <div className="loading">정보를 불러오는 중...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="analysis-page">
      <div className="page-header">
        <button onClick={handleBackToHome} className="back-button">
          &larr; 홈으로 돌아가기
        </button>
        <h1>꿈 분석</h1>
        <p className="dream-date">{dream?.date}</p>
      </div>
      <div className="analysis-container">
        {currentUser && (
          <DreamChatAnalysis 
            dreamId={dreamId} 
            userId={currentUser.username} 
            initialDream={dream} 
          />
        )}
      </div>
    </div>
  );
}

export default AnalysisPage;

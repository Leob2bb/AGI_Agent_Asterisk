import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DreamEntryForm from '../components/DreamEntryForm';
import AnalysisResult from '../components/AnalysisResult';
import { dreamService, authService } from '../services/api';

function UserHomePage({ currentUser, setCurrentUser }) {
  const { userId } = useParams();
  const [dreamHistory, setDreamHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [showAnalysis, setShowAnalysis] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // 사용자의 꿈 기록 가져오기
    const fetchDreamHistory = async () => {
      try {
        const history = await dreamService.getDreamHistory(userId);
        setDreamHistory(history);
      } catch (error) {
        console.error('Failed to load dream history:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDreamHistory();
  }, [userId]);

  const handleLogout = () => {
    authService.logout();
    setCurrentUser(null);
    navigate('/login');
  };

  const handleDreamSubmit = async (result) => {
    // 분석 결과 표시
    setAnalysisResult(result);
    setShowAnalysis(true);

    // 꿈 기록 갱신
    try {
      const history = await dreamService.getDreamHistory(userId);
      setDreamHistory(history);
    } catch (error) {
      console.error('Failed to update dream history:', error);
    }
  };

  const handleBackToForm = () => {
    setShowAnalysis(false);
    setAnalysisResult(null);
  };

  // 권한 확인 - 현재 로그인한 사용자와 페이지 사용자가 일치하는지
  if (currentUser.username !== userId) {
    return <div className="error-message">접근 권한이 없습니다.</div>;
  }

  return (
    <div className="user-home">
      <header className="user-header">
        <h1>DreamInsight</h1>
        <div className="user-actions">
          <span className="welcome-message">안녕하세요, {currentUser.username}님</span>
          <button onClick={handleLogout} className="logout-button">로그아웃</button>
        </div>
      </header>

      {showAnalysis ? (
        <section className="analysis-section">
          <div className="section-header">
            <h2>꿈 분석 결과</h2>
            <button onClick={handleBackToForm} className="back-button">
              새 꿈 입력하기
            </button>
          </div>
          {analysisResult && (
            <AnalysisResult analysis={analysisResult} />
          )}
        </section>
      ) : (
        <section className="dream-entry-section">
          <h2>꿈 일기 작성</h2>
          <DreamEntryForm onSuccess={handleDreamSubmit} userId={userId} />
        </section>
      )}

      <section className="dream-history-section">
        <h2>나의 꿈 기록</h2>

        {loading ? (
          <div className="loading">로딩 중...</div>
        ) : dreamHistory.length > 0 ? (
          <ul className="dream-list">
            {dreamHistory.map(dream => (
              <li key={dream.id} className="dream-item">
                <div className="dream-info">
                  <h3>{dream.title}</h3>
                  <p className="dream-date">{new Date(dream.date).toLocaleDateString()}</p>
                </div>
                <button 
                  onClick={() => {
                    setAnalysisResult(dream.analysis);
                    setShowAnalysis(true);
                  }}
                  className="view-button"
                >
                  분석 결과 보기
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p className="empty-history">아직 기록된 꿈이 없습니다.</p>
        )}
      </section>
    </div>
  );
}

export default UserHomePage;
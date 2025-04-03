import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DreamEntryForm from '../components/DreamEntryForm';
import { dreamService, authService } from '../services/api';

function UserHomePage({ currentUser, setCurrentUser }) {
  const { userId } = useParams();
  const [dreamHistory, setDreamHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  

  const handleLogout = () => {
    authService.logout();
    setCurrentUser(null);
    navigate('/login');
  };

  const handleDreamSubmit = async (result) => {
    try {
      console.log("파일 업로드 결과:", result);

      // result에서 직접 ID 확인
      if (result) {
        const dreamId = result.id || result.dream_id || result.dreamId || result.created_at;
        if (dreamId) {
          console.log("꿈 ID 확인됨:", dreamId);
          // 분석 페이지로 직접 이동
          navigate(`/user/${userId}/dream/${dreamId}/analysis`);
          return;
        }
      }
      console.error('Invalid response:', result);
    } catch (error) {
      console.error('Failed to handle dream submission:', error);
    }
  };

  // 권한 확인 - 현재 로그인한 사용자와 페이지 사용자가 일치하는지
  if (currentUser.username !== userId) {
    return <div className="error-message">접근 권한이 없습니다.</div>;
  }

  return (
    <div className="user-home">
      <header className="user-header">
        <div className="site-title">
          <img src="/dreams-insight-logo.png" alt="DreamsInsight" className="logo-image-small" />
          <h1>DreamsInsight</h1> {/* 이 텍스트는 CSS로 숨겨지지만 접근성을 위해 유지 */}
        </div>
        <div className="user-actions">
          <span className="welcome-message">안녕하세요, {currentUser.username}님</span>
          <button onClick={handleLogout} className="logout-button">로그아웃</button>
        </div>
      </header>
      <section className="dream-entry-section">
        <h2>꿈 일기 작성</h2>
        <DreamEntryForm onSuccess={handleDreamSubmit} userId={userId} />
      </section>
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
                  onClick={() => navigate(`/user/${userId}/dream/${dream.id}`)}
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
import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DreamEntryForm from '../components/DreamEntryForm';
import { dreamService, authService } from '../services/api';

function UserHomePage({ currentUser, setCurrentUser }) {
  const { userId } = useParams();
  const navigate = useNavigate();

  const handleLogout = () => {
    authService.logout();
    setCurrentUser(null);
    navigate('/login');
  };

  const handleDreamSubmit = async (result) => {
    try {
      console.log("파일 업로드 결과:", result);
      if (result && result.id) {
        console.log("꿈 ID 확인됨:", result.id);
        navigate(`/user/${userId}/dream/${result.id}/analysis`);
        return;
      }
      console.error('Invalid response:', result);
    } catch (error) {
      console.error('Failed to handle dream submission:', error);
    }
  };

  if (currentUser.username !== userId) {
    return <div className="error-message">접근 권한이 없습니다.</div>;
  }

  return (
    <div className="user-home">
      <header className="user-header">
        <div className="site-title">
          <img src="/dreams-insight-logo.png" alt="DreamsInsight" className="logo-image-small" />
          <h1>DreamsInsight</h1>
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
    </div>
  );
}

export default UserHomePage;
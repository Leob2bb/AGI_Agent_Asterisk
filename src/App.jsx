import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import UserHomePage from './pages/UserHomePage';
import { authService } from './services/api';

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 페이지 로드 시 로그인 상태 확인
    const user = authService.getCurrentUser();
    setCurrentUser(user);
    setLoading(false);
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        <main>
          <Routes>
            <Route path="/login" element={currentUser ? <Navigate to={`/user/${currentUser.username}`} /> : <LoginPage setCurrentUser={setCurrentUser} />} />
            <Route path="/register" element={currentUser ? <Navigate to={`/user/${currentUser.username}`} /> : <RegisterPage setCurrentUser={setCurrentUser} />} />
            <Route path="/user/:userId" element={!currentUser ? <Navigate to="/login" /> : <UserHomePage currentUser={currentUser} setCurrentUser={setCurrentUser} />} />
            <Route path="/" element={<Navigate to={currentUser ? `/user/${currentUser.username}` : "/login"} />} />
          </Routes>
        </main>

        <footer className="app-footer">
          <p>© 2025 DreamInsight - AI 꿈 분석 해커톤 프로젝트</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
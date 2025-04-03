import React from 'react';
import { Link } from 'react-router-dom';
import LoginForm from '../components/LoginForm';

function LoginPage({ setCurrentUser }) {
  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="logo-header">
          <img src="/dreams-insight-logo.png" alt="DreamsInsight" className="logo-image-large" />
          <p className="tagline">AI 꿈 분석 서비스</p>
        </div>

        <h2>로그인</h2>
        <LoginForm setCurrentUser={setCurrentUser} />

        <div className="auth-switch">
          <p>
            계정이 없으신가요? <Link to="/register" className="auth-link">회원가입</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
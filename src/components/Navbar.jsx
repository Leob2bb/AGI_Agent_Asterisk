import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '../services/api';

function Navbar({ currentUser, setCurrentUser }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    authService.logout();
    setCurrentUser(null);
    navigate('/login');
  };

  return (
    <header className="app-header">
      <div className="logo">
        <Link to="/">DreamInsight</Link>
      </div>

      <nav>
        {currentUser ? (
          <div className="user-menu">
            <span>안녕하세요, {currentUser.username}님</span>
            <button onClick={handleLogout} className="logout-button">로그아웃</button>
          </div>
        ) : (
          <div className="auth-links">
            <Link to="/login">로그인</Link>
            <Link to="/register">회원가입</Link>
          </div>
        )}
      </nav>
    </header>
  );
}

export default Navbar;
import React from 'react';
import { Link } from 'react-router-dom';
import RegisterForm from '../components/RegisterForm';

function RegisterPage({ setCurrentUser }) {
  return (
    <div className="auth-page">
      <div className="auth-container">
        <h1>회원가입</h1>
        <RegisterForm setCurrentUser={setCurrentUser} />
        <div className="auth-switch">
          <p>
            이미 계정이 있으신가요? <Link to="/login">로그인</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;
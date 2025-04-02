import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/api';

function LoginForm({ setCurrentUser }) {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // LoginForm.jsx의 handleSubmit 함수 수정
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await authService.login(formData.username, formData.password);

      // 백엔드가 username을 직접 반환하지 않는 경우를 대비해 추가
      const userData = {
        ...result,
        username: result.username || formData.username // 백엔드 응답에 username이 없으면 입력값 사용
      };

      // 사용자 정보 저장
      localStorage.setItem('user', JSON.stringify(userData));
      setCurrentUser(userData);

      // 사용자 홈 페이지로 리다이렉션
      navigate(`/user/${userData.username}`);

    } catch (err) {
      // 오류 처리 코드...
      if (err.status === 401) {
        setError('아이디 또는 비밀번호가 일치하지 않습니다.');
      } else if (err.status === 404) {
        setError('존재하지 않는 사용자입니다.');
      } else {
        setError('로그인에 실패했습니다. 다시 시도해주세요.');
      }
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-form">
      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">아이디</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">비밀번호</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        <button 
          type="submit" 
          className="submit-button"
          disabled={loading}
        >
          {loading ? '로그인 중...' : '로그인'}
        </button>
      </form>
    </div>
  );
}

export default LoginForm;
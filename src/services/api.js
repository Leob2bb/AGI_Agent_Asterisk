// src/services/api.js
const API_BASE_URL = "https://agi-agent-asterisk-render.onrender.com";

export const authService = {
  // 로그인
  login: async (username, password) => {
    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });
      if (!response.ok) {
        const error = new Error('Login failed');
        error.status = response.status;
        throw error;
      }
      return await response.json();
    } catch (error) {
      console.error('Auth API Error:', error);
      throw error;
    }
  },

  // 회원가입
  register: async (username, password) => {
    try {
      const response = await fetch(`${API_BASE_URL}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });
      if (!response.ok) {
        const error = new Error('Registration failed');
        error.status = response.status;
        throw error;
      }
      return await response.json();
    } catch (error) {
      console.error('Auth API Error:', error);
      throw error;
    }
  },

  // 로그아웃
  logout: () => {
    localStorage.removeItem('user');
  },

  // 현재 로그인한 사용자 가져오기
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch (error) {
      return null;
    }
  }
};

export const dreamService = {
  // 직접 입력한 꿈 내용 제출
  submitDreamText: async (dreamData, userId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/user/${userId}/dream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(dreamData)
      });
      if (!response.ok) {
        throw new Error('Failed to submit dream text');
      }
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  // 파일 업로드로 꿈 내용 제출
  submitDreamFile: async (dreamData, file, userId) => {
    try {
      // FormData 객체만 생성하고 파일 내용 읽기 시도하지 않음
      const formData = new FormData();
      formData.append('title', dreamData.title);
      formData.append('date', dreamData.date);
      formData.append('file', file);

      const response = await fetch(`${API_BASE_URL}/user/${userId}/dream/file`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Accept': 'application/json'
        },
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const error = new Error(errorData.message || 'Failed to upload dream file');
        error.status = response.status;
        throw error;
      }
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  // 사용자의 꿈 기록 가져오기
  getDreamHistory: async (userId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/user/${userId}/dreams`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (!response.ok) {
        throw new Error('Failed to get dream history');
      }
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  // 특정 꿈 정보 가져오기
  getDream: async (userId, dreamId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/user/${userId}/dream/${dreamId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (!response.ok) {
        throw new Error('Failed to get dream');
      }
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  // 초기 분석 결과 가져오기
  getDreamAnalysis: async (userId, dreamId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/user/${userId}/dream/${dreamId}/analysis`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (!response.ok) {
        throw new Error('Failed to get dream analysis');
      }
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  // 채팅 메시지 전송 및 응답 받기
  sendChatMessage: async (userId, dreamId, message) => {
    try {
      const response = await fetch(`${API_BASE_URL}/user/${userId}/dream/${dreamId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ message })
      });
      if (!response.ok) {
        throw new Error('Failed to get chat response');
      }
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }
};
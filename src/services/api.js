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

      const result = await response.json();

      if (!response.ok) {
        const error = new Error(result.message || 'Login failed');
        error.status = response.status;
        throw error;
      }

      // 사용자 정보와 토큰 저장
      const userData = {
        id: result.id || username, // id가 없으면 username을 id로 사용
        username: result.username || username
      };
      localStorage.setItem('user', JSON.stringify(userData));
      if (result.token) {
        localStorage.setItem('token', result.token);
      }

      return userData;
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
    localStorage.removeItem('token'); // 토큰도 함께 제거
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
  },

  // 현재 토큰 가져오기
  getToken: () => {
    return localStorage.getItem('token');
  }
};

export const dreamService = {
  // 직접 입력한 꿈 내용 제출
  submitDreamText: async (dreamData, userId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/user/${userId}/dream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : ''
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
      const formData = new FormData();
      formData.append('title', dreamData.title);
      formData.append('date', dreamData.date);
      formData.append('file', file);
      formData.append('user_id', userId);

      const response = await fetch(`${API_BASE_URL}/user/${userId}/dream/file`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error('Failed to submit dream file');
      }
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  // 특정 꿈 정보 가져오기 - created_at을 사용하도록 수정
  getDream: async (userId, dreamIdOrCreatedAt) => {
    try {
      // created_at 형식인지 확인 (ISO8601 형식이면 created_at으로 간주)
      const isCreatedAt = typeof dreamIdOrCreatedAt === 'string' && 
                          dreamIdOrCreatedAt.includes('T') && 
                          !isNaN(new Date(dreamIdOrCreatedAt).getTime());

      // URL 경로 결정 (ISO8601 형식이면 created_at 경로 사용)
      const url = isCreatedAt 
        ? `${API_BASE_URL}/user/${userId}/dream/${encodeURIComponent(dreamIdOrCreatedAt)}`
        : `${API_BASE_URL}/user/${userId}/dream/${dreamIdOrCreatedAt}`;

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (!response.ok) {
        throw new Error('Failed to get dream');
      }
      const data = await response.json();
      // id 필드가 없으면 created_at을 id로 추가
      if (!data.id && data.created_at) {
        data.id = data.created_at;
      }
      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  // 초기 분석 결과 가져오기 - created_at을 사용하도록 수정
  getDreamAnalysis: async (userId, dreamIdOrCreatedAt) => {
    try {
      const token = localStorage.getItem('token');
      // created_at 형식인지 확인 (ISO8601 형식이면 created_at으로 간주)
      const isCreatedAt = typeof dreamIdOrCreatedAt === 'string' && 
                          dreamIdOrCreatedAt.includes('T') && 
                          !isNaN(new Date(dreamIdOrCreatedAt).getTime());

      // URL 경로 결정
      const url = isCreatedAt 
        ? `${API_BASE_URL}/user/${userId}/dream/${encodeURIComponent(dreamIdOrCreatedAt)}/analysis`
        : `${API_BASE_URL}/user/${userId}/dream/${dreamIdOrCreatedAt}/analysis`;

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : ''
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

  // 채팅 메시지 전송 및 응답 받기 - created_at을 사용하도록 수정
  sendChatMessage: async (userId, dreamIdOrCreatedAt, message) => {
    try {
      const token = localStorage.getItem('token');
      // created_at 형식인지 확인 (ISO8601 형식이면 created_at으로 간주)
      const isCreatedAt = typeof dreamIdOrCreatedAt === 'string' && 
                          dreamIdOrCreatedAt.includes('T') && 
                          !isNaN(new Date(dreamIdOrCreatedAt).getTime());

      // URL 경로 결정
      const url = isCreatedAt 
        ? `${API_BASE_URL}/user/${userId}/dream/${encodeURIComponent(dreamIdOrCreatedAt)}/chat`
        : `${API_BASE_URL}/user/${userId}/dream/${dreamIdOrCreatedAt}/chat`;

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : ''
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
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
      // FormData 객체만 생성하고 파일 내용 읽기 시도하지 않음
      const formData = new FormData();
      formData.append('title', dreamData.title);
      formData.append('date', dreamData.date);
      formData.append('file', file);

      const response = await fetch(`${API_BASE_URL}/user/${userId}/dream`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json'
        },
        body: formData
      });

      // 테스트를 위한 모의 응답 데이터
      return {
        dreamId: new Date().toISOString(),
        title: dreamData.title,
        date: dreamData.date,
        content: "늦은 시간까지 과방에서 민규 형, 태빈이와 함께 해커톤을 위한 프로젝트를 진행하고 있었다. 코드를 새로 짤 때마다 오류가 많이 발생해서 너무 짜증났다. 그렇게 짜증내고 있었는데 갑자기 노트북 화면에서 행렬 요소들이 튀어나와서 나를 덮쳤다. 너무 놀라서 당황했고 그러다 깜짝 놀라서 꿈에서 깼다",
        initialAnalysis: "이 꿈은 프로젝트 작업 중의 스트레스와 압박감이 표현된 것으로 보입니다. 노트북 화면에서 행렬 요소들이 튀어나오는 장면은 코딩 문제가 압도적으로 느껴지는 감정을 상징합니다. 팀원들과 함께 있는 상황은 협업 과정에서의 책임감과 부담감을 나타냅니다.",
        emotions: ["스트레스", "불안", "압박감", "당혹감"],
        symbols: [
          { name: "노트북", meaning: "일과 책임" },
          { name: "행렬", meaning: "복잡한 문제" },
          { name: "과방", meaning: "작업 공간" }
        ],
        created_at: new Date().toISOString()
      };
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
          'Content-Type': 'application/json'
        }
      });
      if (!response.ok) {
        throw new Error('Failed to get dream history');
      }
      const data = await response.json();
      // 'dreams' 키 아래의 배열을 반환하고, 각 꿈 항목에 created_at을 id로 사용
      const dreams = (data.dreams || []).map(dream => ({
        ...dream,
        id: dream.id || dream.created_at // id가 없으면 created_at을 id로 사용
      }));
      return dreams;
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
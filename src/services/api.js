// src/services/api.js
const API_BASE_URL = "https://bf7c9bc2-2560-4704-a3a0-f9c4d3a9c78a-00-7ew1tl3q0m4b.sisko.replit.dev";

  // src/services/api.js의 authService 부분만 수정

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

    // 나머지 함수들은 그대로...

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
          'Content-Type': 'application/json'
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
  // src/services/api.js의 submitDreamFile 함수 수정
  submitDreamFile: async (dreamData, file, userId) => {
    try {
      // 파일 타입에 따른 처리 (파일 내용 미리 읽기)
      let fileContent = null;

      if (file.type === 'text/plain') {
        // TXT 파일은 내용을 미리 읽어서 전송
        fileContent = await new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = (e) => resolve(e.target.result);
          reader.onerror = (e) => reject(e);
          reader.readAsText(file);
        });
      }

      // FormData 객체 생성
      const formData = new FormData();
      formData.append('title', dreamData.title);
      formData.append('date', dreamData.date);
      formData.append('file', file);

      // 텍스트 파일의 경우 미리 읽은 내용도 함께 전송
      if (fileContent) {
        formData.append('fileContent', fileContent);
      }

      const response = await fetch(`${API_BASE_URL}/user/${userId}/dream/file`, {
        method: 'POST',
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
      const response = await fetch(`${API_BASE_URL}/user/${userId}/dreams`);

      if (!response.ok) {
        throw new Error('Failed to get dream history');
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }
};
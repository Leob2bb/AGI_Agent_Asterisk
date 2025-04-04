 const API_BASE_URL = "https://agi-agent-asterisk-render.onrender.com";

 export const authService = {
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

       const userData = {
         id: result.id || username,
         username: result.username || username
       };
       localStorage.setItem('user', JSON.stringify(userData));
       if (result.access_token) {
         localStorage.setItem('token', result.access_token);
       }

       return userData;
     } catch (error) {
       console.error('Auth API Error:', error);
       throw error;
     }
   },

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

   logout: () => {
     localStorage.removeItem('user');
     localStorage.removeItem('token');
   },

   getCurrentUser: () => {
     const userStr = localStorage.getItem('user');
     if (!userStr) return null;
     try {
       return JSON.parse(userStr);
     } catch (error) {
       return null;
     }
   },

   getToken: () => {
     return localStorage.getItem('token');
   }
 };

 export const dreamService = {
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

   submitDreamFile: async (dreamData, file, userId) => {
     try {
       const formData = new FormData();
       formData.append('title', dreamData.title);
       formData.append('date', dreamData.date);
       formData.append('file', file);

       if (dreamData.content) {
         formData.append('content', dreamData.content);
       }

       console.log("FormData 내용 확인:", {
         title: dreamData.title,
         date: dreamData.date,
         fileSize: file.size,
         fileName: file.name
       });

       const response = await fetch(`${API_BASE_URL}/user/${userId}/dream/file`, {
         method: 'POST',
         headers: {},
         body: formData
       });

       console.log("서버 응답 상태:", response.status);

       if (!response.ok) {
         const errorData = await response.json().catch(() => ({}));
         console.error("서버 오류 응답:", errorData);
         throw new Error(errorData.error || `서버 오류: ${response.status}`);
       }

       return await response.json();
     } catch (error) {
       console.error('파일 업로드 API 오류:', error);
       throw error;
     }
   },

   // api.js
   getDream: async (userId, dreamId) => {
     try {
       const url = `${API_BASE_URL}/user/${userId}/dream/${dreamId}`;
       console.log('Dream 조회 URL:', url);

       const response = await fetch(url, {
         method: 'GET',
         headers: {
           'Content-Type': 'application/json'
         }
       });

       console.log('응답 상태:', response.status);

       if (!response.ok) {
         const errorText = await response.text();
         console.error('에러 응답:', errorText);
         throw new Error(`Failed to get dream: ${errorText}`);
       }

       return await response.json();
     } catch (error) {
       console.error('Detailed API Error:', error);
       throw error;
     }
   },

   getDreamAnalysis: async (userId, dreamId) => {
     try {
       const url = `${API_BASE_URL}/user/${userId}/dream/${dreamId}/analysis`;

       const response = await fetch(url, {
         method: 'GET',
         headers: {
           'Content-Type': 'application/json'
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

   sendChatMessage: async (userId, dreamId, message) => {
     try {
       const url = `${API_BASE_URL}/user/${userId}/dream/${dreamId}/chat`;

       const response = await fetch(url, {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json'
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
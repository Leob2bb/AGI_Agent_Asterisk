// src/components/DreamChatAnalysis.jsx
import React, { useState, useEffect, useRef } from 'react';

function DreamChatAnalysis({ dreamId, userId }) {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // 초기 메시지 설정
  useEffect(() => {
    const fetchInitialAnalysis = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/user/${userId}/dream/${dreamId}/analysis`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to get initial analysis');
        }

        const data = await response.json();
        setMessages([
          {
            type: 'analysis',
            content: data.initialAnalysis,
            timestamp: new Date()
          }
        ]);
      } catch (error) {
        console.error('Error fetching initial analysis:', error);
        setMessages([
          {
            type: 'error',
            content: '초기 분석을 불러오는데 실패했습니다. 다시 시도해주세요.',
            timestamp: new Date()
          }
        ]);
      }
    };

    fetchInitialAnalysis();
  }, [userId, dreamId]);

  // 자동 스크롤
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMessage = {
      type: 'user',
      content: inputText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setLoading(true);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/user/${userId}/dream/${dreamId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ message: userMessage.content })
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      setMessages(prev => [...prev, {
        type: 'analysis',
        content: data.response,
        timestamp: new Date()
      }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        type: 'error',
        content: '메시지 전송 중 오류가 발생했습니다. 다시 시도해주세요.',
        timestamp: new Date()
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dream-chat-container">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            {msg.type === 'analysis' && (
              <div className="chat-avatar">AI</div>
            )}
            <div className="message-content">{msg.content}</div>
            <div className="message-time">
              {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message loading">
            <div className="loading-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSendMessage} className="chat-input-form">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="꿈에 대해 더 궁금한 점을 질문해보세요..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !inputText.trim()}>
          {/* 화살표 아이콘은 CSS에서 ::after 가상 요소로 처리됨 */}
        </button>
      </form>
    </div>
  );
}

export default DreamChatAnalysis;
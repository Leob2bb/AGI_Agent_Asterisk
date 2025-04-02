import React, { useState, useEffect, useRef } from 'react';

function DreamChatAnalysis({ dreamId, userId, initialDream }) {
  const [messages, setMessages] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // 초기 분석 데이터 가져오기
  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/user/${userId}/dream/${dreamId}/analysis`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to get analysis');
        }

        const data = await response.json();
        setAnalysis(data);

        // 초기 메시지로 요약된 분석 내용 추가
        setMessages([
          {
            type: 'analysis',
            content: data.interpretation || data.initialAnalysis,
            timestamp: new Date()
          }
        ]);
      } catch (error) {
        console.error('Error fetching analysis:', error);
        setMessages([
          {
            type: 'error',
            content: '분석 정보를 불러오는데 실패했습니다. 다시 시도해주세요.',
            timestamp: new Date()
          }
        ]);
      }
    };

    fetchAnalysis();
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
    <div className="dream-analysis-container">
      {/* 감정 태그와 주요 상징 표시 영역 */}
      {analysis && (
        <div className="analysis-overview">
          {analysis.emotions && analysis.emotions.length > 0 && (
            <div className="emotions-container">
              <h4>감정 분석</h4>
              <div className="emotion-tags">
                {analysis.emotions.map((emotion, index) => (
                  <span key={index} className="emotion-tag">{emotion}</span>
                ))}
              </div>
            </div>
          )}

          {analysis.symbols && analysis.symbols.length > 0 && (
            <div className="symbols-container">
              <h4>주요 상징</h4>
              <div className="symbol-tags">
                {analysis.symbols.map((symbol, index) => (
                  <span key={index} className="symbol-tag">{symbol.name}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* 채팅 인터페이스 */}
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
          <button type="submit" disabled={loading || !inputText.trim()}></button>
        </form>
      </div>
    </div>
  );
}

export default DreamChatAnalysis;
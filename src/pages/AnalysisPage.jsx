import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import AnalysisResult from '../components/AnalysisResult';
import { dreamService, authService } from '../services/api';

function AnalysisPage() {
  const { userId, analysisId } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const currentUser = authService.getCurrentUser();

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const result = await dreamService.getAnalysis(userId, analysisId);
        setAnalysis(result);
      } catch (err) {
        setError('분석 결과를 불러오는데 실패했습니다.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [userId, analysisId]);

  // 권한 확인
  if (currentUser.username !== userId) {
    return <div className="error-message">접근 권한이 없습니다.</div>;
  }

  if (loading) {
    return <div className="loading">분석 결과 로딩 중...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="analysis-page">
      <div className="page-navigation">
        <Link to={`/user/${userId}`} className="back-link">
          &larr; 마이 페이지로 돌아가기
        </Link>
      </div>

      <h1>꿈 분석 결과</h1>

      {analysis && (
        <AnalysisResult analysis={analysis} />
      )}
    </div>
  );
}

export default AnalysisPage;
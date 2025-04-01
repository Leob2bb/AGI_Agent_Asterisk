import React from 'react';

function AnalysisResult({ analysis }) {
  return (
    <div className="analysis-result">
      <div className="result-header">
        <h3>{analysis.title}</h3>
        <p className="dream-date">{new Date(analysis.date).toLocaleDateString()}</p>
      </div>

      <div className="result-content">
        <div className="dream-content">
          <h4>꿈 내용</h4>
          <p>{analysis.content}</p>
        </div>

        <div className="emotions">
          <h4>감정 분석</h4>
          <div className="emotion-tags">
            {analysis.emotions?.map((emotion, index) => (
              <span key={index} className="emotion-tag">{emotion}</span>
            ))}
          </div>
        </div>

        <div className="symbols">
          <h4>상징 분석</h4>
          <ul className="symbol-list">
            {analysis.symbols?.map((symbol, index) => (
              <li key={index} className="symbol-item">
                <span className="symbol-name">{symbol.name}</span>: {symbol.meaning}
              </li>
            ))}
          </ul>
        </div>

        <div className="interpretation">
          <h4>종합 해석</h4>
          <p>{analysis.interpretation}</p>
        </div>

        <div className="recommendations">
          <h4>추천 사항</h4>
          <ul className="recommendation-list">
            {analysis.recommendations?.map((recommendation, index) => (
              <li key={index}>{recommendation}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default AnalysisResult;
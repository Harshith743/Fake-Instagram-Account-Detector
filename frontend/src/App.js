import './App.css';
import React, { useState, useEffect, useRef } from 'react';

function App() {
  const [username, setUsername] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const checkAccount = async () => {
    if (!username.trim()) {
      setResult({ error: 'Please enter a username' });
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(
        `http://localhost:5000/predict?username=${encodeURIComponent(username)}`
      );

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      if (!data.prediction) {
        throw new Error('Invalid response format');
      }

      setResult(data);
    } catch (error) {
      setResult({
        error: error.message || 'Analysis failed. Please try again.'
      });
    } finally {
      setLoading(false);
    }
  };

  const clearError = () => {
    if (result?.error) setResult(null);
  };

  return (
    <div className="container">
      <div className="glow"></div>
      <div className="card">
        <header>
          <h1 className="title">Fake Instagram Account Detector</h1>
          <p className="subtitle">Check if an Instagram account is genuine or fake</p>
        </header>

        <div className="input-wrapper">
          <input
            ref={inputRef}
            type="text"
            value={username}
            onChange={(e) => {
              setUsername(e.target.value);
              clearError();
            }}
            placeholder="@username"
            className="input"
            onKeyDown={(e) => e.key === 'Enter' && checkAccount()}
            disabled={loading}
            autoComplete="off"
          />
        </div>

        <button
          onClick={checkAccount}
          disabled={!username.trim() || loading}
          className="button"
          aria-busy={loading}
        >
          {loading ? (
            <>
              <span className="loading-spinner"></span>
              Analyzing...
            </>
          ) : (
            '🔍 Analyze Account'
          )}
        </button>

        {result && (
          <div className="result">
            {result.error ? (
              <p className="error">{result.error}</p>
            ) : (
              <>
                <p
                  className={`prediction ${
                    result.prediction === 'FAKE'
                      ? 'prediction-fake'
                      : 'prediction-real'
                  }`}
                >
                  {result.prediction === 'FAKE'
                    ? 'Fake Account Detected'
                    : 'Genuine Account'}
                  {result.confidence && (
                    <span className="confidence">
                      {' '}
                      ({result.confidence}% confidence)
                    </span>
                  )}
                </p>
                <div className="tip">
                  {result.prediction === 'FAKE' ? (
                    'Tip: This account shows characteristics commonly associated with fake profiles.'
                  ) : (
                    'Tip: This account appears genuine based on our analysis.'
                  )}
                </div>
              </>
            )}
          </div>
        )}

        <p className="footer">
          Note: This tool analyzes public account characteristics only.
        </p>
      </div>
    </div>
  );
}

export default App;
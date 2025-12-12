import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { WaterBackground, Particles, GlassCard, Button, SentimentEmoji } from '../components';
import { useAuth } from '../context/AuthContext';
import { analyzeService } from '../services/analyze';
import type { AnalysisResponse } from '../services/types';
import './DashboardPage.css';

export const DashboardPage = () => {
    const navigate = useNavigate();
    const { user, logout } = useAuth();

    const [text, setText] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<AnalysisResponse | null>(null);
    const [error, setError] = useState('');

    const handleAnalyze = async () => {
        if (!text.trim()) {
            setError('Please enter some text to analyze');
            return;
        }

        if (text.length < 20) {
            setError('Please enter at least 20 characters for better analysis');
            return;
        }

        setError('');
        setLoading(true);
        setResult(null);

        try {
            const response = await analyzeService.analyzeText(text);
            setResult(response);
        } catch (err: unknown) {
            const error = err as { response?: { data?: { detail?: string } } };
            setError(error.response?.data?.detail || 'Analysis failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = async () => {
        await logout();
        navigate('/');
    };

    const handleClear = () => {
        setText('');
        setResult(null);
        setError('');
    };

    const getTopScores = () => {
        if (!result?.hf_scores) return [];
        return Object.entries(result.hf_scores)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 5);
    };

    return (
        <div className="dashboard">
            <WaterBackground variant="dashboard" intensity="low" />
            <Particles count={25} color="emerald" />

            {/* Header */}
            <header className="dashboard__header">
                <div className="dashboard__header-brand">
                    <span className="dashboard__logo">◈</span>
                    <span className="dashboard__logo-text">Hybrid Analyzer</span>
                </div>
                <div className="dashboard__header-user">
                    <span className="dashboard__user-email">{user?.email}</span>
                    <Button variant="ghost" size="sm" onClick={handleLogout}>
                        Logout
                    </Button>
                </div>
            </header>

            {/* Main Content */}
            <main className="dashboard__main">
                <div className="dashboard__content">
                    {/* Left Panel - Input */}
                    <section className="dashboard__input-section">
                        <GlassCard variant="dusk" className="dashboard__input-card">
                            <h2 className="dashboard__section-title">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                                    <polyline points="14 2 14 8 20 8" />
                                    <line x1="16" y1="13" x2="8" y2="13" />
                                    <line x1="16" y1="17" x2="8" y2="17" />
                                    <polyline points="10 9 9 9 8 9" />
                                </svg>
                                Input Text
                            </h2>

                            <div className="dashboard__textarea-wrapper">
                                <textarea
                                    className="dashboard__textarea"
                                    placeholder="Paste your article, news, or any text here for AI-powered analysis..."
                                    value={text}
                                    onChange={(e) => setText(e.target.value)}
                                    disabled={loading}
                                />
                                <span className="dashboard__char-count">
                                    {text.length} characters
                                </span>
                            </div>

                            {error && (
                                <div className="dashboard__error">
                                    {error}
                                </div>
                            )}

                            <div className="dashboard__actions">
                                <Button
                                    size="lg"
                                    glow
                                    loading={loading}
                                    onClick={handleAnalyze}
                                    disabled={!text.trim()}
                                    className="dashboard__analyze-btn"
                                >
                                    {loading ? 'Analyzing...' : 'Analyze Text'}
                                    {!loading && (
                                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                            <circle cx="11" cy="11" r="8" />
                                            <path d="M21 21l-4.35-4.35" />
                                        </svg>
                                    )}
                                </Button>
                                <Button variant="secondary" onClick={handleClear} disabled={loading}>
                                    Clear
                                </Button>
                            </div>
                        </GlassCard>
                    </section>

                    {/* Right Panel - Results */}
                    <section className="dashboard__results-section">
                        {!result && !loading && (
                            <div className="dashboard__empty-state">
                                <h3>Ready to Analyze</h3>
                                <p>Enter text on the left and click "Analyze Text" to get AI-powered insights.</p>
                            </div>
                        )}

                        {loading && (
                            <div className="dashboard__loading-state">
                                <div className="dashboard__loading-spinner" />
                                <h3>Analyzing your text...</h3>
                                <p>Using HuggingFace + Gemini AI</p>
                            </div>
                        )}

                        {result && (
                            <div className="dashboard__results-grid">
                                {/* Category Card */}
                                <GlassCard variant="emerald" floating className="dashboard__result-card">
                                    <h3 className="dashboard__card-title">Category</h3>
                                    <div className="dashboard__category-badge">
                                        {result.category}
                                    </div>
                                </GlassCard>

                                {/* Sentiment Card */}
                                <GlassCard variant="emerald" floating className="dashboard__result-card">
                                    <h3 className="dashboard__card-title">Sentiment</h3>
                                    <SentimentEmoji sentiment={result.tone} size="lg" />
                                </GlassCard>

                                {/* Confidence Scores */}
                                <GlassCard variant="emerald" floating className="dashboard__result-card dashboard__result-card--wide">
                                    <h3 className="dashboard__card-title">Confidence Scores</h3>
                                    <div className="dashboard__scores">
                                        {getTopScores().map(([category, score]) => (
                                            <div key={category} className="dashboard__score-item">
                                                <div className="dashboard__score-header">
                                                    <span className="dashboard__score-label">{category}</span>
                                                    <span className="dashboard__score-value">{(score * 100).toFixed(1)}%</span>
                                                </div>
                                                <div className="dashboard__score-bar">
                                                    <div
                                                        className="dashboard__score-fill"
                                                        style={{ width: `${score * 100}%` }}
                                                    />
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </GlassCard>

                                {/* Summary */}
                                <GlassCard variant="emerald" floating className="dashboard__result-card dashboard__result-card--full">
                                    <h3 className="dashboard__card-title">AI Summary</h3>
                                    <p className="dashboard__summary-text">{result.summary}</p>
                                </GlassCard>

                                {/* Performance Metrics */}
                                <GlassCard variant="bark" className="dashboard__result-card dashboard__result-card--full dashboard__metrics-card">
                                    <h3 className="dashboard__card-title">Performance Metrics</h3>
                                    <div className="dashboard__metrics">
                                        <div className="dashboard__metric">
                                            <span className="dashboard__metric-label">HuggingFace</span>
                                            <span className="dashboard__metric-value">{result.meta.hf_latency_ms}ms</span>
                                        </div>
                                        <div className="dashboard__metric">
                                            <span className="dashboard__metric-label">Gemini</span>
                                            <span className="dashboard__metric-value">{result.meta.gemini_latency_ms}ms</span>
                                        </div>
                                        <div className="dashboard__metric dashboard__metric--total">
                                            <span className="dashboard__metric-label">Total</span>
                                            <span className="dashboard__metric-value">{result.meta.total_execution_ms}ms</span>
                                        </div>
                                    </div>
                                </GlassCard>
                            </div>
                        )}
                    </section>
                </div>
            </main>
        </div>
    );
};

export default DashboardPage;

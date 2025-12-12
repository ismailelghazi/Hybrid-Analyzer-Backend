import { useNavigate } from 'react-router-dom';
import { WaterBackground, Particles, Button, GlassCard } from '../components';
import { useAuth } from '../context/AuthContext';
import './LandingPage.css';

export const LandingPage = () => {
    const navigate = useNavigate();
    const { isAuthenticated } = useAuth();

    const handleGetStarted = () => {
        if (isAuthenticated) {
            navigate('/dashboard');
        } else {
            navigate('/auth');
        }
    };

    return (
        <div className="landing">
            <WaterBackground variant="landing" intensity="medium" />
            <Particles count={40} color="emerald" />

            {/* Hero Section */}
            <section className="landing__hero">
                <div className="landing__hero-content">
                    <span className="landing__badge">AI-Powered Analysis</span>
                    <h1 className="landing__title">
                        Analyze Media with
                        <span className="landing__title-accent"> AI Precision</span>
                    </h1>
                    <p className="landing__subtitle">
                        Harness the power of HuggingFace and Google Gemini to classify,
                        summarize, and understand the sentiment of any text instantly.
                    </p>
                    <div className="landing__cta-group">
                        <Button
                            size="lg"
                            glow
                            onClick={handleGetStarted}
                            className="landing__cta-primary"
                        >
                            Get Started

                        </Button>
                        <Button
                            variant="secondary"
                            size="lg"
                            onClick={() => document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })}
                        >
                            Learn More
                        </Button>
                    </div>
                </div>

                {/* Floating preview card */}
                <div className="landing__preview">
                    <GlassCard variant="emerald" floating className="landing__preview-card">
                        <div className="landing__preview-header">
                            <div className="landing__preview-dot landing__preview-dot--red" />
                            <div className="landing__preview-dot landing__preview-dot--yellow" />
                            <div className="landing__preview-dot landing__preview-dot--green" />
                        </div>
                        <div className="landing__preview-content">
                            <div className="landing__preview-result">
                                <span className="landing__preview-label">Category</span>
                                <span className="landing__preview-badge">Technology</span>
                            </div>
                            <div className="landing__preview-result">
                                <span className="landing__preview-label">Sentiment</span>
                                <span className="landing__preview-sentiment">Positive</span>
                            </div>
                            <div className="landing__preview-result">
                                <span className="landing__preview-label">Confidence</span>
                                <div className="landing__preview-bar">
                                    <div className="landing__preview-bar-fill" style={{ width: '92%' }} />
                                </div>
                            </div>
                        </div>
                    </GlassCard>
                </div>
            </section>

            {/* Features Section */}
            <section id="features" className="landing__features">
                <div className="landing__features-container">
                    <h2 className="landing__features-title">Powerful Features</h2>
                    <p className="landing__features-subtitle">
                        Everything you need to understand and analyze text content
                    </p>

                    <div className="landing__features-grid">
                        <GlassCard variant="bark" floating className="landing__feature-card">
                            <h3 className="landing__feature-title">Zero-Shot Classification</h3>
                            <p className="landing__feature-description">
                                Classify text into any category without prior training using
                                state-of-the-art HuggingFace models.
                            </p>
                        </GlassCard>

                        <GlassCard variant="bark" floating className="landing__feature-card">
                            <h3 className="landing__feature-title">AI Summarization</h3>
                            <p className="landing__feature-description">
                                Get concise, intelligent summaries powered by Google Gemini's
                                advanced language understanding.
                            </p>
                        </GlassCard>

                        <GlassCard variant="bark" floating className="landing__feature-card">
                            <h3 className="landing__feature-title">Sentiment Analysis</h3>
                            <p className="landing__feature-description">
                                Understand the emotional tone of any text with accurate
                                positive, negative, or neutral detection.
                            </p>
                        </GlassCard>

                        <GlassCard variant="bark" floating className="landing__feature-card">
                            <h3 className="landing__feature-title">Real-time Metrics</h3>
                            <p className="landing__feature-description">
                                Track performance with detailed latency metrics for every
                                analysis request.
                            </p>
                        </GlassCard>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="landing__footer">
                <div className="landing__footer-content">
                    <div className="landing__footer-brand">
                        <span className="landing__footer-logo">Hybrid Analyzer</span>
                        <p className="landing__footer-tagline">
                            AI-powered text analysis combining HuggingFace and Google Gemini for intelligent insights.
                        </p>
                        <div className="landing__footer-social">
                            <a href="https://github.com" className="landing__footer-social-link" aria-label="GitHub">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
                                </svg>
                            </a>
                            <a href="https://linkedin.com" className="landing__footer-social-link" aria-label="LinkedIn">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
                                </svg>
                            </a>
                            <a href="https://twitter.com" className="landing__footer-social-link" aria-label="Twitter">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z" />
                                </svg>
                            </a>
                        </div>
                    </div>




                </div>

                <div className="landing__footer-bottom">
                    <p>© 2025 <span>Hybrid Analyzer</span>. Built with FastAPI, React, and AI.</p>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;

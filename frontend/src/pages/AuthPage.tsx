import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { WaterBackground, Particles, GlassCard, Button, Input } from '../components';
import { useAuth } from '../context/AuthContext';
import './AuthPage.css';

type AuthMode = 'login' | 'register';

export const AuthPage = () => {
    const navigate = useNavigate();
    const { login, register, isLoading } = useAuth();

    const [mode, setMode] = useState<AuthMode>('login');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        if (!email || !password) {
            setError('Please fill in all fields');
            return;
        }

        if (mode === 'register' && password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        if (password.length < 6) {
            setError('Password must be at least 6 characters');
            return;
        }

        setLoading(true);

        try {
            if (mode === 'login') {
                await login(email, password);
            } else {
                await register(email, password);
            }
            navigate('/dashboard');
        } catch (err: unknown) {
            const error = err as { response?: { data?: { detail?: string } } };
            setError(error.response?.data?.detail || 'An error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const toggleMode = () => {
        setMode(mode === 'login' ? 'register' : 'login');
        setError('');
        setConfirmPassword('');
    };

    return (
        <div className="auth">
            <WaterBackground variant="auth" intensity="low" />
            <Particles count={30} color="mixed" />

            <div className="auth__container">
                <GlassCard variant="bark" className="auth__card">
                    {/* Logo / Brand */}
                    <div className="auth__header">
                        <div className="auth__logo">
                            <span className="auth__logo-icon">◈</span>
                            <span className="auth__logo-text">Hybrid Analyzer</span>
                        </div>
                        <h1 className="auth__title">
                            {mode === 'login' ? 'Welcome Back' : 'Create Account'}
                        </h1>
                        <p className="auth__subtitle">
                            {mode === 'login'
                                ? 'Sign in to continue analyzing'
                                : 'Start your AI-powered analysis journey'}
                        </p>
                    </div>

                    {/* Error Message */}
                    {error && (
                        <div className="auth__error">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <circle cx="12" cy="12" r="10" />
                                <path d="M12 8v4M12 16h.01" />
                            </svg>
                            {error}
                        </div>
                    )}

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="auth__form">
                        <Input
                            type="email"
                            label="Email"
                            placeholder="you@example.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            autoComplete="email"
                            icon={
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                                    <polyline points="22,6 12,13 2,6" />
                                </svg>
                            }
                        />

                        <Input
                            type="password"
                            label="Password"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
                            icon={
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                                    <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                                </svg>
                            }
                        />

                        {mode === 'register' && (
                            <Input
                                type="password"
                                label="Confirm Password"
                                placeholder="••••••••"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                autoComplete="new-password"
                                icon={
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                                    </svg>
                                }
                            />
                        )}

                        <Button
                            type="submit"
                            fullWidth
                            glow
                            loading={loading || isLoading}
                            className="auth__submit"
                        >
                            {mode === 'login' ? 'Sign In' : 'Create Account'}
                        </Button>
                    </form>

                    {/* Toggle Mode */}
                    <div className="auth__toggle">
                        <span className="auth__toggle-text">
                            {mode === 'login' ? "Don't have an account?" : 'Already have an account?'}
                        </span>
                        <button
                            type="button"
                            className="auth__toggle-btn"
                            onClick={toggleMode}
                        >
                            {mode === 'login' ? 'Sign Up' : 'Sign In'}
                        </button>
                    </div>

                    {/* Back to home */}
                    <button
                        type="button"
                        className="auth__back"
                        onClick={() => navigate('/')}
                    >
                        ← Back to Home
                    </button>
                </GlassCard>
            </div>
        </div>
    );
};

export default AuthPage;

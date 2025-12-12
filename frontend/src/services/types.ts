// User types
export interface User {
    id: number;
    email: string;
    created_at?: string;
}

export interface AuthResponse {
    message: string;
    user?: User;
}

export interface LoginCredentials {
    email: string;
    password: string;
}

export interface RegisterCredentials {
    email: string;
    password: string;
}

// Analysis types
export interface AnalysisRequest {
    text: string;
}

export interface AnalysisScores {
    [category: string]: number;
}

export interface AnalysisMeta {
    hf_latency_ms: number;
    gemini_latency_ms: number;
    total_execution_ms: number;
}

export interface AnalysisResponse {
    category: string;
    hf_scores: AnalysisScores;
    summary: string;
    tone: 'positif' | 'negatif' | 'neutre';
    meta: AnalysisMeta;
}

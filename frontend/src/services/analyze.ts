import api from './api';
import type { AnalysisResponse } from './types';

export const analyzeService = {
    async analyzeText(text: string): Promise<AnalysisResponse> {
        const response = await api.post<AnalysisResponse>('/analyze/', { text });
        return response.data;
    },

    async healthCheck(): Promise<{ status: string }> {
        const response = await api.get<{ status: string }>('/analyze/health');
        return response.data;
    },
};

export default analyzeService;

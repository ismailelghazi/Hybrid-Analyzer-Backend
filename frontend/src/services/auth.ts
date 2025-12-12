import api from './api';
import type { User, AuthResponse, LoginCredentials, RegisterCredentials } from './types';

export const authService = {
    async register(credentials: RegisterCredentials): Promise<AuthResponse> {
        const response = await api.post<AuthResponse>('/auth/register', credentials);
        return response.data;
    },

    async login(credentials: LoginCredentials): Promise<AuthResponse> {
        const response = await api.post<AuthResponse>('/auth/login', credentials);
        return response.data;
    },

    async logout(): Promise<{ message: string }> {
        const response = await api.post<{ message: string }>('/auth/logout');
        return response.data;
    },

    async getCurrentUser(): Promise<User> {
        const response = await api.get<User>('/auth/me');
        return response.data;
    },
};

export default authService;

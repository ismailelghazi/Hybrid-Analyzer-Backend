import { ReactNode } from 'react';
import './GlassCard.css';

interface GlassCardProps {
    children: ReactNode;
    variant?: 'bark' | 'dusk' | 'emerald';
    floating?: boolean;
    className?: string;
    onClick?: () => void;
}

export const GlassCard = ({
    children,
    variant = 'bark',
    floating = false,
    className = '',
    onClick,
}: GlassCardProps) => {
    const variantClass = `glass-card--${variant}`;
    const floatingClass = floating ? 'glass-card--floating' : '';

    return (
        <div
            className={`glass-card ${variantClass} ${floatingClass} ${className}`}
            onClick={onClick}
        >
            {children}
        </div>
    );
};

export default GlassCard;

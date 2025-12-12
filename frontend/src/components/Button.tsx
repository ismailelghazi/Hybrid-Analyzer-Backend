import { ButtonHTMLAttributes, ReactNode } from 'react';
import './Button.css';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    children: ReactNode;
    variant?: 'primary' | 'secondary' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    glow?: boolean;
    loading?: boolean;
    fullWidth?: boolean;
}

export const Button = ({
    children,
    variant = 'primary',
    size = 'md',
    glow = false,
    loading = false,
    fullWidth = false,
    className = '',
    disabled,
    ...props
}: ButtonProps) => {
    const classes = [
        'button',
        `button--${variant}`,
        `button--${size}`,
        glow ? 'button--glow' : '',
        loading ? 'button--loading' : '',
        fullWidth ? 'button--full' : '',
        className,
    ].filter(Boolean).join(' ');

    return (
        <button
            className={classes}
            disabled={disabled || loading}
            {...props}
        >
            {loading ? (
                <span className="button__spinner" />
            ) : null}
            <span className={loading ? 'button__text--loading' : ''}>
                {children}
            </span>
        </button>
    );
};

export default Button;

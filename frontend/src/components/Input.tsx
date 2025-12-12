import { InputHTMLAttributes, forwardRef } from 'react';
import './Input.css';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
    icon?: React.ReactNode;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
    ({ label, error, icon, className = '', ...props }, ref) => {
        return (
            <div className={`input-group ${error ? 'input-group--error' : ''} ${className}`}>
                {label && <label className="input-label">{label}</label>}
                <div className="input-wrapper">
                    {icon && <span className="input-icon">{icon}</span>}
                    <input
                        ref={ref}
                        className={`input-field ${icon ? 'input-field--with-icon' : ''}`}
                        {...props}
                    />
                </div>
                {error && <span className="input-error">{error}</span>}
            </div>
        );
    }
);

Input.displayName = 'Input';

export default Input;

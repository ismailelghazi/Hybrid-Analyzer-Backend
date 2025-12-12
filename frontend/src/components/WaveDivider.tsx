import './WaveDivider.css';

interface WaveDividerProps {
    flip?: boolean;
    color?: 'emerald' | 'bark' | 'dusk';
}

export const WaveDivider = ({ flip = false, color = 'emerald' }: WaveDividerProps) => {
    const getColorStops = () => {
        switch (color) {
            case 'emerald':
                return ['#10B981', '#059669'];
            case 'bark':
                return ['#5A4636', '#3F2F23'];
            case 'dusk':
                return ['#334155', '#1E293B'];
            default:
                return ['#10B981', '#059669'];
        }
    };

    const [color1, color2] = getColorStops();

    return (
        <div className={`wave-divider ${flip ? 'wave-divider--flip' : ''}`}>
            <svg
                viewBox="0 0 1440 120"
                preserveAspectRatio="none"
                className="wave-divider__svg"
            >
                <defs>
                    <linearGradient id={`wave-gradient-${color}`} x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor={color1} stopOpacity="0.8" />
                        <stop offset="50%" stopColor={color2} stopOpacity="0.6" />
                        <stop offset="100%" stopColor={color1} stopOpacity="0.8" />
                    </linearGradient>
                </defs>
                <path
                    d="M0,60 C240,120 480,0 720,60 C960,120 1200,0 1440,60 L1440,120 L0,120 Z"
                    fill={`url(#wave-gradient-${color})`}
                    className="wave-divider__wave wave-divider__wave--1"
                />
                <path
                    d="M0,80 C240,20 480,100 720,40 C960,80 1200,20 1440,80 L1440,120 L0,120 Z"
                    fill={`url(#wave-gradient-${color})`}
                    opacity="0.5"
                    className="wave-divider__wave wave-divider__wave--2"
                />
                <path
                    d="M0,90 C240,50 480,110 720,70 C960,110 1200,50 1440,90 L1440,120 L0,120 Z"
                    fill={`url(#wave-gradient-${color})`}
                    opacity="0.3"
                    className="wave-divider__wave wave-divider__wave--3"
                />
            </svg>
        </div>
    );
};

export default WaveDivider;

import { useEffect, useRef } from 'react';
import './WaterBackground.css';

interface WaterBackgroundProps {
    variant?: 'landing' | 'auth' | 'dashboard';
    intensity?: 'low' | 'medium' | 'high';
}

export const WaterBackground = ({
    variant = 'landing',
    intensity = 'medium'
}: WaterBackgroundProps) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        let time = 0;

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };

        resize();
        window.addEventListener('resize', resize);

        const getGradientColors = () => {
            switch (variant) {
                case 'auth':
                    return ['#1E293B', '#3F2F23', '#5A4636'];
                case 'dashboard':
                    return ['#1E293B', '#334155', '#3F2F23'];
                default:
                    return ['#1E293B', '#334155', '#10B981'];
            }
        };

        const colors = getGradientColors();
        const waveCount = intensity === 'high' ? 5 : intensity === 'medium' ? 3 : 2;
        const speed = intensity === 'high' ? 0.002 : intensity === 'medium' ? 0.001 : 0.0005;

        const drawWave = (
            yOffset: number,
            amplitude: number,
            frequency: number,
            color: string,
            alpha: number,
            phaseOffset: number
        ) => {
            ctx.beginPath();
            ctx.moveTo(0, canvas.height);

            for (let x = 0; x <= canvas.width; x += 5) {
                const y = yOffset +
                    Math.sin((x * frequency) + time + phaseOffset) * amplitude +
                    Math.sin((x * frequency * 0.5) + time * 0.7 + phaseOffset) * (amplitude * 0.5);
                ctx.lineTo(x, y);
            }

            ctx.lineTo(canvas.width, canvas.height);
            ctx.closePath();

            ctx.fillStyle = color.replace(')', `, ${alpha})`).replace('rgb', 'rgba');
            ctx.fill();
        };

        const hexToRgb = (hex: string): string => {
            const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
            if (result) {
                return `rgb(${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)})`;
            }
            return 'rgb(0, 0, 0)';
        };

        const animate = () => {
            // Create gradient background
            const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
            gradient.addColorStop(0, colors[0]);
            gradient.addColorStop(0.5, colors[1]);
            gradient.addColorStop(1, colors[2]);

            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw multiple wave layers
            for (let i = 0; i < waveCount; i++) {
                const yOffset = canvas.height * (0.5 + i * 0.15);
                const amplitude = 30 + i * 15;
                const frequency = 0.003 - i * 0.0005;
                const alpha = 0.1 - i * 0.02;
                const phaseOffset = i * Math.PI * 0.5;

                const colorIndex = i % colors.length;
                drawWave(yOffset, amplitude, frequency, hexToRgb(colors[colorIndex]), alpha, phaseOffset);
            }

            time += speed;
            animationId = requestAnimationFrame(animate);
        };

        animate();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, [variant, intensity]);

    return (
        <div className="water-background">
            <canvas ref={canvasRef} className="water-canvas" />
            <div className="water-overlay" />
        </div>
    );
};

export default WaterBackground;

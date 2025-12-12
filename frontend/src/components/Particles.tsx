import { useEffect, useRef } from 'react';
import './Particles.css';

interface Particle {
    x: number;
    y: number;
    size: number;
    speedY: number;
    speedX: number;
    opacity: number;
    color: string;
}

interface ParticlesProps {
    count?: number;
    color?: 'emerald' | 'white' | 'mixed';
}

export const Particles = ({ count = 50, color = 'emerald' }: ParticlesProps) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        const particles: Particle[] = [];

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };

        resize();
        window.addEventListener('resize', resize);

        const getColor = (): string => {
            switch (color) {
                case 'emerald':
                    return `rgba(16, 185, 129, ${0.2 + Math.random() * 0.4})`;
                case 'white':
                    return `rgba(255, 255, 255, ${0.1 + Math.random() * 0.3})`;
                case 'mixed':
                    return Math.random() > 0.5
                        ? `rgba(16, 185, 129, ${0.2 + Math.random() * 0.4})`
                        : `rgba(255, 255, 255, ${0.1 + Math.random() * 0.3})`;
                default:
                    return `rgba(16, 185, 129, ${0.2 + Math.random() * 0.4})`;
            }
        };

        // Initialize particles
        for (let i = 0; i < count; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                size: Math.random() * 4 + 1,
                speedY: -0.2 - Math.random() * 0.5,
                speedX: (Math.random() - 0.5) * 0.3,
                opacity: 0.1 + Math.random() * 0.5,
                color: getColor(),
            });
        }

        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            particles.forEach((particle) => {
                // Update position
                particle.y += particle.speedY;
                particle.x += particle.speedX;

                // Reset particle if it goes off screen
                if (particle.y < -10) {
                    particle.y = canvas.height + 10;
                    particle.x = Math.random() * canvas.width;
                }
                if (particle.x < -10) particle.x = canvas.width + 10;
                if (particle.x > canvas.width + 10) particle.x = -10;

                // Draw particle with glow effect
                ctx.beginPath();
                ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                ctx.fillStyle = particle.color;
                ctx.fill();

                // Add subtle glow
                ctx.beginPath();
                ctx.arc(particle.x, particle.y, particle.size * 2, 0, Math.PI * 2);
                const gradient = ctx.createRadialGradient(
                    particle.x, particle.y, 0,
                    particle.x, particle.y, particle.size * 2
                );
                gradient.addColorStop(0, particle.color);
                gradient.addColorStop(1, 'transparent');
                ctx.fillStyle = gradient;
                ctx.fill();
            });

            animationId = requestAnimationFrame(animate);
        };

        animate();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, [count, color]);

    return <canvas ref={canvasRef} className="particles-canvas" />;
};

export default Particles;

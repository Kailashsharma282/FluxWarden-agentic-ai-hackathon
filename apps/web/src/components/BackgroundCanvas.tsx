import React, { useEffect, useRef } from 'react';

export const BackgroundCanvas: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    // Section 29: Respect prefers-reduced-motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', handleResize);

    // Section 29: 1. Particle field
    const particles: Array<{
      x: number;
      y: number;
      vx: number;
      vy: number;
      radius: number;
      alpha: number;
    }> = [];

    const PARTICLE_COUNT = Math.min(45, Math.floor((width * height) / 25000));
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: prefersReducedMotion ? 0 : (Math.random() - 0.5) * 0.35,
        vy: prefersReducedMotion ? 0 : (Math.random() - 0.5) * 0.35,
        radius: Math.random() * 1.5 + 0.8,
        alpha: Math.random() * 0.4 + 0.2
      });
    }

    // Section 29: 2. Data streams (small animated lines/dots)
    const dataStreams: Array<{
      x: number;
      y: number;
      length: number;
      speed: number;
      alpha: number;
    }> = [];

    for (let i = 0; i < 8; i++) {
      dataStreams.push({
        x: Math.random() * width,
        y: Math.random() * height,
        length: Math.random() * 30 + 20,
        speed: prefersReducedMotion ? 0 : Math.random() * 1.5 + 0.8,
        alpha: Math.random() * 0.25 + 0.1
      });
    }

    let gradientOffset = 0;

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // Section 29: 3. Ambient gradient (Slowly moving radial gradients)
      if (!prefersReducedMotion) {
        gradientOffset += 0.002;
      }
      const gradX = width / 2 + Math.sin(gradientOffset) * 80;
      const gradY = height / 3 + Math.cos(gradientOffset) * 50;

      const gradient = ctx.createRadialGradient(
        gradX, gradY, 40,
        width / 2, height / 2, Math.max(width, height) * 0.75
      );
      gradient.addColorStop(0, 'rgba(15, 23, 42, 0.45)');
      gradient.addColorStop(0.5, 'rgba(10, 13, 20, 0.9)');
      gradient.addColorStop(1, '#070a10');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, width, height);

      // Section 29: 4. Infrastructure grid (Subtle perspective grid)
      ctx.strokeStyle = 'rgba(0, 240, 255, 0.025)';
      ctx.lineWidth = 1;
      const gridSize = 64;
      for (let x = 0; x < width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      for (let y = 0; y < height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      // Section 29: 5. Network connections (Faint lines connecting nodes)
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 130) {
            ctx.beginPath();
            ctx.strokeStyle = `rgba(0, 240, 255, ${0.07 * (1 - dist / 130)})`;
            ctx.lineWidth = 0.7;
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }

      // Draw particles
      for (const p of particles) {
        if (!prefersReducedMotion) {
          p.x += p.vx;
          p.y += p.vy;
          if (p.x < 0) p.x = width;
          if (p.x > width) p.x = 0;
          if (p.y < 0) p.y = height;
          if (p.y > height) p.y = 0;
        }

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 240, 255, ${p.alpha})`;
        ctx.shadowColor = '#00f0ff';
        ctx.shadowBlur = 4;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      // Section 29: 6. Data streams (Small animated vertical/diagonal packets)
      for (const ds of dataStreams) {
        if (!prefersReducedMotion) {
          ds.y += ds.speed;
          if (ds.y > height) {
            ds.y = -ds.length;
            ds.x = Math.random() * width;
          }
        }
        ctx.beginPath();
        ctx.strokeStyle = `rgba(139, 92, 246, ${ds.alpha})`;
        ctx.lineWidth = 1.2;
        ctx.moveTo(ds.x, ds.y);
        ctx.lineTo(ds.x, ds.y + ds.length);
        ctx.stroke();
      }

      if (!prefersReducedMotion) {
        animationFrameId = requestAnimationFrame(render);
      }
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationFrameId) cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      <canvas ref={canvasRef} className="w-full h-full opacity-65" />
      {/* Section 29: 7. Scanlines (Extremely subtle) */}
      <div className="scanline" />
    </div>
  );
};

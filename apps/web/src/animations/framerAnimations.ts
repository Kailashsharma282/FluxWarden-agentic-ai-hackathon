import { Variants } from 'framer-motion';

// Section 48: Page transitions (Fade/slide)
export const pageTransitionVariants: Variants = {
  initial: { opacity: 0, y: 12 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.35, ease: [0.16, 1, 0.3, 1] }
  },
  exit: {
    opacity: 0,
    y: -8,
    transition: { duration: 0.2, ease: 'easeOut' }
  }
};

// Section 48: Cards (Staggered entrances)
export const staggerContainerVariants: Variants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.05
    }
  }
};

export const cardEntranceVariants: Variants = {
  hidden: { opacity: 0, y: 15, scale: 0.98 },
  show: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.4, ease: [0.16, 1, 0.3, 1] }
  }
};

// Section 48: Agent status (Subtle pulsing)
export const agentStatusPulseVariants: Variants = {
  idle: { scale: 1, opacity: 0.9 },
  active: {
    scale: [1, 1.02, 1],
    opacity: [0.95, 1, 0.95],
    transition: {
      duration: 2.2,
      repeat: Infinity,
      ease: 'easeInOut'
    }
  }
};

// Section 48: Failure (Brief red pulse)
export const failureRedPulseVariants: Variants = {
  initial: { scale: 1, borderColor: 'rgba(244, 63, 94, 0.3)' },
  pulse: {
    scale: [1, 1.03, 1],
    borderColor: ['rgba(244, 63, 94, 0.4)', 'rgba(244, 63, 94, 0.9)', 'rgba(244, 63, 94, 0.4)'],
    boxShadow: [
      '0 0 0 rgba(244, 63, 94, 0)',
      '0 0 25px rgba(244, 63, 94, 0.6)',
      '0 0 10px rgba(244, 63, 94, 0.2)'
    ],
    transition: { duration: 0.8, ease: 'easeOut' }
  }
};

// Section 48: Replanning (Distinct transition animation)
export const replanningTransitionVariants: Variants = {
  initial: { opacity: 0.8, rotate: 0 },
  replan: {
    opacity: 1,
    rotate: [0, -2, 2, 0],
    transition: { duration: 0.6, ease: 'easeInOut' }
  }
};

// Section 48: Verification (Sequential checks)
export const verificationCheckItemVariants: Variants = {
  hidden: { opacity: 0, x: -10 },
  visible: (customIndex: number) => ({
    opacity: 1,
    x: 0,
    transition: { delay: customIndex * 0.12, duration: 0.3, ease: 'easeOut' }
  })
};

// Section 48: Resolution (Subtle expanding glow)
export const resolutionExpandingGlowVariants: Variants = {
  initial: { opacity: 0, scale: 0.96 },
  resolved: {
    opacity: 1,
    scale: 1,
    boxShadow: [
      '0 0 10px rgba(16, 185, 129, 0.2)',
      '0 0 35px rgba(16, 185, 129, 0.4)',
      '0 0 20px rgba(16, 185, 129, 0.25)'
    ],
    transition: { duration: 0.9, ease: [0.16, 1, 0.3, 1] }
  }
};

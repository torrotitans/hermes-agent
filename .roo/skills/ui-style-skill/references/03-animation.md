# Framer Motion Micro-Interactions

## Purpose

This reference document details the implementation of premium micro-interactions using Framer Motion for polished, award-winning UI experiences.

## Core Principles

### Animation Philosophy

1. **Purpose-Driven**: Every animation must serve a functional purpose
2. **Subtle & Refined**: Less is more; avoid excessive motion
3. **Performance-First**: Use GPU-accelerated properties
4. **Accessible**: Respect `prefers-reduced-motion`

### Timing Standards

| Animation Type | Duration | Easing |
|----------------|----------|--------|
| Button hover | 150ms | ease-out |
| Button press | 100ms | ease-in |
| Modal fade | 200ms | ease-out |
| Page transition | 300ms | ease-in-out |
| Complex sequence | 400ms+ | custom spring |

## Framer Motion Fundamentals

### Installation

```bash
npm install framer-motion
```

### Basic Animation

```tsx
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.3 }}
>
  Content
</motion.div>
```

## Micro-Interaction Patterns

### 1. Button Press (Scale)

```tsx
import { motion } from 'framer-motion';

export function PrimaryButton({ children, onClick }) {
  return (
    <motion.button
      className="bg-torro-primary rounded-[14px] h-[40px] px-6"
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      transition={{ duration: 0.1 }}
      onClick={onClick}
    >
      {children}
    </motion.button>
  );
}
```

### 2. Modal Slide & Fade

```tsx
import { motion, AnimatePresence } from 'framer-motion';

export function Modal({ isOpen, onClose, children }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50"
            onClick={onClose}
          />
          <motion.div
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 100, opacity: 0 }}
            transition={{ type: 'spring', damping: 25 }}
            className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

### 3. Tooltip Fade

```tsx
import { motion } from 'framer-motion';

export function Tooltip({ content, children }) {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
    >
      {children}
      <AnimatePresence>
        {isVisible && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            transition={{ duration: 0.15 }}
            className="absolute -top-8 left-1/2 -translate-x-1/2 bg-black text-white px-2 py-1 rounded"
          >
            {content}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
```

### 4. List Stagger

```tsx
import { motion } from 'framer-motion';

export function StaggeredList({ items }) {
  return (
    <motion.ul
      initial="hidden"
      animate="visible"
      variants={{
        hidden: { opacity: 0 },
        visible: {
          opacity: 1,
          transition: {
            staggerChildren: 0.1
          }
        }
      }}
    >
      {items.map((item, index) => (
        <motion.li
          key={index}
          variants={{
            hidden: { opacity: 0, y: 20 },
            visible: { opacity: 1, y: 0 }
          }}
        >
          {item}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

## Apple Liquid Glass Animation

### Glass Panel Hover

```tsx
import { motion } from 'framer-motion';

export function GlassPanel({ children }) {
  return (
    <motion.div
      className="backdrop-blur-xl bg-white/70 border border-black/5 rounded-[20px] shadow-panel"
      whileHover={{
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
        scale: 1.01
      }}
      transition={{ duration: 0.2 }}
    >
      {children}
    </motion.div>
  );
}
```

### Shimmer Effect

```tsx
import { motion } from 'framer-motion';

export function ShimmerCard() {
  return (
    <div className="relative overflow-hidden rounded-[20px]">
      <motion.div
        className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
        animate={{ x: '-100%' }}
        transition={{
          repeat: Infinity,
          duration: 1.5,
          ease: 'linear'
        }}
      />
      <div className="p-6">
        <h3 className="text-lg font-brand">Card Title</h3>
        <p className="text-muted mt-2">Card content</p>
      </div>
    </div>
  );
}
```

## Performance Optimization

### GPU Acceleration

Use these properties for smooth animations:

```tsx
// ✅ GOOD: GPU-accelerated
<motion.div
  animate={{
    x: 100,
    y: 100,
    scale: 1.1,
    rotate: 45
  }}
/>

// ❌ BAD: Triggers layout recalculation
<motion.div
  animate={{
    width: 200,
    height: 100,
    margin: 20
  }}
/>
```

### will-change CSS

```css
.animated-element {
  will-change: transform, opacity;
}
```

### Skip Animations for SSR

```tsx
import { MotionConfig } from 'framer-motion';

<MotionConfig skipAnimations={true}>
  <App />
</MotionConfig>
```

## Accessibility

### Respecting User Preferences

```tsx
import { useReducedMotion } from 'framer-motion';

export function AnimatedComponent() {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      animate={{ x: 100 }}
      transition={{
        duration: shouldReduceMotion ? 0 : 0.3
      }}
    />
  );
}
```

### Focus Management

```tsx
import { motion } from 'framer-motion';

<motion.button
  whileFocus={{ scale: 1.05 }}
  className="focus:outline-none focus:ring-2 focus:ring-torro-primary"
>
  Click me
</motion.button>
```

## Related Files

- [`04-accessibility.md`](04-accessibility.md) - WCAG compliance and auditing

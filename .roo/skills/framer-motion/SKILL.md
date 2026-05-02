---
name: framer-motion
description: Implement framer-motion for React animations including transitions, gestures, layout animations, AnimatePresence, and motion components with TypeScript support
license: MIT
compatibility:
  - react-18.0+
  - framer-motion-10.0+
metadata:
  version: 1.0.0
  author: Torro Team
  source: https://www.npmjs.com/package/framer-motion
---

# Framer Motion Skill

## When to Use This Skill

Use this skill when you need to:
- Create smooth animations with motion components
- Implement page transitions with AnimatePresence
- Handle layout animations with layout props
- Add gesture support (drag, tap, hover)
- Create staggered animations for lists
- Animate values with useMotionValue and useTransform
- Implement scroll-based animations
- Create spring and tween animations
- Use variants for declarative animations
- Animate CSS properties and transforms

## When NOT to Use This Skill

Do NOT use this skill when:
- Building simple CSS-only animations (use CSS transitions)
- Creating complex 3D animations (use Three.js)
- Building video editing tools (use dedicated video libraries)
- Performing heavy canvas animations (use Canvas/SVG directly)

## Inputs Required

Before starting, ensure you have:
1. React version (default: 18.x+)
2. Animation type (transition, gesture, layout, page)
3. Performance requirements (GPU acceleration)
4. Target browsers (iOS Safari support)

## Workflow

### Step 1: Basic Motion Components

```typescript
import { motion } from 'framer-motion'

function BasicAnimations() {
  return (
    <div>
      {/* Animate on mount */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Fade in and slide up
      </motion.div>

      {/* Hover animation */}
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        Interactive Button
      </motion.button>

      {/* Continuous animation */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
      >
        Spinning Icon
      </motion.div>
    </div>
  )
}
```

### Step 2: Variants for Declarative Animations

```typescript
import { motion } from 'framer-motion'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5 },
  },
}

function StaggeredAnimation() {
  return (
    <motion.ul variants={containerVariants} initial="hidden" animate="visible">
      {['Item 1', 'Item 2', 'Item 3'].map((item, i) => (
        <motion.li key={i} variants={itemVariants}>
          {item}
        </motion.li>
      ))}
    </motion.ul>
  )
}
```

### Step 3: AnimatePresence for Mount/Unmount Animations

```typescript
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function ModalWithAnimation() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open Modal</button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)' }}
            onClick={() => setIsOpen(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              transition={{ type: 'spring', damping: 25 }}
              onClick={(e) => e.stopPropagation()}
              style={{
                background: '#fff',
                padding: '20px',
                borderRadius: '8px',
                maxWidth: '400px',
                margin: '100px auto',
              }}
            >
              <h2>Modal Content</h2>
              <p>This modal animates in and out.</p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
```

### Step 4: Drag and Drop

```typescript
import { motion } from 'framer-motion'

function DraggableCard() {
  return (
    <motion.div
      drag
      dragConstraints={{ left: -200, right: 200, top: -100, bottom: 100 }}
      dragElastic={0.2}
      whileDrag={{ scale: 1.1, cursor: 'grabbing' }}
      onDragEnd={(event, info) => {
        console.log('Dropped at:', info.offset)
      }}
      style={{
        width: 100,
        height: 100,
        background: '#4A90D9',
        borderRadius: '8px',
        cursor: 'grab',
      }}
    >
      Drag me
    </motion.div>
  )
}

// Snap to grid
function SnapToGrid() {
  return (
    <motion.div
      drag
      dragSnapToOrigin
      style={{ width: 50, height: 50, background: '#e74c3c', borderRadius: '50%' }}
    />
  )
}
```

### Step 5: Layout Animations

```typescript
import { motion } from 'framer-motion'
import { useState } from 'react'

function LayoutAnimation() {
  const [items, setItems] = useState([
    { id: 1, text: 'Item 1' },
    { id: 2, text: 'Item 2' },
    { id: 3, text: 'Item 3' },
  ])

  const toggleItem = (id: number) => {
    setItems((prev) =>
      prev.map((item) =>
        item.id === id ? { ...item, hidden: !item.hidden } : item
      )
    )
  }

  return (
    <div>
      <AnimatePresence>
        {items.map((item) => (
          !item.hidden && (
            <motion.div
              key={item.id}
              layout
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              onClick={() => toggleItem(item.id)}
              style={{
                padding: '10px',
                margin: '5px 0',
                background: '#3498db',
                color: '#fff',
                borderRadius: '4px',
              }}
            >
              {item.text}
            </motion.div>
          )
        ))}
      </AnimatePresence>
    </div>
  )
}
```

### Step 6: Scroll-Based Animations

```typescript
import { motion, useScroll, useTransform } from 'framer-motion'

function ScrollAnimations() {
  const { scrollYProgress } = useScroll()
  const scaleX = useTransform(scrollYProgress, [0, 1], [0, 1])

  return (
    <>
      {/* Progress bar */}
      <motion.div
        style={{ scaleX }}
        className="fixed top-0 left-0 right-0 h-1 bg-blue-500 origin-left"
      />

      {/* Parallax effect */}
      <ParallaxSection />
    </>
  )
}

function ParallaxSection() {
  const ref = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({ target: ref })
  const y = useTransform(scrollYProgress, [0, 1], [0, -100])

  return (
    <motion.div ref={ref} style={{ y }} className="h-screen flex items-center justify-center">
      <h1>Parallax Text</h1>
    </motion.div>
  )
}
```

### Step 7: Use Motion Values

```typescript
import { motion, useMotionValue, useTransform, useSpring } from 'framer-motion'

function InteractiveAnimation() {
  const mouseX = useMotionValue(0)
  const mouseY = useMotionValue(0)

  const springX = useSpring(mouseX, { stiffness: 300, damping: 30 })
  const springY = useSpring(mouseY, { stiffness: 300, damping: 30 })

  const rotateX = useTransform(springY, [-200, 200], [15, -15])
  const rotateY = useTransform(springX, [-200, 200], [-15, 15])

  return (
    <motion.div
      onMouseMove={(e) => {
        mouseX.set(e.clientX - window.innerWidth / 2)
        mouseY.set(e.clientY - window.innerHeight / 2)
      }}
      style={{ rotateX, rotateY, transformStyle: 'preserve-3d' }}
      className="w-64 h-64 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl"
    />
  )
}
```

### Step 8: Page Transitions

```typescript
import { motion, AnimatePresence } from 'framer-motion'
import { useRouter } from 'next/router'

const pageVariants = {
  initial: {
    opacity: 0,
    y: 20,
  },
  animate: {
    opacity: 1,
    y: 0,
  },
  exit: {
    opacity: 0,
    y: -20,
  },
}

function PageTransition({ children }: { children: React.ReactNode }) {
  const { pathname } = useRouter()

  return (
    <motion.div
      key={pathname}
      initial="initial"
      animate="animate"
      exit="exit"
      variants={pageVariants}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
    >
      {children}
    </motion.div>
  )
}

// Usage in Next.js
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <PageTransition>
      {children}
    </PageTransition>
  )
}
```

### Step 9: Gesture Animations

```typescript
import { motion } from 'framer-motion'

function GestureCard() {
  return (
    <motion.div
      whileHover={{ scale: 1.05, boxShadow: '0 10px 30px rgba(0,0,0,0.2)' }}
      whileTap={{ scale: 0.95 }}
      drag="x"
      dragConstraints={{ left: -100, right: 100 }}
      dragElastic={0.5}
      onDrag={(event, info) => {
        console.log('Drag distance:', info.offset.x)
      }}
      onDragEnd={(event, info) => {
        if (Math.abs(info.offset.x) > 50) {
          console.log('Swipe detected!')
        }
      }}
      className="w-48 h-32 bg-white rounded-lg shadow-lg cursor-grab active:cursor-grabbing"
    >
      <div className="p-4">
        <h3 className="font-bold">Swipe Me</h3>
        <p className="text-sm text-gray-600">Drag horizontally</p>
      </div>
    </motion.div>
  )
}
```

### Step 10: Animation Configurations

```typescript
import { motion } from 'framer-motion'

// Spring animation (natural, bouncy)
const springConfig = {
  type: 'spring',
  stiffness: 300,
  damping: 30,
}

// Tween animation (smooth, predictable)
const tweenConfig = {
  type: 'tween',
  duration: 0.5,
  ease: 'easeInOut',
}

// Keyframes animation (multiple states)
const keyframesConfig = {
  initial: { scale: 0, rotate: -180 },
  animate: {
    scale: [0, 1.2, 1],
    rotate: [-180, 180, 0],
    transition: {
      duration: 1,
      ease: 'easeInOut',
    },
  },
}

function AnimationConfigs() {
  return (
    <>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={springConfig}
      />

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={tweenConfig}
      />

      <motion.div
        variants={keyframesConfig}
        initial="initial"
        animate="animate"
      />
    </>
  )
}
```

## Files Reference

| File | Purpose |
|------|---------|
| `src/index.ts` | Main exports |
| `src/motion/` | Motion components |
| `src/gestures/` | Gesture handling |
| `src/layout/` | Layout animations |

## Troubleshooting

### Issue: Animations Not Running

**Symptom**: Components don't animate

**Solution**:
- Ensure `motion` component is used (not regular HTML)
- Check `initial` and `animate` props are different
- Verify no CSS `display: none` blocking animations

### Issue: Performance Issues

**Symptom**: Janky animations on low-end devices

**Solution**:
- Use `will-change: transform` sparingly
- Prefer `scale` and `opacity` (GPU accelerated)
- Avoid animating `width`, `height`, `top`, `left`
- Use `transform` instead of layout properties

### Issue: AnimatePresence Not Working

**Symptom**: Exit animations not playing

**Solution**:
- Ensure component has unique `key` prop
- Check conditional rendering (`{isOpen && <motion.div>}`)
- Verify `AnimatePresence` wraps the conditional component

## Examples

### Example 1: Loading Skeleton

```typescript
function LoadingSkeleton() {
  return (
    <motion.div
      initial={{ opacity: 0.4 }}
      animate={{ opacity: [0.4, 0.7, 0.4] }}
      transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
      className="h-4 bg-gray-200 rounded w-3/4"
    />
  )
}
```

### Example 2: Accordion

```typescript
function Accordion({ items }: { items: { title: string; content: string }[] }) {
  return (
    <div>
      {items.map((item, i) => (
        <AccordionItem key={i} {...item} />
      ))}
    </div>
  )
}

function AccordionItem({ title, content }: { title: string; content: string }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>{title}</button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            <p>{content}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
```

## Related Resources

- [Framer Motion Documentation](https://www.framer.com/motion/)
- [Framer Motion Examples](https://www.framer.com/motion/examples/)
- [Motion Values Guide](https://www.framer.com/motion/animation/)

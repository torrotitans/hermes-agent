# 12. Notification Popover

## Component Location
`UI/src/features/session/ui/notification-popover.tsx`

## Structure

```
NotificationPopover
├── Trigger Button (Header)
│   ├── Icon (notifications)
│   ├── Badge (unread count)
│   └── Expandable Text (Notifications + Unread count)
├── Popover Panel
│   ├── Header
│   │   ├── Title ("Notifications")
│   │   └── Total Count (plain text, no badge)
│   ├── Filter Tabs (All / Unread)
│   │   └── Segmented Control
│   ├── Notification List (scrollable)
│   │   └── Notification Item
│   │       ├── Unread Dot
│   │       ├── Title
│   │       ├── Severity Badge
│   │       └── Message
│   └── Footer
│       └── "Mark all as read" Button
```

## Layout Rules

### Popover Container
- `w-80` fixed width
- `rounded-[20px]` border radius
- `border border-white/10` subtle border
- `bg-white/80` semi-transparent background
- `shadow-float` floating shadow
- `backdrop-blur-2xl` liquid glass blur
- `ring-1 ring-black/5` outer ring
- `z-50` above all content
- `animate-in fade-in slide-in-from-top-2` entrance animation

### Header Section
- `border-b border-white/10` divider
- `bg-white/20` slightly darker background
- `px-4 py-3` padding
- Total count: **plain text only** — `text-[10px] font-black uppercase tracking-widest text-torro-primary`
- **NO** bounding box, background, or padding for the total count

### Filter Tabs
- Segmented control style
- `bg-black/5 rounded-xl border border-black/5`
- Active state: `bg-white text-torro-primary shadow-sm`
- Inactive state: `text-torro-muted hover:text-torro-text`

### Notification List
- `flex flex-col max-h-[300px]` — flex column with max height
- Scrollable area: `flex-1 overflow-y-auto`
- **NOT** `overflow-y-auto` on the parent container

### Notification Item
- `rounded-xl p-3` padding
- `border border-white/10` subtle border
- Unread: `bg-white/80 shadow-float`
- Read: `bg-white/20 opacity-60`
- Severity badges:
  - High: `bg-[#EF4444]/10 text-[#EF4444]`
  - Medium: `bg-[#F59E0B]/10 text-[#F59E0B]`
  - Info: `bg-[#3B82F6]/10 text-[#3B82F6]`
  - Low: `bg-[#10B981]/10 text-[#10B981]`

### Footer ("Mark all as read")
- **Fixed at bottom**, outside scrollable area
- `relative px-3 py-2 border-t border-white/10`
- `bg-white/[0.03]` — 3% white background (nearly transparent)
- `backdrop-blur-2xl` — liquid glass blur effect
- Gradient overlay: `absolute inset-x-0 top-0 h-16 bg-gradient-to-b from-white/[0.06] via-white/[0.03] to-transparent pointer-events-none`
- Button: `text-xs font-semibold text-torro-primary/70 hover:text-torro-primary`
- Disabled: `opacity-30 cursor-not-allowed`

## Trigger Button
- `group relative flex items-center gap-2`
- Icon: `h-6 w-6`
- Badge: `absolute top-0 right-0 h-3 w-3` — positioned on icon
- Expandable text: `transition-all duration-200 ease-out`
  - Collapsed: `max-w-0 opacity-0`
  - Expanded (hover/focus): `max-w-[140px] opacity-100`

## Data Flow
- Notifications fetched via `useQuery` from `/api/monitoring/notifications`
- Demo data merged with real data: `[...DEMO_NOTIFICATIONS, ...(response.data || [])]`
- Mark individual read: `apiPost('/api/monitoring/notifications', { id, read: true })`
- Mark all read: loops through unread IDs and calls API for each
- Refetch interval: 30 seconds

## Empty States
- No unread: "No unread messages" + "You've read all your notifications."
- All caught up: "All caught up!" + "We'll notify you when something happens."
- Icon: `notifications` at 20% opacity in a `h-10 w-10 rounded-full bg-black/5` container

## Do Not
- ❌ Use `absolute` positioning for "Mark all as read" inside scrollable container
- ❌ Add bounding box/background to the total count
- ❌ Use solid white background for the footer area
- ❌ Use `overflow-y-auto` on the parent container (use flex-1 on child instead)
- ❌ Use gradient overlay with opacity > 0.06

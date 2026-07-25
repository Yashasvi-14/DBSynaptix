# DBSynaptix Frontend Design System

> Internal UI/UX specification for the planned DBSynaptix product interface.

The frontend described here represents the current design direction and is not part of the implemented backend.

---

## Product Identity

**Product:** DBSynaptix  
**Tagline:** Giving Data a Brain.  
**Philosophy:** Understand. Retrieve. Reason. Query.

The interface should communicate that DBSynaptix is an intelligent database workspace rather than a conventional administration dashboard.

---

## Design Principles

The product should emphasise:

- Clarity
- Simplicity
- Technical depth
- Fast interaction
- Visibility into AI behaviour
- Professional developer-tool aesthetics

Visual inspiration includes modern developer and AI products such as Cursor, Vercel, Linear, ChatGPT, and Supabase.

---

## Theme

Dark mode will be the initial design target.

Light mode may be introduced later.

---

## Colour Palette

### Background

`#09090B`

Primary application background.

### Surface

`#18181B`

Cards, panels, editors, and containers.

### Border

`#27272A`

Borders, separators, and input outlines.

### Primary

`#7C3AED`

Primary actions, active states, and brand accents.

### Secondary

`#3B82F6`

Links and secondary AI-related accents.

### Success

`#10B981`

Successful execution and completed states.

### Warning

`#F59E0B`

Warnings and potentially risky actions.

### Error

`#EF4444`

Errors and validation failures.

### Text

Primary: `#FAFAFA`

Secondary: `#A1A1AA`

Muted: `#71717A`

---

## Typography

**Headings:** Geist  
**Body:** Inter  
**SQL / Code:** JetBrains Mono

---

## Icons

Lucide Icons.

---

## Shape

Suggested border radii:

- Buttons: 12px
- Cards: 16px
- Dialogs: 20px

Use subtle elevation and avoid unnecessarily heavy shadows.

---

## Spacing

Base spacing scale:

```text
4
8
12
16
24
32
40
48
64
96
```

Prefer consistent spacing based around an 8-point grid.

---

## Motion

Animations should be:

- Smooth
- Fast
- Purposeful
- Subtle

Suggested durations:

```text
Fast:    150ms
Normal:  250ms
Slow:    400ms
```

Prefer fade, slide, and scale transitions.

Avoid decorative motion that distracts from the query workflow.

---

## Application Layout

Initial desktop direction:

```text
+-----------------------------------------------------------+
|                       Top Navigation                      |
+-------------+---------------------------------------------+
|             |                                             |
|   Sidebar   |              Workspace                      |
|             |                                             |
|             |                                             |
+-------------+---------------------------------------------+
```

Suggested dimensions:

- Sidebar: 280px
- Top navigation: 72px
- Content padding: 32px
- Maximum content width: 1600px

These values are design starting points rather than fixed implementation requirements.

---

## Core Components

### Navigation

- Sidebar
- Top navigation
- Breadcrumbs
- Theme control

### Database

- Database connection form
- Connection state
- Schema/database information

### Query Workspace

- Natural-language question input
- Query submission state
- Generated SQL viewer/editor
- Results table

### AI Pipeline

Planned visibility into:

- Retrieval
- Context construction
- SQL generation
- Validation
- Execution

The interface should expose useful pipeline state without overwhelming the user with implementation details.

### Feedback

- Loading states
- Progress indicators
- Toasts
- Error states
- Empty states
- Validation feedback

---

## Planned Pages

### Landing Page

Potential sections:

- Hero
- Product capabilities
- Architecture
- Technology
- Development status
- GitHub

### Query Workspace

Primary application experience:

```text
Database
   |
   v
Question
   |
   v
Pipeline State
   |
   v
Generated SQL
   |
   v
Results
```

### History

Planned after query-history support is implemented in the backend.

### Evaluation

Planned as the benchmark infrastructure matures.

### Settings

Database and application configuration.

---

## SQL Experience

Generated SQL should be treated as a first-class output.

The workspace should make it easy to:

- Inspect generated SQL
- Understand whether validation succeeded
- View execution results
- Identify execution errors

A richer SQL explanation interface can be introduced after explanation support exists in the backend.

---

## Responsive Design

Desktop is the initial priority because database exploration and SQL inspection benefit from larger screens.

The interface should eventually support:

- Desktop
- Laptop
- Tablet
- Mobile

Mobile layouts may simplify advanced workspace functionality rather than reproduce the desktop interface exactly.

---

## Accessibility

Frontend implementation should account for:

- Keyboard navigation
- Visible focus states
- Semantic HTML
- Sufficient contrast
- Appropriate ARIA attributes
- Accessible form validation

---

## Performance Direction

The frontend should minimise unnecessary rendering and keep interactions responsive.

Performance targets should be established through measurement once the frontend exists rather than treated as guarantees during the design phase.

---

## Future Interface Capabilities

Potential future additions include:

- Streaming generation state
- SQL explanations
- Query history
- Suggested questions
- Benchmark visualisation
- Retrieval diagnostics
- Charts and data visualisations
- Light mode

These features depend on corresponding backend capabilities and are not part of the current implementation.

---

## Product Feel

DBSynaptix should feel closer to an intelligent developer tool than a traditional admin dashboard.

The interface should reinforce the core workflow:

**Understand → Retrieve → Reason → Query**
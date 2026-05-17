# DESIGN.md — Material 3 Design Specification (Vue 3)

> **Audience:** AI coding agents and developers building this Vue 3 web project.
> **Purpose:** A prescriptive, machine-actionable specification. Every UI the agent
> produces MUST conform to the rules below. When a design choice is not specified
> here, follow Material Design 3 defaults and platform web standards — do not
> invent new patterns.
>
> **Stack assumptions:** Vue 3 + `<script setup lang="ts">` (Composition API),
> Vite, Vue Router, CSS custom properties for design tokens. M3 components come
> from `@material/web` (custom elements) where available, otherwise are built
> from semantic HTML + tokens following M3 specs.

---

## How to Use This Document (Agent Instructions)

1. **Read [Hard Rules](#1-hard-rules) first.** These are non-negotiable and apply to every task.
2. Before writing UI code, locate the relevant section and apply its rules verbatim.
3. Prefer **copy-pasting the code templates** in [§14](#14-theme--token-implementation) over writing equivalents from scratch.
4. When a value is needed (color, spacing, radius, duration), use the **CSS custom property token**, never a literal.
5. Reach for **semantic HTML first**; add ARIA only when native semantics are insufficient.
6. Before marking any UI task complete, run the [Definition of Done](#16-definition-of-done) checklist.
7. If a requirement here conflicts with a user instruction, surface the conflict instead of silently violating the spec.

### Normative Language

| Term | Meaning |
|------|---------|
| **MUST** / **MUST NOT** | Hard requirement. Violations are bugs and must be fixed. |
| **SHOULD** / **SHOULD NOT** | Strong default. Deviate only with an explicit, stated reason. |
| **MAY** | Optional, at the agent's discretion. |

---

## Table of Contents

1. [Hard Rules](#1-hard-rules)
2. [Design Principles](#2-design-principles)
3. [Design Tokens](#3-design-tokens)
4. [Color System](#4-color-system)
5. [Typography](#5-typography)
6. [Shape](#6-shape)
7. [Elevation & Layering](#7-elevation--layering)
8. [Spacing & Layout Grid](#8-spacing--layout-grid)
9. [Iconography & Imagery](#9-iconography--imagery)
10. [Components](#10-components)
11. [Motion](#11-motion)
12. [Responsive & Adaptive Design](#12-responsive--adaptive-design)
13. [Accessibility](#13-accessibility)
14. [Theme & Token Implementation](#14-theme--token-implementation)
15. [Code Organization & Naming](#15-code-organization--naming)
16. [Definition of Done](#16-definition-of-done)
17. [References](#17-references)

---

## 1. Hard Rules

These apply to **every** UI change. They are the most common sources of spec violations.

- **R1.** MUST NOT hardcode color values (`#hex`, `rgb()`, named colors) in components. Use `var(--md-sys-color-*)`.
- **R2.** MUST NOT hardcode `font-size`/`line-height`/`font-weight`. Use the typescale tokens; size text in `rem`, never `px`.
- **R3.** MUST NOT hardcode spacing, radius, elevation, or motion durations. Use the tokens in [§3](#3-design-tokens).
- **R4.** Every screen MUST work in **both light and dark themes** (`prefers-color-scheme` + explicit override). No light-only screens.
- **R5.** Every screen MUST be usable across **Compact, Medium, and Expanded** window size classes ([§12](#12-responsive--adaptive-design)).
- **R6.** Interactive elements MUST be native interactive HTML (`<button>`, `<a>`, `<input>`, …). MUST NOT attach `@click` to a `<div>`/`<span>` to fake a control.
- **R7.** Every interactive element MUST have a pointer target ≥ **48×48 CSS px** and an accessible name.
- **R8.** Information MUST NOT be conveyed by color alone. Pair color with text, icon, or shape.
- **R9.** MUST NOT disable zoom or text scaling. The viewport meta MUST NOT contain `user-scalable=no` or `maximum-scale=1`. UI MUST survive 200% zoom and large browser font sizes.
- **R10.** Layout MUST use CSS logical properties (`margin-inline`, `padding-block`, `inset-inline`, `text-align: start`), never physical `left`/`right`, to keep RTL viable.
- **R11.** MUST NOT use fixed `px` widths/heights for content containers where fluid sizing (`%`, `fr`, `clamp()`, `min()`, `max()`, intrinsic sizing) is appropriate.
- **R12.** Reusable UI MUST be a shared component. MUST NOT copy-paste markup/styles across views.
- **R13.** Component styles MUST be `<style scoped>`. The **only** global CSS is the token layer ([§3](#3-design-tokens)) and a minimal reset.
- **R14.** Every page MUST have exactly one `<h1>`, a correct heading order (no skipped levels), and landmark elements (`<header>`, `<nav>`, `<main>`, `<footer>`).

---

## 2. Design Principles

| Principle | Operational meaning for the agent |
|-----------|-----------------------------------|
| **Consistency** | Reuse existing components and tokens before creating new ones. Identical semantics → identical implementation. |
| **Clear hierarchy** | Use color roles, elevation, and the type scale to establish hierarchy. Limit competing emphasis. |
| **Adaptive by default** | Build for all window size classes from the start, not phone-first with retrofits. |
| **Accessibility built-in** | Semantic markup, contrast, target size, and focus are decided while writing the component, not patched later. |
| **Restrained motion** | Motion serves feedback and continuity. Respect `prefers-reduced-motion`. No decorative animation. |
| **Content first** | Whitespace is intentional. Decoration yields to content. |

---

## 3. Design Tokens

Tokens are the single source of truth, expressed as **CSS custom properties** following the M3 naming convention (`--md-sys-*`). **Component code references tokens only — never literals** (R1–R3).

Generate the color token set with the **Material Theme Builder** (export → "Web / CSS"). Store all tokens in `src/styles/tokens.css`, imported once at the app root.

Token layers:

| Layer | Description | Example |
|-------|-------------|---------|
| Reference | Raw palette / base values | seed color, tonal palette |
| System | Semantic, theme-aware roles | `--md-sys-color-primary`, `--md-sys-typescale-body-large-size` |
| Component | Values consumed inside a component | a button's container = `--md-sys-color-primary` |

Component code uses **System** and **Component** tokens only.

```
src/styles/
  tokens.css        // all --md-sys-* custom properties (light + dark)
  reset.css         // minimal normalize/reset
  base.css          // html/body defaults, font-family
```

---

## 4. Color System

### 4.1 Color Roles

M3 uses a tonal role system. Each "container/surface" color is **paired** with an `on*` foreground color; used together they guarantee contrast.

| Token | Use for |
|-------|---------|
| `--md-sys-color-primary` / `-on-primary` | Primary action, key interactive elements |
| `--md-sys-color-primary-container` / `-on-primary-container` | Emphasized container that does not compete with the primary action |
| `--md-sys-color-secondary` / `-secondary-container` | Secondary emphasis, filter chips |
| `--md-sys-color-tertiary` / `-tertiary-container` | Balancing accent, contrast highlights |
| `--md-sys-color-error` / `-error-container` | Errors, destructive actions, validation |
| `--md-sys-color-surface` / `-on-surface` | Default background and text |
| `--md-sys-color-surface-container-lowest` … `-highest` | Surfaces at different elevation levels ([§7](#7-elevation--layering)) |
| `--md-sys-color-on-surface-variant` | Secondary text, helper text, inactive icons |
| `--md-sys-color-outline` / `-outline-variant` | Borders, dividers |
| `--md-sys-color-inverse-surface` / `-inverse-on-surface` / `-inverse-primary` | Inverted contexts (e.g. toasts) |
| `--md-sys-color-surface-tint` | Elevation tint overlay |
| `--md-sys-color-scrim` | Modal scrim |

### 4.2 Rules

- **C1.** MUST derive the full color set from a single seed color (via Material Theme Builder).
- **C2.** MUST use paired roles (`primary` + `on-primary`, etc.). MUST NOT mix unrelated foreground/background colors.
- **C3.** Dark theme MUST be a first-class peer of light theme.
- **C4.** In dark theme, MUST NOT flood large areas with pure black; use `surface`. Express elevation via `surface-container-*` brightness + tint, not heavier shadows.
- **C5.** Fixed brand colors (e.g. logo) are reference tokens, kept separate, and MUST NOT change with theme.
- **C6.** Any custom color pair MUST be verified for contrast ([§13.2](#132-color--contrast)).

### 4.3 Theming Mechanism

Theme is controlled by a `data-theme` attribute on `<html>`, defaulting to the system preference and user-overridable:

```css
/* tokens.css — light is default in :root, dark overrides */
:root { /* --md-sys-color-* light values */ }

@media (prefers-color-scheme: dark) {
  :root:not([data-theme='light']) { /* --md-sys-color-* dark values */ }
}

:root[data-theme='dark'] { /* --md-sys-color-* dark values */ }
```

---

## 5. Typography

### 5.1 Type Scale

M3 defines 15 levels across 5 groups, exposed as typescale tokens (`--md-sys-typescale-{role}-{size|line-height|weight|font}`).

| Group | Role | Size (rem / px) | Line height | Weight | Typical use |
|-------|------|-----------------|-------------|--------|-------------|
| Display | `display-large` | 3.5625 / 57 | 4 / 64 | 400 | Hero text |
| | `display-medium` | 2.8125 / 45 | 3.25 / 52 | 400 | |
| | `display-small` | 2.25 / 36 | 2.75 / 44 | 400 | |
| Headline | `headline-large` | 2 / 32 | 2.5 / 40 | 400 | Page-level titles |
| | `headline-medium` | 1.75 / 28 | 2.25 / 36 | 400 | |
| | `headline-small` | 1.5 / 24 | 2 / 32 | 400 | |
| Title | `title-large` | 1.375 / 22 | 1.75 / 28 | 400 | App bar / card title |
| | `title-medium` | 1 / 16 | 1.5 / 24 | 500 | List item primary text |
| | `title-small` | 0.875 / 14 | 1.25 / 20 | 500 | |
| Body | `body-large` | 1 / 16 | 1.5 / 24 | 400 | Primary body text |
| | `body-medium` | 0.875 / 14 | 1.25 / 20 | 400 | Default text |
| | `body-small` | 0.75 / 12 | 1 / 16 | 400 | Helper text |
| Label | `label-large` | 0.875 / 14 | 1.25 / 20 | 500 | Button text |
| | `label-medium` | 0.75 / 12 | 1 / 16 | 500 | Small labels |
| | `label-small` | 0.6875 / 11 | 1 / 16 | 500 | Smallest labels |

> `rem` values assume the browser default of 16px. **Never** override the root `font-size` in `px` — it breaks user font-size preferences.

### 5.2 Rules

- **T1.** MUST apply typescale tokens (or a small set of utility classes built from them). MUST NOT set raw `font-size`.
- **T2.** Type role MUST follow semantics: `<h1>`–`<h6>` get headline/title roles; body text gets body roles. Visual size MUST NOT dictate heading level (R14).
- **T3.** A single screen SHOULD use ≤ 4 distinct type levels.
- **T4.** Body text line length SHOULD be 45–75 characters; constrain with `max-inline-size: 70ch` when wider.
- **T5.** Text SHOULD be `text-align: start`. MUST NOT use `justify`.
- **T6.** UI MUST remain functional under WCAG text-spacing overrides (line height 1.5×, paragraph spacing 2×, letter spacing 0.12em) — avoid fixed-height text containers.

---

## 6. Shape

M3 corner radius scale, exposed as shape tokens.

| Token | Radius | Typical components |
|-------|--------|--------------------|
| `--md-sys-shape-corner-none` | 0 | Full-bleed images |
| `--md-sys-shape-corner-extra-small` | 4px | Menus, small chip elements |
| `--md-sys-shape-corner-small` | 8px | Text fields, small cards |
| `--md-sys-shape-corner-medium` | 12px | Cards, dialog inner elements |
| `--md-sys-shape-corner-large` | 16px | Cards, large containers |
| `--md-sys-shape-corner-extra-large` | 28px | Dialogs, sheets |
| `--md-sys-shape-corner-full` | 9999px | Buttons, chips, FAB, search bar |

### 6.1 Rules

- **SH1.** MUST use shape tokens; MUST NOT use arbitrary `border-radius` values.
- **SH2.** Members of the same component family MUST share a radius.

---

## 7. Elevation & Layering

M3 expresses elevation primarily via **surface color/tint**, not shadows — critically so in dark theme.

| Level | Elevation | Surface role | Typical components |
|-------|-----------|--------------|--------------------|
| 0 | 0 | `surface` | Page background, resting cards |
| 1 | 1px | `surface-container-low` | Cards, elevated buttons |
| 2 | 3px | `surface-container` | App bar (scrolled), hovered chips |
| 3 | 6px | `surface-container-high` | FAB, dialogs, menus |
| 4 | 8px | `surface-container-high` | Navigation drawer |
| 5 | 12px | `surface-container-highest` | Dragged elements |

### 7.1 Rules

- **E1.** Distinguish layers using surface container colors; use `box-shadow` (via `--md-sys-elevation-*`) sparingly.
- **E2.** A single screen SHOULD show ≤ 3 elevation levels.
- **E3.** The app bar MUST raise from Level 0 to Level 2 once content scrolls beneath it.
- **E4.** In dark theme, higher elevation MUST mean a lighter surface, not a darker shadow.

---

## 8. Spacing & Layout Grid

### 8.1 Spacing Scale (4px base grid)

All spacing MUST be a multiple of 4. Expose as tokens; consume via `var()`.

| Token | Value | Use |
|-------|-------|-----|
| `--space-xs` | 4px | Tight element gaps |
| `--space-sm` | 8px | Intra-element spacing, icon padding |
| `--space-md` | 16px | **Default page margin**, card padding |
| `--space-lg` | 24px | Section spacing |
| `--space-xl` | 32px | Large section spacing |
| `--space-xxl` | 48px | Page-level partitioning |

### 8.2 Page Margins

| Window class | Inline page margin |
|--------------|--------------------|
| Compact | 16px |
| Medium | 24px |
| Expanded and above | 24px + `max-inline-size` content constraint |

### 8.3 Rules

- **SP1.** MUST use spacing tokens; MUST NOT use raw spacing literals.
- **SP2.** Prefer `gap` on flex/grid containers over margins for spacing between siblings.
- **SP3.** Long-form text and forms MUST set a `max-inline-size` (e.g. `40rem`).
- **SP4.** Use CSS Grid for page layout and 2D component layout; flexbox for 1D rows/columns.

---

## 9. Iconography & Imagery

### 9.1 Rules — Icons

- **IC1.** MUST use **Material Symbols** only (variable font or the `@material-symbols` SVG set). MUST NOT mix icon libraries.
- **IC2.** Standard icon size 24px; dense 20px; emphasis 40/48px. Size icons in `rem` where they should scale with text.
- **IC3.** Inactive icons use `on-surface-variant`; active icons use `primary`.
- **IC4.** A standalone icon control MUST be a `<button>` with an `aria-label`, and a ≥ 48×48px target (R6, R7).
- **IC5.** A decorative icon MUST be hidden from assistive tech (`aria-hidden="true"`).

### 9.2 Rules — Imagery

- **IM1.** `<img>` MUST always have an `alt` attribute. Informative images get descriptive `alt`; decorative images get `alt=""`.
- **IM2.** `<img>` MUST declare `width`/`height` (or `aspect-ratio`) to reserve space and prevent layout shift.
- **IM3.** Use responsive images (`srcset`/`sizes`) and `loading="lazy"` for below-the-fold media.
- **IM4.** Provide a loading placeholder (skeleton) and an error fallback state.
- **IM5.** Thumbnails MUST use a consistent radius (typically `corner-medium`, 12px).

---

## 10. Components

Default to `@material/web` custom elements for covered components; build the rest from semantic HTML + tokens following M3 specs. Wrap everything in shared Vue components (R12).

> `@material/web` elements are custom elements — register them with Vite/Vue:
> ```ts
> // vite.config.ts
> vue({ template: { compilerOptions: { isCustomElement: (t) => t.startsWith('md-') } } })
> ```

### 10.1 Buttons

| Type | Element | Use | Per-screen guidance |
|------|---------|-----|---------------------|
| Primary | `<md-filled-button>` | The single most important action | ≤ 1 |
| Secondary | `<md-filled-tonal-button>` | Important, not top-priority | Few |
| Emphasized outline | `<md-outlined-button>` | Alternative beside the primary | Few |
| Text | `<md-text-button>` | Low-emphasis (e.g. "Cancel") | Unlimited |
| Icon | `<md-icon-button>` | Toolbars, compact actions | Unlimited |
| Floating | `<md-fab>` | Screen-level core action | ≤ 1 |

Rules:
- **B1.** Button labels MUST be concise verb phrases (e.g. "Save", "Retry").
- **B2.** A button that submits a form MUST be `type="submit"`; otherwise `type="button"`.
- **B3.** While loading, a button MUST show progress, set `aria-busy`/`disabled`, and prevent duplicate submits.
- **B4.** Destructive actions MUST use the `error` role and MUST require confirmation.
- **B5.** A control that navigates MUST be an `<a>` (or router-link), not a button (R6).

### 10.2 Navigation Components

| Pattern | Window class | Notes |
|---------|--------------|-------|
| Bottom navigation bar | Compact | 3–5 top-level destinations |
| Navigation rail | Medium / Expanded | Side navigation |
| Navigation drawer | Expanded and above | Persistent; many destinations |
| Modal drawer | Compact | Temporary; overflow destinations |

Rules:
- **N1.** Top-level navigation MUST be a `<nav>` landmark with an accessible name.
- **N2.** The current destination MUST be marked `aria-current="page"`.
- **N3.** The same selection state MUST persist when the navigation form switches at breakpoints.
- See [§12.3](#123-adaptive-navigation).

### 10.3 Cards

- **CD1.** A single list MUST use one card variant (elevated / filled / outlined) only.
- **CD2.** Default card padding 16px; radius `corner-large`/`corner-medium`.
- **CD3.** A fully clickable card MUST wrap its primary action in a single `<a>`/`<button>`; MUST NOT nest multiple interactive elements ambiguously.

### 10.4 Inputs & Forms

- **F1.** Use `<md-outlined-text-field>` / `<md-filled-text-field>` consistently project-wide (one style).
- **F2.** Every field MUST have a programmatically associated, persistently visible label (`<label for>` or the element's `label`). Placeholder MUST NOT be the only label.
- **F3.** Group related controls with `<fieldset>` + `<legend>`.
- **F4.** Required fields MUST be marked (`required` + visible indicator). Invalid fields MUST set `aria-invalid="true"` and link the message via `aria-describedby`.
- **F5.** On submit failure, focus MUST move to the first invalid field; an error summary SHOULD be exposed via a live region.
- **F6.** Validation errors MUST use `error`-role text + icon, not color alone.

### 10.5 Feedback

| Scenario | Component | Notes |
|----------|-----------|-------|
| Lightweight notice | Snackbar/toast | Brief, ≤ 1 action; announced via polite live region |
| User decision needed | `<md-dialog>` | Blocking; use sparingly; traps focus |
| Loading | `<md-circular-progress>` / skeleton | Any wait > ~300ms MUST show feedback |
| Empty state | Shared empty-state component | Illustration + text + optional action |
| Error | Shared error component | Cause + retry entry point |

### 10.6 Lists

- **L1.** Use `<ul>`/`<ol>` + `<li>` for semantic lists; `<md-list>` for M3 styling.
- **L2.** Long/large lists MUST be virtualized (e.g. a virtual-scroller) for performance.
- **L3.** Separate rows with either a divider (`outline-variant`) or whitespace — not both.

---

## 11. Motion

### 11.1 Duration

| Tier | Duration | Use |
|------|----------|-----|
| Short | 50–200ms | Small state changes, ripple, toggles |
| Medium | 250–400ms | Component enter/exit, expand/collapse |
| Long | 450–600ms | Large transitions, route changes |
| Extra long | 700–1000ms | Large expressive transitions (rare) |

### 11.2 Easing (M3 motion tokens)

| Token | Use |
|-------|-----|
| `--md-sys-motion-easing-standard` | Most standard transitions |
| `--md-sys-motion-easing-emphasized` | Prominent enter/exit |
| `--md-sys-motion-easing-emphasized-decelerate` | Elements entering the screen |
| `--md-sys-motion-easing-emphasized-accelerate` | Elements leaving the screen |

### 11.3 Rules

- **M1.** Motion MUST serve feedback, spatial continuity, or attention — never pure decoration.
- **M2.** Entering elements use a decelerate curve; leaving elements use an accelerate curve.
- **M3.** Route transitions MUST use a single shared `<Transition>`/`<RouterView>` wrapper.
- **M4.** MUST respect `prefers-reduced-motion`:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
  ```
  Components SHOULD also branch in script via `usePreferredReducedMotion()` (VueUse) for JS-driven animation.
- **M5.** MUST NOT autoplay looping/large motion that cannot be paused.

---

## 12. Responsive & Adaptive Design

> **Responsive:** layout scales/reflows continuously with size.
> **Adaptive:** layout switches structure/components at breakpoints (e.g. bottom nav → side rail).
> This project requires **both**.

### 12.1 Window Size Classes

Classified by **viewport (or container) width**, not device.

| Class | Width | Typical |
|-------|-------|---------|
| **Compact** | 0–599px | Phone, narrow window |
| **Medium** | 600–839px | Portrait tablet, large phone landscape, split window |
| **Expanded** | 840–1199px | Landscape tablet, small desktop window |
| **Large** | 1200–1599px | Desktop |
| **Extra-large** | ≥ 1600px | Large/ultrawide desktop |

Breakpoint custom properties + a composable:

```ts
// src/composables/useWindowSizeClass.ts
import { computed } from 'vue'
import { useMediaQuery } from '@vueuse/core'

export type WindowSizeClass =
  | 'compact' | 'medium' | 'expanded' | 'large' | 'extraLarge'

export function useWindowSizeClass() {
  const isMedium = useMediaQuery('(min-width: 600px)')
  const isExpanded = useMediaQuery('(min-width: 840px)')
  const isLarge = useMediaQuery('(min-width: 1200px)')
  const isExtraLarge = useMediaQuery('(min-width: 1600px)')

  const sizeClass = computed<WindowSizeClass>(() => {
    if (isExtraLarge.value) return 'extraLarge'
    if (isLarge.value) return 'large'
    if (isExpanded.value) return 'expanded'
    if (isMedium.value) return 'medium'
    return 'compact'
  })

  return { sizeClass }
}
```

### 12.2 Breakpoint Behavior

| Aspect | Compact | Medium | Expanded and above |
|--------|---------|--------|---------------------|
| Columns | 1 | 1–2 | Multi-column / list-detail side-by-side |
| Navigation | Bottom bar | Navigation rail | Navigation rail or drawer |
| Page margin | 16px | 24px | 24px + max content width |
| FAB | Standard | Standard / Extended | Extended FAB |
| Dialogs | Full-screen / bottom sheet | Centered dialog | Centered dialog |

### 12.3 Adaptive Navigation

Navigation structure MUST switch with window class; the **selected destination MUST persist across forms** (N3).

- **Compact:** bottom navigation bar (3–5 items). Overflow → "More" or modal drawer.
- **Medium:** navigation rail (collapsible).
- **Expanded and above:** expanded rail, or persistent drawer when destinations are numerous.

```vue
<!-- src/components/layout/AppShell.vue -->
<script setup lang="ts">
import { useWindowSizeClass } from '@/composables/useWindowSizeClass'
import AppNavBar from './AppNavBar.vue'
import AppNavRail from './AppNavRail.vue'
import AppNavDrawer from './AppNavDrawer.vue'

const { sizeClass } = useWindowSizeClass()
</script>

<template>
  <div class="app-shell" :data-size="sizeClass">
    <AppNavDrawer
      v-if="sizeClass === 'large' || sizeClass === 'extraLarge'" />
    <AppNavRail
      v-else-if="sizeClass === 'medium' || sizeClass === 'expanded'"
      :extended="sizeClass === 'expanded'" />

    <main class="app-shell__content">
      <slot />
    </main>

    <AppNavBar v-if="sizeClass === 'compact'" />
  </div>
</template>

<style scoped>
.app-shell {
  display: grid;
  min-block-size: 100dvh;
  grid-template-columns: auto 1fr;
}
.app-shell[data-size='compact'] {
  grid-template-columns: 1fr;
  grid-template-rows: 1fr auto;
}
.app-shell__content {
  padding-inline: var(--space-md);
  overflow: auto;
}
</style>
```

### 12.4 Canonical Layouts

Apply one of M3's four canonical layouts before designing a custom one.

| Layout | Description | Compact | Expanded |
|--------|-------------|---------|----------|
| **List-Detail** | Master/detail | Two separate routes | List + detail side-by-side |
| **Supporting Pane** | Main + supporting info | Supporting content collapses to sheet/tab | Main area + right supporting pane |
| **Feed** | Card grid | Single column | Multi-column grid; columns scale with width |
| **Single Column** | Forms, reading detail | Full width | Centered, `max-inline-size` (e.g. `40rem`) |

Implementation rules:
- **RD1.** Choose structure with the size-class composable or CSS media queries; reflow with CSS Grid/flex.
- **RD2.** For component-level responsiveness, prefer **container queries** (`@container`) over viewport media queries so a component adapts to its slot, not the page.
- **RD3.** List-Detail MUST keep the selected item when expanding; when shrinking to Compact, fall back sensibly to list or detail route.
- **RD4.** Grid column count MUST switch at breakpoints, not at arbitrary pixel values. `repeat(auto-fill, minmax(<token>, 1fr))` is acceptable when the min size is a defined token.

### 12.5 Input-Mode Adaptation

UI MUST adapt to input method, not only size.

- **Touch:** targets ≥ 48×48px; ensure tap and swipe affordances work.
- **Mouse:** `:hover` states, correct `cursor`, optional context menus.
- **Keyboard:** every interaction reachable and operable; visible focus ([§13.6](#136-keyboard--focus)).
- **Coarse vs fine pointer:** MAY use `@media (pointer: coarse)` to enlarge targets; never shrink below 48px on coarse pointers.
- Layout MUST reflow live on window resize and zoom — no reload required.

### 12.6 Reflow & Zoom

- **RZ1.** Content MUST reflow with no loss of information or function, and no two-axis scrolling, down to a **320 CSS px** viewport width / at **400% zoom** (WCAG 1.4.10 Reflow). Exception: data tables and other content that genuinely requires 2D.
- **RZ2.** Use `dvh`/`svh` (not `vh`) for full-height layouts to handle mobile browser chrome.
- **RZ3.** Respect safe-area insets with `env(safe-area-inset-*)` where the app is installable / fullscreen.

### 12.7 Responsive Rules

- **RR1.** MUST NOT branch layout on user-agent sniffing. Branch on size class / feature queries.
- **RR2.** MUST NOT ship per-device duplicate views. One view, breakpoint-conditional rendering.
- **RR3.** Use fluid sizing (`%`, `fr`, `clamp()`, `min()`, `max()`); avoid fixed `px` dimensions (R11).

---

## 13. Accessibility

Accessibility is **mandatory**, targeting **WCAG 2.1 AA** (and WCAG 2.2 additions where applicable). Every screen MUST satisfy this section before completion.

### 13.1 Semantic HTML First

- **A1.** Use the correct native element for the job: `<button>` for actions, `<a>` for navigation, `<input>`/`<select>`/`<textarea>` for input, `<nav>/<main>/<header>/<footer>/<aside>` for landmarks, `<ul>/<ol>/<li>` for lists, `<table>` for tabular data (R6, R14).
- **A2.** ARIA is a last resort. Add `role`/`aria-*` only when no native element provides the semantics. **No ARIA is better than bad ARIA.**
- **A3.** Each page MUST have one `<h1>` and a logical, gap-free heading outline.
- **A4.** Provide a "Skip to main content" link as the first focusable element.
- **A5.** Set `<html lang="…">`; update it when the UI language changes.

### 13.2 Color & Contrast

| Content type | Minimum contrast (AA) |
|--------------|------------------------|
| Body text (< 24px, or < 18.66px bold) | **4.5 : 1** |
| Large text (≥ 24px, or ≥ 18.66px bold) | **3 : 1** |
| UI component bounds, icons, focus indicators, non-text graphics | **3 : 1** |
| Decorative elements | None |

- **A6.** M3 `on-*` roles meet contrast when used as pairs — using pairs satisfies this by default.
- **A7.** Any custom color pair MUST be verified with a contrast tool.
- **A8.** MUST NOT express "secondary" via low-contrast text; use size/weight instead.
- **A9.** SHOULD honor `prefers-contrast: more` with a higher-contrast token set where feasible.

### 13.3 Target Size

- **A10.** Interactive targets MUST be ≥ **48×48 CSS px** (Material recommendation). The absolute WCAG 2.2 AA floor is 24×24px — never go below it, and never below 48px for primary touch targets.
- **A11.** Adjacent targets MUST have ≥ 8px spacing.
- **A12.** Enlarge small visuals' hit area via padding on the interactive element, not a separate overlay.

### 13.4 Dynamic Type & Scaling

- **A13.** MUST support 200% zoom and large browser font sizes without loss of content/function (R9).
- **A14.** Size text and many spacings in `rem`/`em` so they respond to user font-size settings.
- **A15.** The viewport meta MUST allow scaling: `<meta name="viewport" content="width=device-width, initial-scale=1">` — no `user-scalable=no`, no `maximum-scale`.
- **A16.** Containers MUST tolerate WCAG text-spacing overrides (T6) — avoid fixed heights on text.

### 13.5 Semantics & Screen Readers

Support NVDA, JAWS, and VoiceOver.

- **A17.** Every interactive element MUST have an accessible name (visible text, `aria-label`, or `aria-labelledby`).
- **A18.** Icon-only controls MUST have `aria-label`; decorative icons MUST be `aria-hidden="true"`.
- **A19.** Accessible names MUST NOT include the role word ("button", "link") — the role conveys it.
- **A20.** Dynamic updates MUST be announced via live regions (`aria-live="polite"` for status, `assertive` for errors) or `role="status"`/`role="alert"`.
- **A21.** State MUST be exposed via ARIA where native HTML cannot: `aria-expanded`, `aria-selected`, `aria-current`, `aria-pressed`, `aria-busy`.
- **A22.** Content hidden visually MUST also be hidden from AT when appropriate (`hidden`, `display:none`); content for AT only uses a visually-hidden utility (not `display:none`).

### 13.6 Keyboard & Focus

- **A23.** All functionality MUST be operable by keyboard alone, in an order matching the visual/reading order.
- **A24.** Focus MUST be visible. MUST NOT remove outlines without an equally clear replacement; prefer `:focus-visible` and ensure ≥ 3:1 contrast for the indicator.
- **A25.** MUST NOT create keyboard traps — any region entered must be exitable via keyboard.
- **A26.** Dialogs/modals MUST trap focus while open and restore focus to the trigger on close.
- **A27.** Composite widgets (menus, tabs, listboxes) MUST implement the expected keyboard model (arrow keys, `Home`/`End`, roving `tabindex`) per the ARIA Authoring Practices.
- **A28.** Support common shortcuts (`Esc` closes overlays, `Enter`/`Space` activate). MUST NOT override critical browser/AT shortcuts.
- **A29.** MUST NOT use positive `tabindex` values; use DOM order or `tabindex="0"` / `tabindex="-1"`.

### 13.7 Forms

- **A30.** Every control MUST have a programmatically associated, persistently visible label.
- **A31.** Errors MUST be conveyed by text + icon, linked via `aria-describedby`, with `aria-invalid` set; focus moves to the first invalid field.
- **A32.** Required fields and format requirements MUST be visible and announced before submission.
- **A33.** Use appropriate `type`, `inputmode`, and `autocomplete` attributes to ease input and assistive entry.

### 13.8 Motion & Sensory

- **A34.** MUST respect `prefers-reduced-motion` (M4).
- **A35.** MUST NOT flash content more than 3 times per second (photosensitivity risk).
- **A36.** Auto-updating/auto-advancing content MUST be pausable and MUST NOT steal focus.

### 13.9 Content & Language

- **A37.** Copy MUST be clear and concise; avoid ambiguity and unexplained jargon.
- **A38.** Link/button text MUST be self-descriptive (avoid "click here", "read more" with no context).
- **A39.** Use logical CSS properties and `dir` to keep RTL viable (R10).

### 13.10 Accessibility Testing

The agent MUST integrate accessibility checks:

- **Lint:** enable `eslint-plugin-vuejs-accessibility` in the project ESLint config.
- **Automated:** run `axe-core` (e.g. via `@axe-core/playwright` or `vitest-axe`) against key views; zero violations is the bar.
- **Audit:** Lighthouse accessibility score tracked in CI.
- **Manual (when feasible):** keyboard-only walkthrough of core flows; one screen-reader pass (NVDA or VoiceOver); regression at 200% zoom, 320px width, and with `prefers-reduced-motion`.

> Automated tools catch ~30–40% of issues. Keyboard + screen-reader checks are still required.

---

## 14. Theme & Token Implementation

Copy these templates directly.

### 14.1 `tokens.css` (excerpt)

```css
/* src/styles/tokens.css — generated color values via Material Theme Builder */
:root {
  /* Color — light (default) */
  --md-sys-color-primary: #4a6fa5;
  --md-sys-color-on-primary: #ffffff;
  --md-sys-color-surface: #fdfcff;
  --md-sys-color-on-surface: #1a1c1e;
  --md-sys-color-surface-container: #eef0f4;
  /* …full role set… */

  /* Shape */
  --md-sys-shape-corner-small: 8px;
  --md-sys-shape-corner-medium: 12px;
  --md-sys-shape-corner-large: 16px;
  --md-sys-shape-corner-extra-large: 28px;
  --md-sys-shape-corner-full: 9999px;

  /* Spacing */
  --space-xs: 4px;  --space-sm: 8px;  --space-md: 16px;
  --space-lg: 24px; --space-xl: 32px; --space-xxl: 48px;

  /* Typescale (example: body-large) */
  --md-sys-typescale-body-large-size: 1rem;
  --md-sys-typescale-body-large-line-height: 1.5rem;
  --md-sys-typescale-body-large-weight: 400;

  /* Motion */
  --md-sys-motion-duration-short: 150ms;
  --md-sys-motion-duration-medium: 300ms;
  --md-sys-motion-duration-long: 500ms;
  --md-sys-motion-easing-standard: cubic-bezier(0.2, 0, 0, 1);
  --md-sys-motion-easing-emphasized: cubic-bezier(0.2, 0, 0, 1);
}

/* Dark theme: follow system unless explicitly set to light */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme='light']) {
    --md-sys-color-primary: #adc7ff;
    --md-sys-color-on-primary: #002f65;
    --md-sys-color-surface: #1a1c1e;
    --md-sys-color-on-surface: #e3e2e6;
    --md-sys-color-surface-container: #1e2022;
    /* …full dark role set… */
  }
}
/* Explicit override */
:root[data-theme='dark'] { /* …same dark role set… */ }
```

### 14.2 Theme Composable

```ts
// src/composables/useTheme.ts
import { ref, watchEffect } from 'vue'

type ThemeMode = 'system' | 'light' | 'dark'
const mode = ref<ThemeMode>(
  (localStorage.getItem('theme') as ThemeMode) ?? 'system',
)

export function useTheme() {
  watchEffect(() => {
    const root = document.documentElement
    if (mode.value === 'system') root.removeAttribute('data-theme')
    else root.setAttribute('data-theme', mode.value)
    localStorage.setItem('theme', mode.value)
  })
  return { mode }
}
```

### 14.3 Token Usage in a Component

```vue
<!-- CORRECT — references tokens only -->
<style scoped>
.card {
  background: var(--md-sys-color-surface-container-low);
  color: var(--md-sys-color-on-surface);
  border-radius: var(--md-sys-shape-corner-large);
  padding: var(--space-md);
}
.card__title {
  font-size: var(--md-sys-typescale-title-large-size);
  line-height: var(--md-sys-typescale-title-large-line-height);
}
</style>

<!-- WRONG — hardcoded (violates R1–R3) -->
<style scoped>
.card { background: #eef0f4; border-radius: 16px; padding: 16px; }
.card__title { font-size: 22px; color: #1a1c1e; }
</style>
```

### 14.4 Accessible Icon Button Component

```vue
<!-- src/components/base/AppIconButton.vue -->
<script setup lang="ts">
defineProps<{
  /** Visible-to-AT name; required. */
  label: string
  icon: string
  active?: boolean
}>()
defineEmits<{ (e: 'click'): void }>()
</script>

<template>
  <button
    type="button"
    class="icon-button"
    :class="{ 'icon-button--active': active }"
    :aria-label="label"
    @click="$emit('click')"
  >
    <span class="material-symbols-rounded" aria-hidden="true">{{ icon }}</span>
  </button>
</template>

<style scoped>
.icon-button {
  /* >= 48x48 target (R7, A10) */
  inline-size: 3rem;
  block-size: 3rem;
  display: inline-grid;
  place-items: center;
  border: none;
  border-radius: var(--md-sys-shape-corner-full);
  background: transparent;
  color: var(--md-sys-color-on-surface-variant);
  cursor: pointer;
  transition: background var(--md-sys-motion-duration-short)
    var(--md-sys-motion-easing-standard);
}
.icon-button:hover { background: color-mix(in srgb,
  var(--md-sys-color-on-surface) 8%, transparent); }
.icon-button:focus-visible {
  outline: 2px solid var(--md-sys-color-primary);
  outline-offset: 2px;
}
.icon-button--active { color: var(--md-sys-color-primary); }
</style>
```

---

## 15. Code Organization & Naming

### 15.1 Directory Structure

```
src/
  styles/        // tokens.css, reset.css, base.css
  components/
    base/        // generic, spec-compliant building blocks
    layout/      // AppShell, nav components
    shared/      // cross-feature business components
  composables/   // useTheme, useWindowSizeClass, …
  views/         // route-level pages
  router/
  locales/       // i18n message catalogs
  assets/
```

### 15.2 Rules

- **O1.** Any UI used in more than one place MUST be a shared component (R12).
- **O2.** Components MUST expose semantic props/slots, not style internals; colors/radii resolve internally from tokens.
- **O3.** Every base component MUST support light/dark themes, zoom/font scaling, keyboard operation, and correct semantics.
- **O4.** Components MUST be SFCs with `<script setup lang="ts">` and `<style scoped>` (R13).
- **O5.** Component file/name in `PascalCase` and purpose-describing: `PrimaryActionButton.vue`, `SectionCard.vue`, `EmptyState.vue`.
- **O6.** Props/events `camelCase` in script, `kebab-case` in templates; emits declared explicitly and typed.
- **O7.** Token names are semantic and stable — `--space-md`, `--md-sys-color-primary` — never visual-appearance names.
- **O8.** All user-facing strings MUST go through i18n (`locales/`), never hardcoded inline.

---

## 16. Definition of Done

Run this checklist before marking any UI task complete. Every item MUST pass.

**Tokens & Theming**
- [ ] No hardcoded colors; all from `var(--md-sys-color-*)` (R1).
- [ ] No hardcoded `font-size`/`line-height`/`weight`; typescale tokens, text in `rem` (R2).
- [ ] No raw spacing/radius/elevation/duration literals; all from tokens (R3).
- [ ] Light and dark themes both implemented and verified (R4).
- [ ] Component styles are `<style scoped>` (R13).

**Responsive / Adaptive**
- [ ] Usable in Compact, Medium, and Expanded (R5).
- [ ] Navigation structure switches by window class; `aria-current` + selection persist (12.3).
- [ ] Reflows with no info loss and no 2-axis scroll at 320px / 400% zoom (RZ1).
- [ ] An appropriate canonical layout is applied; container queries used for component-level adaptation (12.4).
- [ ] No user-agent sniffing for layout (RR1).

**Accessibility**
- [ ] Semantic HTML used; one `<h1>`, gap-free headings, landmarks present (R6, R14, A1–A3).
- [ ] Skip link present; `<html lang>` set (A4, A5).
- [ ] Text contrast ≥ 4.5:1 (≥ 3:1 large / non-text) (13.2).
- [ ] All targets ≥ 48×48px with an accessible name (R7, A10, A17).
- [ ] No color-only information (R8).
- [ ] Survives 200% zoom; viewport allows scaling (R9, A13–A15).
- [ ] Fully keyboard operable; focus visible; no traps; modals trap+restore focus (13.6).
- [ ] Dynamic updates announced via live regions (A20).
- [ ] `prefers-reduced-motion` respected (M4, A34).
- [ ] `axe-core` reports zero violations; a11y lint passes (13.10).

**Structure**
- [ ] Reusable UI extracted into shared components (R12, O1).
- [ ] User-facing strings localized via i18n (O8).

---

## 17. References

- Material Design 3: https://m3.material.io
- Material Web (`@material/web`): https://github.com/material-components/material-web
- Material Theme Builder: https://material-foundation.github.io/material-theme-builder/
- Vue 3 docs: https://vuejs.org
- Vue accessibility guide: https://vuejs.org/guide/best-practices/accessibility
- VueUse: https://vueuse.org
- WCAG 2.1 / 2.2: https://www.w3.org/TR/WCAG22/
- ARIA Authoring Practices Guide: https://www.w3.org/WAI/ARIA/apg/
- MDN — CSS logical properties, container queries, `prefers-*` media features

---

> Living document. Update as the project evolves. The seed color (`#4a6fa5`),
> font choices, and the token values in §14 are placeholders — replace with real
> brand values (regenerate via Material Theme Builder) before use.

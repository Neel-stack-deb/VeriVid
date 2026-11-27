# VeriVid UI Audit — Phase 5.1

## Scope

Next.js 15 app under `frontend/src` with routes: `/` (landing), `/app` (workspace), `/app/demo`, `/app/videos/[videoId]`, `/app/videos/[videoId]/analysis`.

## Current design issues

- **Tokens**: `globals.css` defines only five raw hex variables; pages hard-code `#08090d`, `#12131a`, etc. across components.
- **Hero contrast**: Landing hero relies on flat dark backgrounds; product preview is `hidden` below `lg`, so mobile/tablet users miss the product story.
- **Product preview**: Minimal list of four labels — does not represent analysis UI, Debate Council, or scene intelligence.
- **Landing**: Missing dedicated final CTA section; workflow includes "Upload" as a fifth step while marketing copy says Perceive → Structure → Reason → Present (inconsistent with hero workflow array).
- **API health**: Workspace only shows disconnected state (`apiReachable === false`); no "checking" or explicit connected indicator.
- **Results page**: Long vertical scroll with no section navigation; transcript mixes full text and segments without clear hierarchy.
- **Debate Council**: Functional but uniform styling; consensus culmination is only a subtle ring.
- **Sidebar**: No mobile collapse; full-width sidebar stacks above content on small screens without overlay pattern.
- **Loading**: Plain text "Loading…" without skeleton placeholders.
- **Empty states**: Generic copy; upload area is the focus but empty workspace card adds little.

## Component inconsistencies

- Border radius alternates `rounded-lg`, `rounded-xl`, `rounded-2xl` without a rule.
- Buttons use inline Tailwind; cards duplicate `border-zinc-800 bg-[#12131a]`.
- Error alerts use similar rose styling but different padding/radius in workspace vs analysis.
- Active nav uses `bg-violet-500/10` (acceptable) but matches no shared `nav-active` token.

## Typography problems

- Geist is loaded correctly; scale is ad hoc (`text-2xl` page titles, `text-4xl` hero) with no documented scale.
- Too many `font-semibold` headings; supporting text sometimes `text-zinc-500` on `#08090d` (acceptable but not tokenized).
- Mono used only for video IDs — good; transcript timestamps could use mono for scanability.

## Layout problems

- Content widths: `max-w-3xl` workspace, `max-w-4xl` processing, `max-w-5xl` analysis — intentional but undocumented.
- Landing sections use `max-w-6xl` consistently — good.
- Results Debate Council `lg:grid-cols-4` can feel cramped; needs mobile stacking with visible flow.

## Accessibility issues

- `prefers-reduced-motion` honored in `globals.css` and Debate Council — good.
- Focus rings on buttons — good.
- Product preview stage icons use `aria-label` on pipeline — good.
- Sidebar mobile: needs keyboard-reachable menu control.
- Some `details/summary` for reports — keyboard accessible but focus style weak.

## Proposed design system

### Semantic colors (CSS variables)

| Token | Role |
|-------|------|
| `--bg-base` | Page background `#09090B` |
| `--bg-muted` | Secondary `#0F1014` |
| `--bg-elevated` | Cards `#14151B` |
| `--bg-hover` | Hover `#1B1C24` |
| `--text-primary` | `#F4F4F5` |
| `--text-secondary` | `#A1A1AA` |
| `--text-muted` | `#71717A` |
| `--border-default` | zinc subtle |
| `--accent` | violet `#8B5CF6` |
| `--success` / `--warning` / `--error` | emerald / amber / rose muted |

### Typography scale

- Display: landing hero
- Page title: `text-2xl font-semibold tracking-tight`
- Section: `text-lg font-medium`
- Body: `text-sm` / `text-base`
- Meta: `text-xs` uppercase labels

### Spacing

- Page: `px-4 sm:px-6`, vertical `py-8 lg:py-10`
- Card: `p-5`, header border-bottom
- Section gap: `space-y-6` / `gap-6`

### Shared components

- Standardize `Button`, `Card`, `Badge`, add `ConnectionStatus`, `Skeleton`, `SectionTabs` (results), `DemoBanner`, `ProductPreview` (landing).

## Implementation order

1. Expand `globals.css` tokens and utility classes.
2. Refactor UI primitives to consume tokens.
3. Landing: hero contrast, rich preview, workflow alignment, final CTA.
4. App shell: mobile sidebar + connection status hook/component.
5. Workspace upload polish.
6. Processing page skeletons and pipeline visuals.
7. Analysis: tabbed layout, transcript/scene/knowledge/council polish.
8. Demo persistent banner.
9. Tests, build, screenshots, `UI_POLISH_REPORT.md`.
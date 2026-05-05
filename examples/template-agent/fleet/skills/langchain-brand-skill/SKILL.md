---
name: langchain-brand-skill
description: Design guidelines for 2026 LangChain brand
---

```
---
name: langchain-brand-guidelines
description: Applies LangChain's official brand colors, typography, and visual identity to any sort of artifact that may benefit from having LangChain's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply. Make sure to use this skill whenever the user mentions LangChain branding, brand colors, brand styling, visual identity, corporate identity, or wants to apply LangChain's design system to any output — even if they don't explicitly say "brand guidelines."
---

# LangChain Brand Styling

## Overview

To access LangChain's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, LangChain brand, visual formatting, visual design, LangSmith, LangGraph

## Brand Guidelines

### Colors

**Primary Brand Palette — Dark Blue Family:**

- Dark Blue: `#030710` — Primary dark background, replaces pure black in light mode
- Dark Shade 1: `#0D1322` — Secondary dark background (darkmode UI)
- Dark Shade 2: `#161F34` — Accent dark background
- Dark Shade 3: `#2F4B68` — Dark accent
- Dark Shade 4: `#40668D` — Mid-dark accent
- Blue: `#006DDD` — Core brand blue, used in gradients and accents

**Primary Brand Palette — Light Blue Family:**

- Light Blue: `#7FC8FF` — Primary light accent, logomark on dark backgrounds
- Light Tint 1: `#99D3FF`
- Light Tint 2: `#B2DEFF`
- Light Tint 3: `#CCE9FF`
- Light Tint 4: `#E5F4FF`
- Light Tint 5: `#F2FAFF` — Replaces pure white in light mode UI

**Extended Product Palette:**

- Plum: `#885270` (deep: `#441E33`, light: `#C78EAD`, lighter: `#EBD0F0`)
- Purple: `#504B5F` (mid: `#7E65AE`, light: `#D5C3F7`, lighter: `#FDF3FF`)
- Peach: `#634643` (mid: `#FBB0A5`, light: `#B27D75`, lighter: `#F8E8E6`) — Deepest shade reserved for warning states only
- Green: `#6E8900` (deep: `#2E3900`, light: `#E3FF8F`, lighter: `#F6FFDB`)

**Gradients (only these three are permitted):**

Gradients are created combining colors from the core palette. They add an elevated, technical quality to graphic language and product diagrams. Gradients can be applied to solid and dotted lines or nodes. They should NOT be used as backgrounds. Do not create any gradient combinations other than these three:

- Dark Blue → Blue: `#030710` → `#006DDD`
- Dark Blue → Light Blue: `#030710` → `#7FC8FF`
- Blue → Light Blue: `#006DDD` → `#7FC8FF`

**Color Rules:**

- Do not create new colors outside the palette
- Do not overlay colors
- Do not set type in colors not specified in the system
- In darkmode: use Dark Blue / Dark Shade 1 as backgrounds, lighter tints for text and accents
- In lightmode: use Dark Blue (`#030710`) instead of pure black, Light Tint 5 (`#F2FAFF`) instead of pure white
- Always select color combinations with the highest legibility

### Typography

**Primary Typeface: Lausanne**

- Weights: 600 Bold, 400 Medium, 250 Regular
- 600 Bold should be used sparingly — headlines are typically set in 250 Regular for a lightweight aesthetic
- Open-source fallback: **Inter**

**Secondary Typeface: Aeonik Mono**

- Weights: Medium, Regular, Light
- Used for product names (lowercase), code, short body copy, CTAs, and H2 headings
- Open-source fallback: **IBM Plex Mono**

**Typographic Hierarchy:**

- **H1**: Lausanne / Inter, **Weight 300 (default)**, Tracking -2%, Leading 100%, Title Case
- **H2**: Aeonik Mono / IBM Plex Mono, Regular (400), Tracking 0%, Leading 110%, Sentence case
- **Long Body Copy**: Lausanne / Inter, Weight 300 + 600, Tracking 0%, Leading 130%, Sentence case
- **Short Body Copy**: Aeonik Mono / IBM Plex Mono, Regular (400), Tracking -1%, Leading 140%, Sentence case
- **Code**: Aeonik Mono / IBM Plex Mono, Regular (400), Tracking 0%, Leading 170%, Lowercase
- **Caption & CTA**: Aeonik Mono / IBM Plex Mono, Regular (400), Tracking -2%, Leading 115%, Title Case

**Headers must default to weight 300 (light).** This is a defining characteristic of the LangChain brand — headlines are intentionally lightweight. Weight 600 (semi bold) should only be used sparingly for emphasis within body copy, never for headings.

**Typography Rules:**

- Do not outline type
- Do not use unapproved type weights
- Do not apply effects to type
- Do not justify text
- Do not apply overly loose tracking
- Do not use low contrast color combinations

### Border Radius

LangChain uses subtle, tight corner rounding — not bubbly or heavily rounded. The reference ratio is **12px radius on a ~700px wide element**. Scale proportionally:

- **4px** — small buttons, tags, inline elements
- **6px** — standard buttons, input fields
- **8px** — small cards, dropdowns, tooltips
- **10px** — medium cards, modals
- **12px** — large cards, sections, containers (~700px+)
- **14px** — floating nav bars, hero containers
- **100px (pill)** — pill-shaped buttons and tags only

Do not use radius values above 14px for rectangular containers. Product icon pills use ~20px radius at 100px size (matching the brand spec), but this is specific to icon pills and should not be applied to cards or layout containers.

### Brand Architecture

- **LangChain** — Parent brand
- **LangSmith** — Sub-brand / Platform (services: Observability, Evaluation, Deployment, Fleet)
- **LangGraph** — Open source framework
- **Deep Agents** — Open source framework
- **Company Logos**: LangChain Academy, LangChain Labs, LangChain Docs, LangChain Reference, LangChain Support, LangChain Community, LangChain Blog

### Logo & Lockup System

**Full Lockup** (icon + wordmark) = The default. Use this whenever the LangChain logo appears standalone — in navigation, headers, hero sections, footers, social profiles, favicons at large size, and any context where the logo represents the brand on its own.

**Wordmark only** = Use ONLY when "LangChain" appears inline within a sentence or paragraph of text. The wordmark replaces the plain-text name to add brand styling. The only stylized part of the sentence should be the wordmark — no icon accompanies it in this context.

**Symbol only** = acceptable when viewers are already very familiar with LangChain (e.g., app icon, favicon, small UI elements where the full lockup won't fit).

**LangSmith is a wordmark only** — it does not have its own symbol/icon. The LangChain symbol must NEVER be used in conjunction with the LangSmith wordmark. LangSmith service lockups pair the LangSmith wordmark with a service-specific icon pill, not the LangChain symbol.

Minimum size: 22px height. Clear space: defined by the quarter-circle dimension ("x") from the logomark. Do not stretch, wrap, outline, apply effects, reposition elements, or use off-brand colors.

**Always use the provided SVG files** — do not recreate logos or icons.

**CRITICAL: SVG file integrity.** When using logo/lockup SVG files, the internal path data (`d` attributes), `viewBox`, and all internal elements must remain byte-for-byte identical to the source file. Only the outer `width` and `height` attributes on the root `<svg>` element may be changed for display sizing. Never compress, simplify, re-type, or approximate SVG path data — this introduces visual artifacts (e.g., malformed letterforms). Always read the SVG file and use its contents unmodified.

**LangSmith service lockups** must always use the official SVG lockup files from `assets/logos/langsmith-platform/` (e.g., `LangSmith_Evaluation_dark.svg`). Never recreate a LangSmith lockup by combining a separate icon SVG with manually typed text.

**LangChain full lockup** (symbol + wordmark) must always be used in the navigation bar. Use the files from `assets/logos/company/` (e.g., `LangChain_Lockup_dark_mode_white.svg`). Never recreate the LangChain logo by drawing shapes and adding text.

All SVG assets are bundled in `assets/logos/` organized by category:

- `assets/logos/company/` — LangChain lockup, wordmark, icon; LangSmith wordmark (4 color variants each: dark mode blue, dark mode white, light mode dark blue, light mode black)
- `assets/logos/oss-lockups/` — LangChain, LangGraph, Deep Agents OSS lockups (dark + light)
- `assets/logos/langsmith-platform/` — Service lockups (Observability, Evaluation, Deployment), Fleet full set (lockup, wordmark, icon variants)
- `assets/logos/doc-icons/` — Product icon pills for docs/UI: LangChain, LangGraph, Deep Agents, Observability, Evaluation, Deployment, Prompt Engineering (dark + light)
- `assets/logos/sub-brands/` — Wordmark logomarks: Academy, Docs, Labs, Reference, Support, Community, LangSmith for Startups (dark + light)

### Logo Sizing & Aspect Ratios

**CRITICAL: Never stretch, squash, or distort logos.** Always preserve the original aspect ratio. When inserting logos into slides, documents, or layouts, set only the width OR the height — never both — and let the other dimension scale proportionally.

**SVG dimensions (width × height in px):**

| Logo | Dimensions | Ratio | Shape |
|---|---|---|---|
| LangChain Lockup | 613 × 113 | ~5.4:1 | Very wide |
| LangChain Wordmark | 578 × 113 | ~5.1:1 | Wide |
| LangChain Icon | 117 × 117 | 1:1 | Square |
| LangSmith Wordmark | 565 × 113 | 5:1 | Wide |
| OSS Lockups (LangChain, LangGraph) | 472 × 100 | ~4.7:1 | Wide |
| OSS Lockup (Deep Agents) | 510 × 100 | 5.1:1 | Wide |
| LangSmith Observability | 801 × 100 | 8:1 | Very wide |
| LangSmith Evaluation | ~720 × 100 | ~7.2:1 | Very wide |
| LangSmith Deployment | ~771 × 100 | ~7.7:1 | Very wide |
| LangSmith Fleet Lockup | 574 × 102 | ~5.6:1 | Wide |
| Doc Icons (all) | ~98 × 98 | 1:1 | Square |
| Sub-brand wordmarks | 640–833 × 100 | 6.4–8.3:1 | Very wide |

**For presentations (PPTX):**
- Set logo width to fit available space, let height auto-calculate — NEVER set both dimensions
- For wide lockups/wordmarks: use at most 60–70% of slide width
- For square icons: set a fixed height (e.g., 1 inch) and width will match
- Never place a wide logo inside a square container — it will squash
- When placing multiple logos in a row, normalize by height (not width) so they look balanced
- Add generous padding around logos (minimum clear space per brand rules)

**For HTML/React:**
- Use `width: auto; height: [value]` or `max-width: [value]; height: auto` — never set both fixed dimensions
- Apply `object-fit: contain` if using `<img>` tags inside fixed containers
- For inline SVGs, preserve the `viewBox` attribute and set only one dimension

### Logo Color Usage — Dark Mode vs Light Mode

All logos and icons have both dark mode and light mode variants.

**Dark Mode (on `#030710` or `#0D1322` backgrounds):**

- LangChain / LangGraph / Deep Agents (OSS): icon pill `#161F34`, symbol `#7FC8FF`, wordmark text `#FFFFFF`
- LangSmith (all services): icon pill `#7FC8FF`, symbol `#030710`, wordmark `#F2FAFF`
- LangSmith Fleet: icon `#7FC8FF` bg, `#030710` vector; wordmark `#7FC8FF` or `#FFFFFF`
- Prompt Engineering: icon `#7FC8FF` bg, `#030710` vector; text `#F2FAFF`
- Company wordmarks (Academy, Labs, Docs, etc.): `#7FC8FF` or `#F2FAFF`

**Light Mode (on `#F2FAFF` backgrounds):**

- LangChain / LangGraph / Deep Agents (OSS): icon pill `#161F34`, symbol `#7FC8FF`, wordmark text `#161F34`
- LangSmith (all services): icon pill `#030710`, symbol `#7FC8FF`, wordmark `#030710`
- LangSmith Fleet: icon `#030710` bg, `#7FC8FF` vector; wordmark `#030710`
- Prompt Engineering: icon `#030710` bg, `#7FC8FF` vector; text `#030710`
- Company wordmarks (Academy, Labs, Docs, etc.): `#030710`

**Black/White fallback (only when color is not an option):**

- Black (`#000000`) background → White (`#FFFFFF`) symbol/wordmark
- White (`#FFFFFF`) or `#F2FAFF` background → Black (`#000000`) symbol/wordmark

**Key rules:**
- OSS products (LangChain, LangGraph, Deep Agents) use `#161F34` as icon pill background in both modes, always `#7FC8FF` foreground
- LangSmith products invert per mode: `#7FC8FF` bg / `#030710` fg in dark; `#030710` bg / `#7FC8FF` fg in light
- OSS product names: Aeonik Mono Regular, lowercase
- LangSmith service names: TWK Lausanne Weight 250
- LangGraph icon is rotated 90° from base orientation
- Never use pure black/white except in the fallback scenario

### Product Icon Specifications

All product icons are rounded rectangles (`border-radius: 20px` at 100×100px). Icons ~97–100px at standard size.

**OSS icons (both modes):** pill `#161F34`, symbol `#7FC8FF`
**LangSmith icons dark mode:** pill `#7FC8FF`, symbol `#030710`
**LangSmith icons light mode:** pill `#030710`, symbol `#7FC8FF`

### Iconography System (Marketing Assets Only)

LangChain has a set of 6 brand-level icons used **exclusively in marketing assets** — such as headlines, large-scale graphic applications, and product illustrations. These icons visually contrast the product sub-brand icons to indicate a different level of hierarchy. Do NOT use these icons in product UI.

**Available icons** (bundled as SVG assets in `assets/icons/`):

| Icon | Dark Mode SVG | Light Mode SVG |
|---|---|---|
| Visibility and Control | `Visibility_and_Control_dark_mode.svg` | `Visibility_and_Control_light_mode.svg` |
| Fast Iteration | `Fast_Iteration_dark_mode.svg` | `Fast_Iteration_light_mode.svg` |
| Durable Performance | `Durable_Performance_dark_mode.svg` | `Durable_Performance_light_mode.svg` |
| Framework Neutral | `Framework_Neutral_dark_mode.svg` | `Framework_Neutral_light_mode.svg` |
| Agent Studio | `Agent_Studio_dark_mode.svg` | `Agent_Studio_light_mode.svg` |
| LLM | `LLM_dark_mode.svg` | `LLM_light_mode.svg` |

**Usage rules:**
- Use `_dark_mode` variants on dark backgrounds (`#030710`)
- Use `_light_mode` variants on light backgrounds (`#F2FAFF`)
- These are geometric line-art icons with 2.5px stroke weight
- Dark mode icons use `#F2FAFF` or light strokes; light mode icons use `#030710` strokes
- Always use the provided SVG files — do not recreate or modify them
- Icons should be used at large scale in marketing contexts (social media, presentations, website hero sections, blog graphics)
- Do NOT use these icons for product UI, app icons, or navigation elements
- **Do NOT create any new icons outside of this icon library.** Only the 6 icons listed above exist in the brand system. If a concept is not covered by an existing icon, use text or other brand elements instead — never invent new icons.

## Dual-Mode Export (Dark + Light)

When the user requests branded assets, **always produce both a dark mode and a light mode variant** unless the user explicitly asks for only one. This applies to all output types: HTML/React artifacts, presentations, social graphics, documents, and any other branded deliverable.

**For HTML / React artifacts:**
- Build the layout once with CSS custom properties (variables) for all theme-dependent colors
- Include a theme toggle (button or switch) that swaps between dark and light mode in real time
- Dark mode is the default / initial state (matching the primary website aesthetic)
- CSS variable mapping:

```
/* Dark mode (default) */
--bg-primary: #030710;
--bg-secondary: #0D1322;
--bg-card: #161F34;
--text-primary: #F2FAFF;
--text-secondary: #99D3FF;
--accent: #7FC8FF;
--accent-bright: #006DDD;

/* Light mode */
--bg-primary: #F2FAFF;
--bg-secondary: #E5F4FF;
--bg-card: #CCE9FF;
--text-primary: #030710;
--text-secondary: #161F34;
--accent: #7FC8FF;
--accent-bright: #006DDD;
```

- Swap logos/icons to the correct mode variant (use `_dark_mode` SVGs on dark backgrounds, `_light_mode` SVGs on light backgrounds)
- Product icon pills invert per the logo color rules (OSS icons keep `#161F34` pill in both modes; LangSmith icons swap)

**For static file exports (PPTX, PDF, DOCX, images):**
- Generate two separate files: `filename_dark.ext` and `filename_light.ext`
- Each file should be complete and self-contained
- Apply the correct logo, icon, and text color variants for each mode

**For SVG / image exports:**
- Export two variants with the appropriate background and foreground colors
- Name them with `_dark` and `_light` suffixes

**Mode-specific reminders:**
- Dark mode: backgrounds `#030710` / `#0D1322`, text `#F2FAFF`, accents `#7FC8FF`
- Light mode: backgrounds `#F2FAFF` / `#E5F4FF`, text `#030710`, accents `#7FC8FF`
- The accent blue (`#7FC8FF`) stays the same in both modes
- Never use pure black (`#000000`) or pure white (`#FFFFFF`) in either mode

## Features

### Smart Font Application

- Applies Lausanne (or Inter fallback) to headings and long body copy
- Applies Aeonik Mono (or IBM Plex Mono fallback) to H2, code, short body, and CTAs
- Automatically falls back to Inter / IBM Plex Mono if custom fonts unavailable
- Preserves readability across all systems

### Text Styling

- H1 headings: Inter weight 300 (light) — never bold or semi bold
- H2 / subheadings: IBM Plex Mono Regular (400)
- Body text: Inter for long form, IBM Plex Mono for short form
- Dark mode text: `#F2FAFF` for primary text, `#7FC8FF` for accent labels/headings, `rgba(255, 255, 255, 0.6)` for subtitle/tertiary text. Never use palette blues (`#40668D`, `#2F4B68`) as text color on `#030710` — they are illegible.
- Light mode text: `#030710` or `#161F34` on light backgrounds

### Shape and Accent Colors

- Non-text shapes use the primary blue palette and gradients
- Gradients for lines, nodes, and subtle depth effects — never for backgrounds

**Extended palette usage is restricted.** The extended product palette (Plum, Purple, Peach, Green) must ONLY be used for:
- Product screenshots and product demo imagery
- In-product UI application (within the actual LangSmith product)
- Subtle accents when editorializing the brand (e.g., blog post graphics, social media)

Do NOT use extended palette colors for card backgrounds, section fills, buttons, or general brand layouts. Cards and containers should use the primary blue palette only (`#030710`, `#0D1322`, `#161F34` for dark; `#F2FAFF`, `#E5F4FF` for light).

### Web Layout & Hierarchy (reference: langchain.com)

When creating web layouts, landing pages, or HTML artifacts, **always read `references/web-template.md` first** — it contains the complete CSS design system, component classes, typography scale, spacing tokens, and a page skeleton ready to use. This produces publish-ready output matching langchain.com.

**IMPORTANT override for frontend-design skill:** The LangChain brand uses Inter and IBM Plex Mono intentionally. Do NOT follow generic advice to "avoid Inter" or use decorative fonts. The brand aesthetic is refined dark minimalism — no grain, no textures, no maximalist effects. Sophistication comes from precise spacing, weight-300 headings, subtle borders, and restrained use of `#7FC8FF` as the sole accent.

Always reference **https://www.langchain.com/** as the canonical example. When in doubt about layout decisions, hierarchy, spacing, or visual treatment, consult the live website.

**Page structure:**
- Dark mode is the primary website aesthetic — `#030710` backgrounds predominate
- Hero sections: large H1 in Inter weight 300 (light), short subtitle, two CTAs ("Start building" primary + "Get a demo" secondary)
- Hero top padding should be at least 220px to clear the floating nav and provide generous breathing room
- Sections alternate between full-dark (`#030710`) and subtle contrast where needed
- Logo bars / trust badges: horizontally scrolling rows of partner logos on dark backgrounds

**Section spacing:**
- Every section needs generous breathing room — minimum 80px vertical padding between sections, 100px preferred for major section breaks
- Hero → first content section: at least 80px gap
- Between major sections (e.g., feature cards → stats → offline/online): 80–100px padding top and bottom
- Stats section: 100px top and bottom padding for visual weight
- Final CTA: 100px top padding to separate from content above
- Never let sections feel cramped — when in doubt, add more space

**Hero headline text:**
- Be intentional about line breaks in hero headlines — don't let words wrap arbitrarily based on container width
- Manually control line breaks to create balanced, visually pleasing lines (e.g., "Continuously Improve\nAgent Quality" rather than letting "Agent" hang alone or wrapping mid-phrase)
- Each line should feel like a complete semantic unit
- Footer: **every webpage must include a footer.** Standard footer spec:
  - 4 equal columns: Products, Resources, Company, Newsletter
  - Each column topped by a `#161F34` horizontal separator line (2px)
  - Column headings: TWK Lausanne / Inter Weight 300, 24px, `#7FC8FF`, `letter-spacing: -0.03em`, `line-height: 120%`
  - Link text: Aeonik Mono / IBM Plex Mono Regular, 14px, `rgba(255, 255, 255, 0.4)`, `line-height: 16px`, `gap: 4px` between items
  - Newsletter column: heading + email input (`border: 1px solid rgba(255, 255, 255, 0.16)`, `border-radius: 6px`) + Subscribe button (`#E5F4FF` bg, `#030710` text)
  - Bottom bar: status indicator (8px `#7FC8FF` circle + "All systems operational" in `#2F4B68`) left, "Privacy policy" and "Terms of service" in `rgba(127, 200, 255, 0.4)` right

**Card patterns:**
- Feature cards: dark background (`#0D1322` or `#161F34`), with product icon pill, Aeonik Mono / IBM Plex Mono label, Lausanne / Inter heading, body text in `#F2FAFF` or light tints
- Cards do NOT use extended palette colors as backgrounds — keep to the dark/light blue system
- Product screenshots (`.avif` imagery) appear inside cards as the visual, with the extended palette appearing only within those product shots
- Customer story cards: dark background, partner logo, short quote, "Read Use Case" link

**Navigation:**
- Top nav: **floating style** — semi-transparent dark background (`rgba(13, 19, 34, 0.85)`), subtle border (`rgba(255, 255, 255, 0.08)`), rounded corners (`border-radius: 12px`), absolutely positioned at top of page with ~16px margin from edges, `z-index: 100`. Matches langchain.com pattern.
- LangChain full lockup (symbol + wordmark) on the left — always use the official SVG asset
- Nav links in Aeonik Mono / IBM Plex Mono Regular, `rgba(255, 255, 255, 0.6)`
- Product mega-menu: organized into "LangSmith Platform" (services with icon pills: Observability, Evaluation, Deployment, Fleet) and "Open Source Frameworks" (with icon pills, names in lowercase Aeonik Mono / IBM Plex Mono: deepagents, langchain, langgraph)

**CTAs and buttons:**
- Primary CTA (nav): `#E5F4FF` background, `#030710` text, `border-radius: 6px`
- Primary CTA (hero): `#7FC8FF` background, `#030710` text, `border-radius: 8px`
- Secondary CTA: ghost button with `rgba(255, 255, 255, 0.16)` border, `#F2FAFF` text, `border-radius: 6px` (nav) or `8px` (hero)
- CTA text: Aeonik Mono / IBM Plex Mono Regular, Title Case

**Pricing pages:**
- Three-tier layout (Developer / Plus / Enterprise) on dark backgrounds
- Feature comparison tables with checkmark icons
- Tier cards use subtle dark background differentiation, not extended palette colors

**Product imagery:**
- Product screenshots/demos are where the extended palette appears naturally (trace colors, chart colors, UI accents within the product itself)
- Product images sit inside dark card containers or on dark backgrounds
- Glow effects (soft radial gradients of `#7FC8FF` at low opacity) are used behind hero images and key product visuals for depth

**Stats / social proof sections:**
- Large numbers in Inter weight 300 (e.g., "100M+", "6K+")
- Descriptive labels in Aeonik Mono / IBM Plex Mono Regular below
- Arranged in horizontal rows on dark backgrounds

### Social Media & Marketing Asset Templates

**Default canvas dimensions** (use these unless the user specifies otherwise):

| Asset Type | Width | Height |
|---|---|---|
| Social post | 3000px | 3000px |
| LinkedIn post | 3000px | 3000px |
| Blog header | 990px | 742px |
| Conceptual guide header | 1080px | 605px |

**Social media template layout (3000x3000):**

Social posts require a completely different design approach from web layouts. Text must be large, bold, and instantly readable at thumbnail size. Do NOT use web-style centered layouts with small text, feature pills, or detailed information architecture — these are illegible on social.

- **LangChain full lockup** (symbol + wordmark): Always placed at top-left, ~200px height. Use the official SVG from `assets/logos/company/`. This is mandatory on every social post.
- **Headline text**: ~300px height per line (font-size ~260px at line-height 1.0). TWK Lausanne weight 250, `#7FC8FF`, left-aligned. The headline should dominate 40–50% of the frame area. Keep it punchy — 3–5 words per line maximum.
- **Background**: Sweeping arc lines (`#161F34`) with dots as subtle texture on the right side. The graphic language is background decoration, not the focal point.
- **Metadata pill** (bottom area): `rgba(22, 31, 52, 0.7)` background, `border-radius: 14px`, Aeonik Mono 42px, `#7FC8FF` text, left-aligned. Contains URL, date/time/location, or event details.
- **Layout**: Top-heavy hierarchy — lockup at top, headline in upper-middle, large whitespace, metadata at bottom. Left-aligned throughout. Never centered.
- **Padding**: ~160px on all sides at 3000x3000.

**Blog header template (990x742):**
- Centered layout acceptable for blog headers
- TWK Lausanne weight 250 for headline, sized to fit within the frame
- Subtitle in `rgba(255,255,255,0.6)` below headline
- Dot-matrix graphic language or subtle background texture
- LangSmith service lockup or Aeonik Mono label at top

**Conceptual guide header template (1080x605):**
- Similar to blog header but wider aspect ratio
- Headline left-aligned or centered depending on content
- Graphic language elements can be more prominent since guides are technical content

### Graphic Language (Visual Diagrams & Illustrations)

LangChain uses a distinctive graphic language for marketing illustrations, hero graphics, and technical diagrams. These are SVG-based compositions using dots, lines, nodes, and arcs from the brand palette.

**Core principles:**
- Clean, geometric, and sophisticated — every element must be intentional
- All graphic element fills and strokes use **solid hex colors only** — never apply `opacity` to fills or strokes. Use intermediate solid colors derived from the palette instead.

**Solid color intermediates for graphic elements (instead of opacity):**
- Darkest tier: `#2F4B68` (minimum visible on `#030710`)
- Dark-mid tier: `#40668D`
- Mid tier: `#1A5EAA` (between `#006DDD` and dark)
- Light-mid tier: `#5BADDF` (between `#7FC8FF` and `#006DDD`)
- Lightest tier: `#7FC8FF` (primary accent)

**Line and connection rules:**
- No line should have two open ends — every line must terminate at a dot (endpoint) or a node (on-axis circle)
- Lines connecting to nodes must terminate precisely at the node center
- Use solid stroke colors, not opacity-reduced strokes

**Label placement:**
- Text labels must NEVER overlap with lines, nodes, or other graphic elements
- Place labels in a separate row above/below the graphic area, or with sufficient clear space
- Minimum label color on `#030710`: `rgba(255, 255, 255, 0.6)` — never use `#40668D` or `#2F4B68` for text

**Minimum brightness on `#030710` backgrounds:**
- Lines/arcs: `#2F4B68` minimum (`#161F34` is nearly invisible)
- Text labels: `rgba(255, 255, 255, 0.6)` minimum
- Dots/circles: `#2F4B68` minimum, `#40668D` preferred for secondary
- Both hero graphic and lifecycle diagrams must use the same brightness tier for equivalent elements

**Arrow placement on Bézier arcs:**
- Arrow triangles must sit precisely ON the arc line at the mathematical midpoint, not floating detached
- For a quadratic Bézier `Q` curve from P0 to P2 with control point P1, the midpoint at t=0.5 is: `x = (P0.x + 2*P1.x + P2.x) / 4`, `y = (P0.y + 2*P1.y + P2.y) / 4`
- The tangent direction at the midpoint is simply `P2 - P0` (the direction from start to end)
- Arrow triangles should be oriented along this tangent: rightward-pointing for forward flow, leftward-pointing for return flow
- Draw arrows as `<polygon>` elements centered on the calculated midpoint, NOT as SVG `marker-mid` (which may not render in all design tools)
- Example: for arc `Q 220 -10, 330 120` from `(80,120)`, midpoint = `(212.5, 55)`, tangent = rightward → `<polygon points="207,49 218,55 207,61" fill="#5BADDF"/>`

**Lifecycle / flow diagrams:**
- Curved lines use smooth quadratic Bézier curves (`Q` paths in SVG)
- Nodes: concentric circles — outer ring (`#0D1322` fill + colored stroke) + inner fill (`#161F34`) + icon
- **Icon centering within nodes is critical.** All icons inside node circles must be mathematically centered on the circle's center point. For a circle at `(cx, cy)`, the icon's visual bounding box center must equal `(cx, cy)`. When using multiple stroked paths (e.g., double chevrons), calculate the combined visual center of all paths and ensure it equals the circle center. Off-center icons look unpolished.
- Labels placed in separate HTML rows below the SVG, not inside the SVG — this prevents overlap and keeps text crisp

**Dot-matrix / convergence patterns (hero graphics):**
- Dots further from center use darker colors (`#2F4B68`), closer use brighter (`#5BADDF`, `#7FC8FF`)
- Background grid: `#161F34` verticals with `stroke-dasharray: "2 8"`
- Central flow line: gradient stroke from Dark Blue → Blue → Light Blue

**Glow effects:**
- Soft radial gradients of `#7FC8FF` at 7–12% opacity behind hero graphics
- Applied as background fills, never foreground overlays

## Technical Details

### Font Management

- Primary: Lausanne (CSS: 'TWK Lausanne') — **licensed typeface, not bundled with this skill**
- Secondary: Aeonik Mono — **licensed typeface, not bundled with this skill**

**Font priority rule:** When designing in environments where TWK Lausanne and Aeonik Mono are available (e.g., Paper.design, Figma with fonts installed), always use them directly. Only fall back to Inter and IBM Plex Mono when the primary typefaces are confirmed unavailable. Check font availability before defaulting to fallbacks.

- Fallback fonts (for environments without licensed fonts):
  - **Inter** replaces Lausanne (available via Google Fonts: `Inter`)
  - **IBM Plex Mono** replaces Aeonik Mono (available via Google Fonts: `IBM+Plex+Mono`)
- Apply the same typographic hierarchy, weights, tracking, and leading rules to the fallback fonts
- Inter weight mappings: use 250→300 (Light), 400→400 (Regular), 600→600 (Semi Bold)
- IBM Plex Mono weight mappings: use Light→300, Regular→400, Medium→500

### Color Application

- Dark mode: backgrounds `#030710` or `#0D1322`, text/accents `#F2FAFF` / `#7FC8FF`
- Light mode: backgrounds `#F2FAFF` (not white), text `#030710` (not black)
- Gradients via CSS `linear-gradient()`, combining core palette colors
- Extended palette ONLY for product shots, in-product UI, and editorial accents — never for card backgrounds or general layouts
- Never use pure `#000000` or `#FFFFFF` except in black/white fallback

### Logo & Icon Implementation

- LangChain symbol: 4 geometric vector shapes (circular + sharp edges)
- All product icons: rounded rect container (`border-radius: ~20px`) with centered symbol
- LangGraph icon rotated 90°
- LangSmith service lockups: icon pill + LangSmith wordmark + service name (Lausanne 250, 60px)
- OSS lockups: icon pill + product name (Aeonik Mono Regular, lowercase, 60px)
- Company wordmark logos (Academy, Labs, Docs, etc.): vector wordmarks in rounded rect containers (~20.83px radius), no icon pill
- Always provide both dark and light mode variants when creating branded assets

### Paper.design Conceptual Guide Diagram Standards

When creating conceptual guide diagrams, infographics, or technical illustrations in Paper.design, follow these standards for typography, color, and layout. These were developed through iterative design review and take priority over the general typography hierarchy above when working at diagram scale in Paper.design.

**Typography at Diagram Scale:**

- **Diagram titles**: TWK Lausanne weight 300, **48px**, `#F2FAFF`, `letter-spacing: -0.02em`, `line-height: 1.0`. No subtitle or category label above the title — the title stands alone.
- **Card headings / primary labels**: TWK Lausanne weight 400, **18–20px**, accent color (`#7FC8FF` or `#99D3FF`).
- **Body descriptions**: TWK Lausanne weight 300, **16–18px**, `#B2DEFF`.
- **Tags / badges**: TWK Lausanne weight 400, **13px**, `#CCE9FF`, inside `#161F34` pill with `#2F4B68` border.
- **Data values** (durations, token counts, status labels): TWK Lausanne weight 400, **14–16px**, `#B2DEFF` for values, `#E3FF8F` for success status, `#FBB0A5` for error status.
- **Mono text** (Aeonik Mono / IBM Plex Mono): reserved for code-like content only — file names, config structures, thread IDs, column headers. Never use mono for general labels or body descriptions at diagram scale; it is too thin to read on dark backgrounds.
- **Minimum font size**: 13px. Nothing smaller should appear in any diagram.
- **Weight rule**: Prefer TWK Lausanne weight 400 (Regular) over weight 300 (Light) for any text below 20px. Weight 300 is acceptable at 16px+ for body descriptions but never for labels, values, or annotations.

**Color & Accessibility at Diagram Scale:**

- **Never use opacity-reduced text** (e.g., `rgba(255,255,255,0.5)`). Always use solid hex colors from the brand palette.
- Text color minimums on `#030710` backgrounds: `#B2DEFF` for body text, `#CCE9FF` for small labels and tags, `#F2FAFF` for primary headings and names.
- Arrow tips: `#7FC8FF` solid fill. Arrow lines: `#40668D` or `#2F4B68` stroke.
- Extended palette colors for category color-coding: `#7FC8FF` (primary blue), `#5BADDF` (light-mid blue), `#6E8900`/`#E3FF8F` (green), `#C78EAD` (plum), `#FBB0A5` (peach for errors).

**Layout & Framing:**

- **Tight framing**: Artboard height must hug the content — no excess empty space at the bottom of cards or the artboard. Measure content height and set the artboard height accordingly.
- **Standard artboard width**: 1080px for most diagrams. Use narrower widths (e.g., 660px) when content is naturally compact (file structures, single-column layouts).
- **Artboard padding**: 48px top/bottom, 56px left/right.
- **Card heights**: Sized to content, not stretched to fill available space. If content occupies 350px, the card should be ~350px, not 520px.
- **Gap between artboard elements**: 12px default gap in the artboard's flex column.

**Diagram Pattern: Mapping (e.g., Primitives → Infrastructure):**

- Left column: primitive cards with centered SVG icon + TWK Lausanne 400 15px `#F2FAFF` label, bordered with `#2F4B68`, `border-radius: 10px`.
- Arrow connectors: `#2F4B68` line + `#7FC8FF` polygon arrowhead, centered in an 80px-wide zone.
- Right column: infra cards with `#0D1322` fill, `#2F4B68` border, `border-radius: 10px`, 24px horizontal padding. Title in TWK Lausanne 400 18px `#7FC8FF`, description in TWK Lausanne 300 18px `#B2DEFF`.

**Diagram Pattern: Three-Column Tiers (e.g., Memory Layers):**

- Three equal-width cards (280px) with `#0D1322` fill, colored borders indicating hierarchy (`#7FC8FF` → `#5BADDF` → `#40668D`).
- Each card: SVG icon (40×40), heading (TWK Lausanne 400, 20px, accent color), description (TWK Lausanne 300, 16px, `#B2DEFF`, centered), and scope tags at bottom.
- Bidirectional arrows between columns in 64px-wide zones with labeled flow directions (offload/recall, persist/load).

**Diagram Pattern: Architecture / Harness (e.g., Harness ↔ Model Provider API):**

- Solid `#7FC8FF` border for owned/open components (Harness). Dashed `#2F4B68` border for external/closed components (Model Provider API).
- Sub-components as pill-shaped elements (`border-radius: 100px`) inside the container, with colored borders and TWK Lausanne 400 18px `#F2FAFF` labels.
- Section labels (e.g., "HARNESS", "MODEL PROVIDER API"): TWK Lausanne 400, 14px, `#99D3FF`, uppercase, `letter-spacing: 0.06em`.
- Dashed bidirectional arrows between containers: `#40668D` stroke with `stroke-dasharray: 6 4`, `#7FC8FF` polygon arrowheads.

**Diagram Pattern: Nested Timeline / Trace (e.g., Anatomy of an Agent Trace):**

- Outer container: `#0D1322` fill, `#2F4B68` border, `border-radius: 10px`.
- Top-level run header: TWK Lausanne 600 18px `#F2FAFF` for the run name, with duration/tokens/status metadata in TWK Lausanne 400 16px `#B2DEFF`. Status dot: 8px circle with `#6E8900` for success.
- Color-coded timeline bar: segmented horizontal bar (6px height, `border-radius: 100px`) with colors representing each phase.
- Span rows: `#161F34` fill, `border-radius: 6px`, with a 4px-wide colored left-edge bar. Span name in TWK Lausanne 400 16px `#F2FAFF`, metadata in 15px `#B2DEFF`.
- Nested tool calls: `#0D1322` fill, indented 22px from parent, with 3px left-edge bar. Tool names in 14px `#CCE9FF`.
- Error states: `#634643` border on the tool row, `#FBB0A5` for the left bar, status dot, and "error" label. Error message in TWK Lausanne 300 13px `#B27D75`.
- Annotations: icon (16×16 SVG circle with relevant symbol) + TWK Lausanne 400 13px in the annotation color (`#5BADDF` for info, `#FBB0A5` for errors, `#7FC8FF` for approvals).

**Diagram Pattern: Config / File Structure (e.g., deepagents.toml):**

- Outer container: `#0D1322` fill, `#2F4B68` border, `border-radius: 12px`. Width sized to content (e.g., 560px), not full artboard width.
- File/folder names in Aeonik Mono weight 500, 17px, color-coded by type from the extended palette: `#7FC8FF` for primary config, `#5BADDF` for markdown, `#6E8900`/`#E3FF8F` for directories, `#C78EAD` for JSON/data files.
- Nested items (fields, sub-directories) in Aeonik Mono weight 400, 15px, one tint lighter than the parent color (e.g., `#B2DEFF` for fields under a `#7FC8FF` file).
- Parenthetical hints (e.g., "OpenAI, Gemini, Claude, etc") in `#99D3FF`.
- Highlighted blocks (e.g., the primary config file): `#161F34` fill, `#7FC8FF` border, `border-radius: 8px`, nested inside the outer container.
```
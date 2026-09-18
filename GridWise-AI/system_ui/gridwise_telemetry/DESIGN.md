---
name: GridWise Telemetry
colors:
  surface: '#111318'
  surface-dim: '#111318'
  surface-bright: '#37393f'
  surface-container-lowest: '#0c0e13'
  surface-container-low: '#1a1b21'
  surface-container: '#1e1f25'
  surface-container-high: '#282a2f'
  surface-container-highest: '#33353a'
  on-surface: '#e2e2e9'
  on-surface-variant: '#d2c5b0'
  inverse-surface: '#e2e2e9'
  inverse-on-surface: '#2e3036'
  outline: '#9b8f7c'
  outline-variant: '#4e4636'
  surface-tint: '#f0c04e'
  primary: '#ffe4af'
  on-primary: '#3f2e00'
  primary-container: '#f5c452'
  on-primary-container: '#6d5100'
  inverse-primary: '#785a00'
  secondary: '#adc6ff'
  on-secondary: '#002e6a'
  secondary-container: '#0566d9'
  on-secondary-container: '#e6ecff'
  tertiary: '#77ffc4'
  on-tertiary: '#003825'
  tertiary-container: '#4ae3a8'
  on-tertiary-container: '#006243'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdf9d'
  primary-fixed-dim: '#f0c04e'
  on-primary-fixed: '#251a00'
  on-primary-fixed-variant: '#5b4300'
  secondary-fixed: '#d8e2ff'
  secondary-fixed-dim: '#adc6ff'
  on-secondary-fixed: '#001a42'
  on-secondary-fixed-variant: '#004395'
  tertiary-fixed: '#68fcbf'
  tertiary-fixed-dim: '#45dfa4'
  on-tertiary-fixed: '#002114'
  on-tertiary-fixed-variant: '#005137'
  background: '#111318'
  on-background: '#e2e2e9'
  surface-variant: '#33353a'
typography:
  headline-xl:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 30px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0em
  body-lg:
    fontFamily: Space Mono
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0em
  body-md:
    fontFamily: Space Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0em
  body-sm:
    fontFamily: Space Mono
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-md:
    fontFamily: Space Mono
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Space Mono
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.08em
  telemetry-num-lg:
    fontFamily: Space Mono
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.03em
  telemetry-num-md:
    fontFamily: Space Mono
    fontSize: 16px
    fontWeight: '700'
    lineHeight: 20px
    letterSpacing: 0em
spacing:
  gutter: 0.5rem
  gutter-mobile: 0.5rem
  margin: 1rem
  margin-mobile: 0.75rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

## Brand & Style

This design system delivers an industrial, high-density SCADA-inspired interface engineered for campus microgrid monitoring and algorithmic load dispatch. Tailored for energy systems engineers, microgrid operators, and infrastructure directors, the interface translates high-velocity telemetry into decisive operational control. 

The aesthetic is experimental brutalist SCADA: stark, high-contrast, angular, and functional. It abandons ornamental softening in favor of raw structural discipline, hard boundaries, and visual efficiency. The environment evokes the focused precision of an advanced industrial operations terminal, where high-contrast solar anchors pierce through deep obsidian depths to indicate system states, critical battery thresholds, and grid anomalies instantaneously.

## Colors

The palette is engineered around high-contrast telemetry visualization on deep planar backdrops. 

- **Primary (`#F5C452` / Solar Yellow):** Serves as the primary system anchor, key visual priority marker, interactive cursor indicator, and active solar PV generation signal.
- **Secondary (`#3B82F6` / Electric Blue):** Utilized for active control paths, command execution states, grid power import vectors, and utility-level operations.
- **Tertiary (`#34D399` / Telemetry Teal):** Designated for storage dynamics (State of Charge / SOC), optimization convergence confirmation, and positive nominal system health.
- **Neutral Palette:**
  - Canvas Base: `#0B0D12` (Void Black)
  - Surface Panel / Cards: `#161A22` (Dark Slate)
  - Structural Delimiters / Borders: `#242938` (Low-contrast frame)
  - Contrast Borders: `#384056` (High-definition divider)
  - Telemetry Text Primary: `#E5E7EB` (Off-white readout)
  - Telemetry Text Secondary: `#8B93A6` (Muted engineering grey)
- **Functional Semantics:**
  - Alert / Amber: `#F59E0B` (Curtailment warning, thermal stress, peak pricing window)
  - Critical / Red: `#EF4444` (Infeasible optimization state, system fault, load drop)

Always apply semantic accents at full saturation against `#161A22` or `#0B0D12` backdrops; avoid tinted glowing fills in favor of precise bounding line indicators and high-contrast text tags.

## Typography

The typographic hierarchy implements an uncompromising technical protocol: `Space Grotesk` dictates macro-level hierarchy and panel titles, imparting structural engineering modernity, while `Space Mono` governs all data telemetry, tabular readouts, metric units (kW, kWh, MWh, Hz, V), temporal scales (00:00–23:00), and parameter configurations.

- All numeric telemetry values must be presented via `Space Mono` to guarantee tabular column alignment and optical scanning speed.
- Labels (`label-md`, `label-sm`) default to uppercase transformations with generous character tracking (`0.05em` to `0.08em`) to mimic physical industrial labeling and control panel legends.
- Maintain strict baseline lockups across dual-column data metrics; labels always anchor above raw values or pair directly with a colon separator (e.g., `SOC: 84.2%`).

## Layout & Spacing

The layout model is driven by a rigid 8px baseline matrix optimized for ultra-dense data dashboards. The screen space utilizes a fluid multi-column grid (16 columns on ultra-wide monitoring displays, 12 columns on desktop, 4 columns on mobile) with compressed gutters (`0.5rem`) to maximize screen real estate for complex charts and concurrent metrics.

- **Desktop (>= 1280px):** 12-to-16 column continuous matrix, dense multi-widget instrumentation, persistent command ribbon, zero extraneous outer margins (`1rem`).
- **Tablet (768px - 1279px):** 8-column layout, metrics collapse into horizontal scrolling data strips, charts retain strict 16:9 or 21:9 telemetry ratios.
- **Mobile (< 768px):** Single-column stacked telemetry stack with pinned key performance index (KPI) ticker. Padding steps down to `space-xs` and `space-sm` inside cards to eliminate dead space.
- Structural elements snap directly to the 8px interval. Component paddings rely strictly on `space-xs` (4px), `space-sm` (8px), `space-md` (12px), and `space-lg` (16px).

## Elevation & Depth

This design system completely rejects blurred dropshadows and skeletal illusions. Elevation is structural, mechanical, and binary. 

Visual layering is achieved through **Bold Borders** and **Tonal Stratification**:
- **Layer 0 (Canvas):** Pure base `#0B0D12`. Serves as the substrate for uncontained telemetry and grid rules.
- **Layer 1 (Instrumentation Panels & Cards):** `#161A22` bounded by a crisp 1px `#242938` outer border. Panels sit directly adjacent or separated by minimal gutters.
- **Layer 2 (Active Focus & Terminal Insets):** `#0E1117` insets with `#384056` borders for terminal logs, telemetry tables, and interactive configuration drawers.
- **Layer 3 (Overlays, Flyouts & Modals):** `#161A22` bounded by a high-contrast 1px solid `#F5C452` or `#384056` perimeter with zero drop-shadow blur. A 1px hard offset shadow (`2px 2px 0px #000000`) may be applied strictly to active modal dialogue frames to mimic physical terminal overlays.

## Shapes

In alignment with brutalist industrial telemetry hardware, all interface geometry enforces absolute angularity: `roundedness: 0` (0px border radius across every element).

- Cards, badges, buttons, tooltips, dialogs, inputs, and chart markers are rendered with hard, right-angle vertices.
- Cut-corner accents (45-degree chamfers, 4px by 4px) are permitted exclusively on primary KPI module headers and system status chips to reinforce the industrial microgrid console metaphor.
- Internal dividing lines use 1px solid dividers with zero feathering or ambient gradients.

## Components

### Buttons & Trigger Controls
- **Primary Action (Dispatch / Execute):** Solid `#F5C452` background with `#0B0D12` bold text (`Space Mono`, uppercase). Square edges, no shadow. Active state shifts background to `#F59E0B`. Focus ring is a 1px offset solid white line.
- **Secondary Action (Grid Import / Mode Toggle):** Transparent background, 1px solid `#3B82F6` border, `#3B82F6` text. Hover fills background with `rgba(59, 130, 246, 0.12)`.
- **Tertiary / Utility (Acknowledge Alert):** Transparent background, 1px solid `#242938`, `#E5E7EB` text. Hover shifts border to `#8B93A6`.

### Telemetry Cards & Instrumentation Panels
- Solid `#161A22` planar surface, sharp 1px `#242938` border.
- Header block features a mandatory 28px height strip with a 1px solid bottom border (`#242938`), holding an uppercase panel label (`label-sm`, `#8B93A6`) and an optional real-time sync indicator dot (3px square).

### Status Indicators & Badges
- Strictly rectangular chips (0px radius).
- **Nominal / Optimal:** 1px border `#34D399`, background `rgba(52, 211, 153, 0.08)`, text `#34D399`.
- **Solar Generating:** 1px border `#F5C452`, background `rgba(245, 196, 82, 0.08)`, text `#F5C452`.
- **Infeasible / Alarm:** 1px border `#EF4444`, background `rgba(239, 68, 68, 0.15)`, text `#EF4444`.

### Input Fields & Parameter Adjusters
- Background `#0B0D12`, 1px solid `#242938` border. Sharp 0px corners.
- Font: `Space Mono`, text color `#E5E7EB`.
- Active focus state: 1px solid `#F5C452`. No outer glow or halo.
- Numeric inputs must include hard unit attachments (e.g., `[ kW ]`, `[ $/MWh ]`) fixed to the right edge with a vertical 1px divider.

### Data Tables & Telemetry Matrix
- Dense rows (32px row height), alternating row backgrounds (`#161A22` and `#11141B`).
- Column dividers: 1px `#242938`.
- Header row: `#0B0D12` background, uppercase `label-sm` text, pinned during vertical scrolling.

### Specialized Energy Visualizations
- **Dispatch Heatmap / 24hr Schedule:** Monolithic 24-column block cells (hours 0–23). Zero radius. Active load shifts from deep navy (`#161A22`) to solar gold (`#F5C452`) or storage teal (`#34D399`).
- **Telemetry Sparklines:** 1.5px hard path lines with zero area gradient fill, sharp square vertices at data sample points.
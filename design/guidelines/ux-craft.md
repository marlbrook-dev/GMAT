# Craft rules — Meridian Prep

Adapted for this system from tommyjepsen/awesome-ux-skills (craft): https://github.com/tommyjepsen/awesome-ux-skills

1. Flat, deliberate color — no gradients (the gold band and navy blocks do the lifting), no glow shadows.
2. Transitions name their properties (background, transform, box-shadow) at 120–200ms --ease-out; never \`transition: all\`. Motion animates transform/opacity, respects prefers-reduced-motion (wired in tokens/base.css).
3. Break monotony deliberately: one big element per view (hero headline, mono score), section rhythm alternates white / gray-50 / navy.
4. Real copy only — no lorem ipsum, no "John Doe"; microcopy is part of the design (see readme Content fundamentals).
5. Stacking contexts: use the z tokens only (--z-sticky 20, --z-dropdown 40, --z-modal 100, --z-toast 110). Components that layer internally get isolation:isolate. No z-index arms races.
6. No pure #000; text is navy-900/gray-700 on gray-50 pages. White is reserved for card surfaces on tinted grounds.
7. Spacing from --space-* only; gaps within a group < gaps between groups.
8. Hierarchy from weight and color before size; body max measure ~70ch; scores/timers use tabular numerals (.numeric or [data-numeric]).
9. Elevation language: hairline borders for structure, soft low-alpha shadows only for things that float (menus, dialogs, toasts). Never border + heavy shadow + tint on one card.
10. Every interactive element: hover, focus-visible, active, disabled. Every async surface: loading (static skeleton), empty (what + one action), error (plain words + way forward) — see guidelines/states.html.
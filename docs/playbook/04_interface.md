# The Interface: One System, Defined Once

## The type and spacing system

One file holds the whole visual system and is injected into every page. Currently
{{TOKEN_COUNT}} tokens covering:

- A type scale, `--t-100` to `--t-900`
- A tracking ramp, `--tr-900` to `--tr-caps`
- A four-pixel spacing grid, `--s1` to `--s10`
- One page width, one gutter, one reading measure
- The full colour palette, in both themes

**Reach for a token before a number.** A raw pixel value in a template is how this site
reached thirty-seven font sizes, twenty-eight spacing values and eight page widths.

Two type rules worth stealing outright:

**Type tightens as it grows and never opens up.** Negative tracking on headings, scaling
from about -0.032em at hero size to 0 at body size. The single positive value is +0.06em,
reserved for small uppercase labels.

**Three faces, no more.** A serif for headings, one sans for everything else, and a mono
for figures that sit in a column, never for words. This site once ran a fourth face as a
second sans, and the two were close enough that the result read as a mistake rather than
as a choice. Sites that do this well are lopsided on purpose: Stripe runs roughly a
hundred declarations of its sans to two of mono.

## The layout traps

Three CSS behaviours caused more wasted hours on this project than anything else. They are
not obscure. They are just silent.

**Grid and flex children need `min-width: 0`.** Without it a child holds its min-content
width and pushes the page sideways on a phone. This broke pricing, the rankings controls
and the blog submit form, separately, each time looking like a different bug.

**CSS comments do not nest.** The first `*/` closes the outer comment. A template
placeholder left inside an opening comment killed the colour palette on over a thousand
pages and was chased as a design problem for hours.

**An undefined custom property is silent.** CSS does not treat `var(--nope)` as an error;
it falls back and paints. A page here referenced nine colour tokens that existed nowhere,
and the legally required Do Not Sell button rendered as white text on a transparent
background on a white page, invisible from the day it shipped. **Audit computed colour on
the rendered page, not authored colour in the source.**

And one more, for completeness: `overflow: hidden` makes an element the scroll container
that `position: sticky` resolves against. A sticky header that will not stick almost
always means an ancestor picked up an `overflow`.

## Dark mode, and the way it actually breaks

A dark mode does not break by having a wrong colour. It breaks by **missing** one. A token
defined only inside a media query falls back to whatever it inherits, and the result is
usually legible enough to pass a glance and wrong enough to matter.

The structure that avoids it:

1. Define the **complete** palette on bare `:root`. Every token, no exceptions.
2. Redefine **only** those tokens under `@media (prefers-color-scheme: dark)`, guarded as
   `:root:not([data-theme="light"])`.
3. Redefine them again under `:root[data-theme="dark"]`, so an explicit choice wins in
   both directions.

Three states, not two: light, dark, and follow the system. A two-state toggle cannot
express "follow the system", and that is the most common way a dark mode is got wrong.

Then test it by parity: read both `:root` blocks and assert every colour token defined in
one is defined in the other. Select by whether the **value** is a colour, not by whether
the **name** starts with a colour-ish prefix. Classifying by name caught a font size on
this project.

Finally, resolve the theme before first paint, in a tiny inline script in the head. A
theme applied after paint is a flash of the wrong one.

## Colour in data display

This is the part most teams get wrong, and it is measurable rather than a matter of taste.

**Brand colours are usually wrong inside a chart.** This site's navy, teal and secondary
navy all sit below the chroma floor and read as grey in a plot; its blue against its
violet is a deuteranopia delta-E of 0.4, which means two series a colourblind reader
cannot distinguish at all. Brand colour belongs on the page around the chart. Inside the
plot, the job is telling series apart.

**Validate the palette under simulated colour vision deficiency, across every pair, not
just neighbours.** The categorical set here passes protanopia, deuteranopia and
tritanopia on all pairs in light mode.

**A dark palette has about half the lightness range to work with.** Roughly 0.48 to 0.67,
against 0.43 to 0.77 for light, so hue has to carry more of the separation, and hue is
exactly what collapses under deuteranopia. Measured, this palette tops out at three slots
distinguishable by colour alone on dark. That is only workable with secondary encoding, so
secondary encoding is not optional: every chart with two or more series ships a legend,
small sets are direct labelled, and every chart has a table view.

**Status colours are reserved and never used for a series.** A chart with four series and
a red one implies the red one is bad.

**Never encode identity by colour alone.** Two games on this site signalled right and
wrong only by colour until an accessibility pass; outcomes now carry a word as well, which
also survives greyscale printing and forced-colors mode.

## Chart form is a claim

The form you choose asserts something about the data.

**A line claims the values in between existed.** Money movement on this site was charted
as a line, and the line between $13.32 on one day and $4.99 on the next passed through
every value in between, none of which happened. Discrete events are bars.

**A funnel drawn as a tapering polygon encodes the number twice**, once in width and once
in area, and area is the one people misread. A ranked list of bars with the drop-off
written between them says the same thing without the illusion.

**Every chart should be able to become its own numbers.** A table view under each chart is
the accessibility backstop, and it is also what a person actually wants when they are
trying to copy a figure out.

## Accessibility, as a set of habits

- Announce outcomes in a live region, not just in colour or motion.
- A flipped card, a revealed tile, a state change: say what it is.
- Contrast is measured on the rendered page, in both themes, on every page. A near miss
  is a fail; the grey carrying most of the secondary text here measured 4.83:1 on white
  and 4.41:1 on the tinted cards, and only the second one is obviously wrong.
- No horizontal scroll at 390 pixels. Assert it in a test rather than checking it by eye,
  and measure the component, not the document, or a wide child can hide behind a narrower
  page.

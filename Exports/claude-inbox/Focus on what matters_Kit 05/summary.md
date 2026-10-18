# Design report: Focus on what matters_Kit 05

Sent: 2026-10-18T11:05:12.799Z

**Will import, with differences** (score 84): 0 to fix, 2 differences, 5 tips.
65 layers, 22 frames, 5 with auto layout, 1 text, 0 images.

## Will look different

- **Flipped (mirrored) layers** x17: Mirrored layers import un-mirrored.
  - Fix: In Figma, flatten the flip (Object → Flatten / Outline stroke) or redraw it mirrored; for icons, export a mirrored copy.
  - Layers: Frame 1948755364 (3405:380), Ellipse 2338 (3405:381), Group (3405:382), Vector (3405:383), Vector (3405:384), Vector (3405:385), Vector (3405:386), Vector (3405:387), Vector (3405:388), Vector (3405:389), and 7 more
- **Background blur (frosted glass)** x5: Background blur is not supported in Rive.
  - Fix: Fake it with a semi-transparent fill, or add a blurred copy of the background image.
  - Layers: Frame 1948755370 (3405:363), Frame 1948755367 (3405:365), Frame 1948755371 (3405:367), Frame 1948755369 (3405:369), Frame 1948755364 (3405:380)

## Tips

- **Shadows with spread** x14: Shadow spread is ignored; the shadow imports at the layer's own size.
  - Fix: Set spread to 0 and adjust blur and offset, or use a larger shape under the layer.
  - Layers: Ellipse 550 (3405:362), Frame 1948755370 (3405:363), Frame 1948755370 (3405:363), Frame 1948755367 (3405:365), Frame 1948755367 (3405:365), Frame 1948755371 (3405:367), Frame 1948755371 (3405:367), Frame 1948755369 (3405:369), Frame 1948755369 (3405:369), Ellipse 552 (3405:373), and 4 more
- **Component instances are detached** x5: Instances import as ordinary layout; they stay linked to nothing, so editing the component later will not update them in Rive.
  - Fix: The main component is also added as a Rive component artboard you can reuse.
  - Layers: AI (3405:355), energy (3405:364), target-02 (3405:366), user (3405:368), chart-up (3405:370)
- **Inside/outside strokes with a shadow** x4: These cannot be combined (the clip would cut the shadow), so the stroke is drawn centred.
  - Fix: Use a centre stroke, or put the shadow on a separate rectangle underneath.
  - Layers: Ellipse 550 (3405:362), Ellipse 552 (3405:373), Ellipse 549 (3405:376), Ellipse 551 (3405:379)
- **1 font file to supply**: Rive does not read fonts from Figma, so each font and weight needs a .ttf file: Geist-SemiBold.ttf.
  - Fix: Put the files in the helper's Fonts Library folder (or the project's fonts folder) using exactly these names. Without them a stand-in font is used.
- **Treated as an illustration**: This design is mostly shapes with little text and no real layout, so layout and naming tips are left out of the score.
  - Fix: Nothing to do. Keep layers grouped by part (for example one group per icon) if you plan to animate them.

## Fonts needed

- Geist SemiBold -> Geist-SemiBold.ttf

## Files

- `report.json`: this report as data
- `snapshot.json`: the full design data (large; open only for specific layers)
- `preview-1-Focus-on-what-matters_Kit-05.png`: preview image

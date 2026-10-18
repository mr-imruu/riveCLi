# Design report: Deliver with accountability_Kit 06

Sent: 2026-10-18T10:18:32.192Z

**Will import, with differences** (score 84): 0 to fix, 2 differences, 5 tips.
74 layers, 34 frames, 20 with auto layout, 1 text, 0 images.

## Will look different

- **Background blur (frosted glass)** x5: Background blur is not supported in Rive.
  - Fix: Fake it with a semi-transparent fill, or add a blurred copy of the background image.
  - Layers: Frame 2147230246 (3405:433), Frame 2147230241 (3405:435), Frame 2147230243 (3405:439), Window (3405:444), Frame 2147230678 (3405:456)
- **Flipped (mirrored) layers**: Mirrored layers import un-mirrored.
  - Fix: In Figma, flatten the flip (Object → Flatten / Outline stroke) or redraw it mirrored; for icons, export a mirrored copy.
  - Layers: Line 30 (3405:442)

## Tips

- **Shadows with spread** x12: Shadow spread is ignored; the shadow imports at the layer's own size.
  - Fix: Set spread to 0 and adjust blur and offset, or use a larger shape under the layer.
  - Layers: Frame 2147230246 (3405:433), Frame 2147230246 (3405:433), Frame 2147230241 (3405:435), Frame 2147230241 (3405:435), Frame 2147230243 (3405:439), Frame 2147230243 (3405:439), Window (3405:444), Frame 2088239621 (3405:458), Frame 2088239621 (3405:465), Frame 2088239621 (3405:472), and 2 more
- **Component instances are detached** x3: Instances import as ordinary layout; they stay linked to nothing, so editing the component later will not update them in Rive.
  - Fix: The main component is also added as a Rive component artboard you can reuse.
  - Layers: user (3405:434), user (3405:436), user (3405:440)
- **Inside/outside strokes with a shadow**: These cannot be combined (the clip would cut the shadow), so the stroke is drawn centred.
  - Fix: Use a centre stroke, or put the shadow on a separate rectangle underneath.
  - Layers: Dot (3405:488)
- **1 font file to supply**: Rive does not read fonts from Figma, so each font and weight needs a .ttf file: Geist-SemiBold.ttf.
  - Fix: Put the files in the helper's Fonts Library folder (or the project's fonts folder) using exactly these names. Without them a stand-in font is used.
- **Treated as an illustration**: This design is mostly shapes with little text and no real layout, so layout and naming tips are left out of the score.
  - Fix: Nothing to do. Keep layers grouped by part (for example one group per icon) if you plan to animate them.

## Fonts needed

- Geist SemiBold -> Geist-SemiBold.ttf

## Files

- `report.json`: this report as data
- `snapshot.json`: the full design data (large; open only for specific layers)
- `preview-1-Deliver-with-accountability_Ki.png`: preview image

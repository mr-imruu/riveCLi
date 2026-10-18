# Design report: Move faster think deeper_Kit 03

Sent: 2026-10-18T11:05:05.316Z

**Will import, with differences** (score 84): 0 to fix, 2 differences, 5 tips.
119 layers, 46 frames, 28 with auto layout, 3 text, 0 images.

## Will look different

- **Background blur (frosted glass)** x7: Background blur is not supported in Rive.
  - Fix: Fake it with a semi-transparent fill, or add a blurred copy of the background image.
  - Layers: Window (3405:196), Body (3405:201), Badge (3405:233), Badge (3405:237), Badge (3405:244), Badge (3405:249), Badge (3405:253)
- **Flipped (mirrored) layers** x2: Mirrored layers import un-mirrored.
  - Fix: In Figma, flatten the flip (Object → Flatten / Outline stroke) or redraw it mirrored; for icons, export a mirrored copy.
  - Layers: Vector 9320 (3405:259), Vector 9319 (3405:261)

## Tips

- **Shadows with spread** x22: Shadow spread is ignored; the shadow imports at the layer's own size.
  - Fix: Set spread to 0 and adjust blur and offset, or use a larger shape under the layer.
  - Layers: Tag (3405:149), Icon dot (3405:154), Icon dot (3405:163), Icon dot (3405:168), Icon dot (3405:177), Icon dot (3405:182), Icon dot (3405:191), Dot (3405:195), Window (3405:196), Icon dot (3405:207), and 12 more
- **Inside/outside strokes with a shadow** x2: These cannot be combined (the clip would cut the shadow), so the stroke is drawn centred.
  - Fix: Use a centre stroke, or put the shadow on a separate rectangle underneath.
  - Layers: Dot (3405:195), Dot (3405:252)
- **Component instances are detached**: Instances import as ordinary layout; they stay linked to nothing, so editing the component later will not update them in Rive.
  - Fix: The main component is also added as a Rive component artboard you can reuse.
  - Layers: AI (3405:344)
- **2 font files to supply**: Rive does not read fonts from Figma, so each font and weight needs a .ttf file: Geist-SemiBold.ttf, Geist-Medium.ttf.
  - Fix: Put the files in the helper's Fonts Library folder (or the project's fonts folder) using exactly these names. Without them a stand-in font is used.
- **Treated as an illustration**: This design is mostly shapes with little text and no real layout, so layout and naming tips are left out of the score.
  - Fix: Nothing to do. Keep layers grouped by part (for example one group per icon) if you plan to animate them.

## Fonts needed

- Geist SemiBold -> Geist-SemiBold.ttf
- Geist Medium -> Geist-Medium.ttf

## Files

- `report.json`: this report as data
- `snapshot.json`: the full design data (large; open only for specific layers)
- `preview-1-Move-faster-think-deeper_Kit-0.png`: preview image

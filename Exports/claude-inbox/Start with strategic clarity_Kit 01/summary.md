# Design report: Start with strategic clarity_Kit 01

Sent: 2026-10-18T10:35:10.863Z

**Will import, with differences** (score 84): 0 to fix, 2 differences, 5 tips.
62 layers, 28 frames, 14 with auto layout, 2 text, 0 images.

## Will look different

- **Background blur (frosted glass)** x6: Background blur is not supported in Rive.
  - Fix: Fake it with a semi-transparent fill, or add a blurred copy of the background image.
  - Layers: Window (3398:13544), Check (3398:13563), Badge (3398:13571), Limitation (3398:13575), Badge 3 (3398:13580), Badge 4 (3398:13584)
- **Blend modes with no Rive equivalent**: The LINEAR_BURN blend mode does not exist in Rive, so the layer blends normally.
  - Fix: Flatten the effect into the colours, or pick the closest mode (for example Multiply or Screen) in Figma.
  - Layers: Ellipse 5 (3398:13562)

## Tips

- **Shadows with spread** x11: Shadow spread is ignored; the shadow imports at the layer's own size.
  - Fix: Set spread to 0 and adjust blur and offset, or use a larger shape under the layer.
  - Layers: Window (3398:13544), Check (3398:13563), Tag (3398:13567), Badge (3398:13571), Badge (3398:13571), Limitation (3398:13575), Limitation (3398:13575), Badge 3 (3398:13580), Badge 3 (3398:13580), Badge 4 (3398:13584), and 1 more
- **Component instances are detached**: Instances import as ordinary layout; they stay linked to nothing, so editing the component later will not update them in Rive.
  - Fix: The main component is also added as a Rive component artboard you can reuse.
  - Layers: AI (3398:13540)
- **Inside/outside strokes with a shadow**: These cannot be combined (the clip would cut the shadow), so the stroke is drawn centred.
  - Fix: Use a centre stroke, or put the shadow on a separate rectangle underneath.
  - Layers: Dot (3398:13543)
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
- `preview-1-Start-with-strategic-clarity_K.png`: preview image

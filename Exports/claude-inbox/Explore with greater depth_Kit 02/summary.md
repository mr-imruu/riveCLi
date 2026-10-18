# Design report: Explore with greater depth_Kit 02

Sent: 2026-10-18T11:05:01.421Z

**Will import, with differences** (score 84): 0 to fix, 2 differences, 4 tips.
61 layers, 28 frames, 16 with auto layout, 1 text, 0 images.

## Will look different

- **Background blur (frosted glass)** x5: Background blur is not supported in Rive.
  - Fix: Fake it with a semi-transparent fill, or add a blurred copy of the background image.
  - Layers: Frame 2147230678 (3401:79), Frame 2147230683 (3401:88), Frame 2147230684 (3401:97), Frame 2147230685 (3401:106), Frame 2147230686 (3401:115)
- **Flipped (mirrored) layers** x2: Mirrored layers import un-mirrored.
  - Fix: In Figma, flatten the flip (Object → Flatten / Outline stroke) or redraw it mirrored; for icons, export a mirrored copy.
  - Layers: Vector 9323 (3401:129), Vector 9324 (3401:130)

## Tips

- **Shadows with spread** x15: Shadow spread is ignored; the shadow imports at the layer's own size.
  - Fix: Set spread to 0 and adjust blur and offset, or use a larger shape under the layer.
  - Layers: Frame 2147230678 (3401:79), Frame 2147230678 (3401:79), Frame 2088239621 (3401:82), Frame 2147230683 (3401:88), Frame 2147230683 (3401:88), Frame 2088239621 (3401:91), Frame 2147230684 (3401:97), Frame 2147230684 (3401:97), Frame 2088239621 (3401:100), Frame 2147230685 (3401:106), and 5 more
- **Component instances are detached**: Instances import as ordinary layout; they stay linked to nothing, so editing the component later will not update them in Rive.
  - Fix: The main component is also added as a Rive component artboard you can reuse.
  - Layers: AI (3401:133)
- **1 font file to supply**: Rive does not read fonts from Figma, so each font and weight needs a .ttf file: Geist-SemiBold.ttf.
  - Fix: Put the files in the helper's Fonts Library folder (or the project's fonts folder) using exactly these names. Without them a stand-in font is used.
- **Treated as an illustration**: This design is mostly shapes with little text and no real layout, so layout and naming tips are left out of the score.
  - Fix: Nothing to do. Keep layers grouped by part (for example one group per icon) if you plan to animate them.

## Fonts needed

- Geist SemiBold -> Geist-SemiBold.ttf

## Files

- `report.json`: this report as data
- `snapshot.json`: the full design data (large; open only for specific layers)
- `preview-1-Explore-with-greater-depth_Kit.png`: preview image

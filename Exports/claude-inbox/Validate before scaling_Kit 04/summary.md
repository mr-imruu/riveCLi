# Design report: Validate before scaling_Kit 04

Sent: 2026-10-18T11:05:09.969Z

**Will import, with differences** (score 84): 0 to fix, 2 differences, 4 tips.
82 layers, 39 frames, 22 with auto layout, 5 text, 0 images.

## Will look different

- **Background blur (frosted glass)** x5: Background blur is not supported in Rive.
  - Fix: Fake it with a semi-transparent fill, or add a blurred copy of the background image.
  - Layers: Frame 2147230245 (3405:276), Frame 2147230246 (3405:278), Window (3405:283), Frame 2147230241 (3405:310), Frame 2147230243 (3405:312)
- **Flipped (mirrored) layers**: Mirrored layers import un-mirrored.
  - Fix: In Figma, flatten the flip (Object → Flatten / Outline stroke) or redraw it mirrored; for icons, export a mirrored copy.
  - Layers: fluent:cursor-16-filled (3405:332)

## Tips

- **Shadows with spread** x14: Shadow spread is ignored; the shadow imports at the layer's own size.
  - Fix: Set spread to 0 and adjust blur and offset, or use a larger shape under the layer.
  - Layers: Frame 2147230245 (3405:276), Frame 2147230245 (3405:276), Frame 2147230246 (3405:278), Frame 2147230246 (3405:278), Window (3405:283), Frame 2088239621 (3405:287), Frame 2147230241 (3405:310), Frame 2147230241 (3405:310), Frame 2147230243 (3405:312), Frame 2147230243 (3405:312), and 4 more
- **Component instances are detached** x5: Instances import as ordinary layout; they stay linked to nothing, so editing the component later will not update them in Rive.
  - Fix: The main component is also added as a Rive component artboard you can reuse.
  - Layers: AI (3405:271), user (3405:277), user (3405:279), user (3405:311), user (3405:313)
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
- `preview-1-Validate-before-scaling_Kit-04.png`: preview image

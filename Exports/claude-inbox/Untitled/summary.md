# Design report: Untitled

Sent: 2026-10-16T05:38:19.542Z

**Will import, with differences** (score 44): 0 to fix, 6 differences, 8 tips.
60 layers, 24 frames, 14 with auto layout, 2 text, 0 images.

## Will look different

- **Curved vector paths** x9: Curves are flattened to straight segments, so round shapes look faceted.
  - Fix: Use ellipses and rectangles with corner radius where you can. Import icons as images, or redraw the curves in Rive.
  - Layers: Vector (2:214), Vector (2:235), Vector (2:236), Vector (2:239), Vector (2:241), Vector (2:244), Vector (2:245), Vector (2:248), Vector (2:249)
- **Radial, angular and diamond gradients** x8: Only linear gradients are converted. These import as a solid colour (the first stop).
  - Fix: Use a linear gradient, or recreate the gradient in Rive after import.
  - Layers: Frame 2147228967 (I2:202;2649:32460), Ellipse 2338 (2:223), Ellipse 2339 (2:224), Tag (2:229), Badge (2:233), Badge (2:237), Badge (2:242), Badge (2:246)
- **Frames without auto layout** x6: Their children are placed by position, so they import as fixed boxes and will not reflow when the content or size changes.
  - Fix: Select the frame and press Shift+A to add auto layout, then set direction, gap and padding. Ignore this for illustrations that should stay fixed.
  - Layers: Content (2:193), Window (2:206), security-check (2:234), limitation (2:238), view (2:243), settings-01 (2:247)
- **Background blur (frosted glass)** x6: Background blur is not supported in Rive.
  - Fix: Fake it with a semi-transparent fill, or add a blurred copy of the background image.
  - Layers: Window (2:206), Check (2:225), Badge (2:233), Badge (2:237), Badge (2:242), Badge (2:246)
- **Blend modes** x4: Blend modes (LINEAR_DODGE) are not converted, so the layer blends normally.
  - Fix: Flatten the effect into the colours, or set the blend mode again in Rive.
  - Layers: Glow / AI (2:200), Glow / AI (2:201), Ellipse 2338 (2:223), Ellipse 2339 (2:224)
- **Dashed strokes**: Dash patterns are not converted; the stroke imports solid.
  - Fix: Add a dash effect to the stroke in Rive after import.
  - Layers: Orbit (2:204)

## Tips

- **Layers with default names** x20: Layer names become names in the Rive hierarchy and are how scripts and state machines find things.
  - Fix: Rename the layers you plan to animate or script (for example "Avatar", "Submit button").
  - Layers: Frame 2147228967 (I2:202;2649:32460), Line (2:203), Ellipse (2:208), Ellipse (2:209), Ellipse (2:210), Image (2:212), Vector (2:214), Ellipse 2338 (2:223), Ellipse 2339 (2:224), Vector (2:228), and 10 more
- **Shadows with spread** x11: Shadow spread is ignored; the shadow imports at the layer's own size.
  - Fix: Set spread to 0 and adjust blur and offset, or use a larger shape under the layer.
  - Layers: Window (2:206), Check (2:225), Tag (2:229), Badge (2:233), Badge (2:233), Badge (2:237), Badge (2:237), Badge (2:242), Badge (2:242), Badge (2:246), and 1 more
- **Fractional sizes** x10: Sizes like 10.667 come from scaled or fill-resized layers and can cause blurry edges.
  - Fix: Round sizes to whole pixels (Figma: select layers → Shift+Alt+drag, or type clean numbers).
  - Layers: Vector (2:228), Vector (2:231), Vector (2:235), Vector (2:236), Vector (2:239), Vector (2:240), Vector (2:241), Vector (2:244), Vector (2:248), Vector (2:249)
- **Clip content with a shadow** x7: Clipping would cut the shadow off, so "Clip content" is switched off for these frames.
  - Fix: If content spills outside the frame, resize or mask it in Figma first.
  - Layers: Window (2:206), Check (2:225), Tag (2:229), Badge (2:233), Badge (2:237), Badge (2:242), Badge (2:246)
- **Inside/outside strokes with a shadow** x3: These cannot be combined (the clip would cut the shadow), so the stroke is drawn centred.
  - Fix: Use a centre stroke, or put the shadow on a separate rectangle underneath.
  - Layers: Dot (2:205), Window (2:206), Check (2:225)
- **Vector shapes** x3: Straight-line vectors import as paths.
  - Fix: Nothing to do.
  - Layers: Vector (2:228), Vector (2:231), Vector (2:240)
- **Component instances are detached**: Instances import as ordinary layout; they stay linked to nothing, so editing the component later will not update them in Rive.
  - Fix: The main component is also added as a Rive component artboard you can reuse.
  - Layers: AI (2:202)
- **2 font files to supply**: Rive does not read fonts from Figma, so each font and weight needs a .ttf file: Geist-SemiBold.ttf, Geist-Medium.ttf.
  - Fix: Put the files in the helper's fonts-library folder (or the project's fonts folder) using exactly these names. Without them a stand-in font is used.

## Fonts needed

- Geist SemiBold -> Geist-SemiBold.ttf
- Geist Medium -> Geist-Medium.ttf

## Files

- `report.json`: this report as data
- `snapshot.json`: the full design data (large; open only for specific layers)
- `preview-1-Start-with-strategic-clarity_K.png`: preview image

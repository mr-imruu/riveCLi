# riveCLi
For helper of rive animation

Everything for turning Figma designs into Rive, with the Rive CLI.

```
Figma to Rive/   the Figma plugin + the local helper (see its README.md and START-HELPER.md)
Fonts Library/   .ttf files the converter needs (Geist). Names must match what the plugin reports
Projects/        Rive CLI projects: Mascot, Start with strategic clarity_Kit 01
Exports/        made by the helper: claude-inbox/ (design reports for Claude) and backups/ (scene backups). Private data, so keep this repo private
```

## Set up on a new computer
1. Install Node.js, then the Rive CLI and sign in: `curl -fsSL https://releases.rive.app/cli/install.sh | sh` then `rive login`.
2. Open a project and check it: `cd Projects/Mascot && rive . --verify`, then `rive .` to preview.
3. Each project's `rive.yaml` has a `push:` block with the ids of the Rive file it was uploaded to. **If you use a different
   Rive account, delete the `push:` lines** and the next `rive push --project=<your project id>` creates a new file.
4. Plugin: in Figma, Plugins -> Development -> Import plugin from manifest -> `Figma to Rive/manifest.json`. Start the helper
   (`cd "Figma to Rive" && node serve.js`) and paste its token into the plugin once.

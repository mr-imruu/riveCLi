# riveCLi
For helper of rive animation

Everything for turning Figma designs into Rive, with the Rive CLI.

```
Figma to Rive/   the Figma plugin + the local helper (see its README.md and START-HELPER.md)
Fonts Library/   .ttf files the converter needs (Geist). Names must match what the plugin reports
Projects/        Rive CLI projects: Mascot, Start with strategic clarity_Kit 01
Exports/        made by the helper: claude-inbox/ (design reports for Claude) and backups/ (scene backups). Private data, so keep this repo private
```

## Easy setup (new computer)
Full step-by-step guide: [SETUP-NEW-COMPUTER.md](SETUP-NEW-COMPUTER.md). Short version:

1. Get the files: `git clone https://github.com/mr-imruu/riveCLi.git` (GitHub must be signed in: GitHub Desktop or `gh auth login`).
2. In that folder run `./setup.sh`. It checks Node.js, the Rive CLI, your Rive login, the fonts and both projects, and tells you
   what to fix. If the Rive CLI is missing it asks before installing it. If you are not signed in, run `rive login`.
3. Double-click **`Start Helper.command`** and leave its window open. It prints a token.
4. In Figma: Plugins -> Development -> Import plugin from manifest -> `Figma to Rive/manifest.json`, then paste the token into
   the plugin once.

Using a **different Rive account**? Delete the `push:` lines in each `Projects/*/rive.yaml` (they hold the ids of the Rive file
it was uploaded to) and set your own project id in `Figma to Rive/config.json` (`rive push --list` shows the ids).

## Updating GitHub from your computer
This folder is the repo. After changes: `git add -A && git commit -m "what changed" && git push`. The helper token (`.token`),
`build/` folders and `.DS_Store` are git-ignored. `Exports/` is committed on purpose, so keep the repo **private**.

# riveCLi
For helper of rive animation

Everything for turning Figma designs into Rive, with the Rive CLI.

```
Figma to Rive/   the Figma plugin + the local helper (see its README.md and START-HELPER.md)
Fonts Library/   .ttf files the converter needs (Geist). Names must match what the plugin reports
Projects/        Rive CLI projects: Mascot, Start with strategic clarity_Kit 01
Exports/        made by the helper: claude-inbox/ (design reports for Claude) and backups/ (scene backups). Private data, so keep this repo private
```

## Easy setup (new computer): 5 steps
Full guide with fixes for common problems: [SETUP-NEW-COMPUTER.md](SETUP-NEW-COMPUTER.md)

1. **Clone the repo:** `git clone https://github.com/mr-imruu/riveCLi.git` (GitHub must be signed in: GitHub Desktop, or `gh auth login`).
2. **Run the setup check:** `cd riveCLi && ./setup.sh`. It checks Node.js, the Rive CLI, your Rive login, the fonts and both
   projects. If the Rive CLI is missing it asks before installing it.
3. **Sign in to Rive** (if setup says you are not): `rive login`, then run `./setup.sh` again until every line has a check mark.
4. **Start the helper:** double-click `Start Helper.command` and leave its window open. It prints a token.
5. **Add the plugin in Figma:** Plugins -> Development -> Import plugin from manifest -> `Figma to Rive/manifest.json`, then
   paste the token into the plugin once.

Using a **different Rive account**? Delete the `push:` lines in each `Projects/*/rive.yaml` and set your own project id in
`Figma to Rive/config.json` (`rive push --list` shows the ids).

## Updating GitHub from your computer
This folder is the repo. After changes: `git add -A && git commit -m "what changed" && git push`. The helper token (`.token`),
`build/` folders and `.DS_Store` are git-ignored. `Exports/` is committed on purpose, so keep the repo **private**.

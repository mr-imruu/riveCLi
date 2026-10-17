# How to start the helper

The helper is a small program that runs on your Mac. The Figma To Rive plugin needs it for **Send to Rive**,
**Add to my open Rive file** and **Send to Claude**. (The plain **Zip only** button works without it.)

## Start it

1. Open **Terminal**.
2. Paste this and press Enter:

```bash
cd "/Users/mr.imruu/Documents/Work Projects/Rive Folder/Figma to Rive" && node serve.js
```

You should see three lines:

```
Figma to Rive helper on http://localhost:4747
Token (paste into the plugin once): ...
Real fonts go in: .../Fonts Library
```

3. **Leave that Terminal tab open.** The helper only works while it is running.

## Token

Your token is saved in the file `.token` in this folder (a hidden file), and the plugin remembers it after the first time.
If the plugin's token box is empty, paste the token the helper printed.

## Stop it

Press **Ctrl-C** in the Terminal tab where it is running.

## If something goes wrong

| What you see | What to do |
|---|---|
| `address already in use` | An old helper is still running. Run `lsof -ti tcp:4747 \| xargs kill`, then start it again. |
| Plugin says "Could not reach the helper" | The helper is not running. Start it (above). |
| Plugin says "bad token" | Paste the token printed by the helper into the plugin's token box. |
| Fonts look the same in every weight | Put real font files in `Fonts Library/` named like `Inter-Regular.ttf`, then send again. |

## What it does (and does not do)

- Listens on your own computer only (`localhost`), and every request needs the token.
- Runs only two commands: `rive <folder> --verify` and `rive push`.
- Nothing is uploaded to your Rive account until you click the push button in the plugin.
- **Send to Claude** saves a report in `Exports/claude-inbox/`. Then tell Claude: "check the inbox".

## Where things are saved
Next to the plugin folder: `../Exports/` (exports and the Claude inbox) and `../Fonts Library/` (put your `.ttf` files here).

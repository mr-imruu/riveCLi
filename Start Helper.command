#!/bin/bash
# Double-click this to start the Figma to Rive helper. Leave the window open; press Ctrl-C to stop.
cd "$(dirname "$0")/Figma to Rive" || { echo "Cannot find the 'Figma to Rive' folder next to this file."; read -r -p "Press Enter to close"; exit 1; }
if ! command -v node >/dev/null 2>&1; then echo "Node.js is not installed. Get it from https://nodejs.org, then double-click this again."; read -r -p "Press Enter to close"; exit 1; fi
node pick-project.js
echo "Starting the helper. Keep this window open while you use the plugin."
node serve.js
echo; read -r -p "The helper stopped. Press Enter to close"

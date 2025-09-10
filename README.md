# Racing Game

A simple top-down racing/dodging game built with **Pygame**.

---

## Overview

This small project is a lightweight racing game where the player controls a car and must avoid enemy cars while trying to increase their score. Enemy cars spawn and move down the screen; the player moves left/right/up/down inside lanes. The game saves a high score in `game_data/high_score.json`.

## Demo / Preview

> Add a GIF or screenshot here (place files inside `images/` and reference them).

---

## Features

* Smooth player movement and lane-based enemy spawning
* Multiple enemy car colors
* Dynamic speed/level changes based on score
* Persistent high score saved to `game_data/high_score.json`
* SVG-based car artwork (fallback to simple rectangles if SVG loading fails)

---

## Requirements

* Python 3.8+ (this project was developed with Python 3.10.8)
* `pygame` (recommended version `2.6.1`, but latest is usually fine)

---

## Quick start (Windows PowerShell)

1. Open PowerShell and navigate to the project folder:

   ```powershell
   cd "C:\Users\mohar\OneDrive\Desktop\game"
   ```

2. (Optional but recommended) Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install requirements:

   ```powershell
   pip install -r requirements.txt
   ```

4. Run the game:

   ```powershell
   python racing_game.py
   ```

---

## Controls

* **Left / Right arrows** — Move left/right
* **Up / Down arrows** — Move forward/back (stay on screen)
* **SPACE** — Start game from menu
* **R** — Restart after game over
* **Q** — Quit

---

## Files and structure

```
game/
├─ racing_game.py        # Main game loop and rendering
├─ game_manager.py      # Game state, scoring and persistence
├─ requirements.txt     # pip dependencies (pygame)
├─ README.md            # You are reading it
├─ .gitignore
├─ images/              # Car SVGs (auto-created by the script if missing)
└─ game_data/           # Runtime data (high score JSON) — ignored by git
```

---

## Notes for packaging / distribution

* `game_data/` is used to store runtime files (high score). It's ignored by Git so each user will create it when they run the game.
* If you want the `images/` folder tracked (so the game shows car images before the first run), copy the SVGs into `images/` and commit them.

---

## Troubleshooting

* **Pygame fails to load SVG**: Pygame's `image.load()` may not load SVGs on some platforms. The game code falls back to drawing rectangles automatically.
* **Permission errors pushing to GitHub**: If you get `Permission denied (publickey)`, either push via HTTPS or add your SSH key to GitHub.

---

## Contributing

If you want to improve the game (new levels, better graphics, sound, menus), fork the repo and send a PR. Keep `game_data/` ignored for safety.

---

## License

This project is released under the **MIT License** — see LICENSE file.

---

## Author

Mohamed Noor Adan

*Created for a simple Pygame project — enjoy!*

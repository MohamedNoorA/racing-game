# Racing Game

A simple top-down racing/dodging game built with **Pygame**.

---

## Overview

This project is a lightweight racing game where the player controls a car and must avoid enemy cars while trying to increase their score.  
Enemy cars spawn and move down the screen; the player moves left, right, up, and down inside lanes.  
The game also saves the highest score in `game_data/high_score.json`.

---

## Demo / Preview

> You can add a GIF or screenshot here (place files inside `images/` and reference them in the README).

---

## Features

* Smooth player movement and lane-based enemy spawning  
* Multiple enemy car colors  
* Increasing speed and difficulty as score rises  
* Persistent high score saved to `game_data/high_score.json`  
* SVG-based car graphics (falls back to rectangles if SVGs fail to load)  

---

## Requirements

* Python **3.8+** (developed with Python **3.10.8**)  
* `pygame` (tested with **2.6.1**, but latest is usually fine)  

---

## Quick start (Windows PowerShell)

1. Open PowerShell and navigate to the project folder:

   ```powershell
   cd "C:\Users\mohar\game"
(Optional but recommended) Create and activate a virtual environment:

powershell
Copy code
python -m venv venv
.\venv\Scripts\Activate.ps1
Install requirements:

powershell
Copy code
pip install -r requirements.txt
Run the game:

powershell
Copy code
python racing_game.py
Controls
Left / Right arrows — Move left/right

Up / Down arrows — Move forward/back (stay on screen)

SPACE — Start game from menu

R — Restart after game over

Q — Quit

Files and structure
bash
Copy code
game/
├─ racing_game.py        # Main game loop and rendering
├─ game_manager.py       # Game state, scoring, and persistence
├─ requirements.txt      # pip dependencies (pygame)
├─ README.md             # You are reading it
├─ .gitignore
├─ images/               # Car SVGs (auto-created if missing)
└─ game_data/            # Runtime data (high score JSON) — ignored by git
Notes for packaging / distribution
game_data/ is used to store runtime files (like high score). It’s ignored by Git so each user will generate their own.

If you want car images available immediately, copy the SVGs into images/ and commit them.

Troubleshooting
SVG loading error: Some platforms may not support SVG loading in Pygame. The game will draw rectangles as fallback.

GitHub push errors: If you get Permission denied (publickey) when pushing, switch to HTTPS or add your SSH key to GitHub.

Contributing
If you’d like to improve the game (better graphics, menus, sounds, or new levels), fork the repo and submit a pull request.
Keep game_data/ ignored to avoid conflicts.

License
This project is released under the MIT License — see LICENSE file.

Author
Mohamed Noor Adan

Created as a simple Pygame project — enjoy!
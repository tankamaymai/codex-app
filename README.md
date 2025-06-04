# codex-app

This repository now includes a gyaru ("gal")-style Tetris game implemented in two ways:

1. A legacy Python version using **pygame** (`gal_tetris.py`).
2. A modern React version for the browser (`index.html` and related scripts).

## Python Version

### Requirements
- Python 3
- `pygame` (`pip install pygame`)

### Running
```bash
python3 gal_tetris.py
```
Use the arrow keys to move/rotate the pieces and the space bar for a hard drop. The score appears in the window title.

## React Version

The React version runs entirely in the browser using React and Babel CDNs. No build step is required.

### Running
Simply open `index.html` in a modern browser. The UI uses a vibrant gal-style color palette and responsive layout.

Use the arrow keys to move and rotate, and the space bar for a hard drop. Your score is shown below the board.

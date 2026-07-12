# 4D Polytope Rotation Visualizer

A real-time, interactive Python/Pygame application that renders six different 4-dimensional polytopes, rotates them through 4D space, and projects them down to a 2D screen so you can visually explore 4D geometry.

## Overview

The visualizer implements a double perspective projection pipeline (4D → 3D → 2D), full 6-plane 4D rotation controls, and w-coordinate color coding, letting you rotate and inspect six classic 4D polytopes interactively.

## Architecture

| Module | Responsibility |
|---|---|
| `main.py` | Entry point — instantiates and runs `App` |
| `app.py` | Owns the main loop, event handling, state (angles, rotation order, toggles) |
| `config.py` | Central constants: window size, colors, speeds, plane/axis mappings |
| `polytopes.py` | `Polytope` abstract base class + 6 concrete polytope generators |
| `rotation.py` | Builds and composes 4D rotation matrices for the 6 rotation planes |
| `projection.py` | Double perspective projection: 4D → 3D → 2D |
| `colouring.py` | Maps w-coordinate to color (RGB or HSV lerp) |
| `rendering.py` | `Display` class + all drawing functions (polytope, legends, FPS, labels) |

## Key Features

### 1. Six Supported Polytopes
Switchable live via keyboard:

| Key | Polytope |
|---|---|
| Q | Pentachoron (5-Cell) |
| W | Tesseract (8-Cell) |
| E | Hexadecachoron (16-Cell) |
| A | Icositetrachoron (24-Cell) |
| S | Hecatonicosachoron (120-Cell) |
| D | Hexacontachoron (600-Cell) |

Each polytope class independently generates its own vertices, edges, and a "bound" (max distance from origin, used for scaling and color normalization). The 120-Cell and 600-Cell use advanced coordinate-orbit math based on H4 Coxeter group symmetry and icosian orbits.

### 2. Full 4D Rotation Control
- Rotation across all 6 coordinate planes: XY, XZ, XW, YZ, YW, ZW
- Ability to select the active rotation plane
- Ability to manually rotate in the chosen plane
- Can reorder which planes get applied first — useful since 4D rotation composition isn't commutative
- Can toggle continuous auto-rotation across all planes
- Can reset all angles and the rotation order

### 3. Double Perspective Projection Pipeline
`projection.py` projects each vertex 4D → 3D (perspective divide using `w`) then 3D → 2D (perspective divide using `z`), so depth cues in both "hidden" dimensions come through as visual perspective.

### 4. W-Value Color Coding
Every vertex and edge is colored based on its w-coordinate (the 4th dimension), interpolated either in RGB or HSV space (**Tab** toggles the mode). Edges get colored gradient segments — not just flat colors — via line-segment interpolation, so you can visually track how deep in "w-space" different parts of the shape are.

### 5. UI / UX
- **T**: toggle numeric w-value labels on each vertex (auto-disabled for the 120-Cell and 600-Cell for performance, since they have hundreds of vertices)
- **H**: toggle helper legend showing all controls
- **F**: toggle FPS counter
- Color legend showing the w-value gradient scale
- Live display of current angles per plane, chosen plane, and rotation order
- Loading screen with progress while all six polytopes are pre-generated at startup

## Controls Summary

| Key | Action |
|---|---|
| Q / W / E / A / S / D | Switch polytope |
| 1–6 | Select rotation plane (XY, XZ, XW, YZ, YW, ZW) |
| → / ← | Rotate in chosen plane |
| Z / X | Move chosen plane earlier / later in rotation order |
| Space | Toggle auto-rotation |
| R | Reset angles and rotation order |
| T | Toggle w-value labels |
| H | Toggle helper legend |
| F | Toggle FPS display |
| Tab | Toggle RGB / HSV color mode |

## Requirements
 
- Python 3
- `pygame`
- `numpy`
- `pyinstaller` (only needed if building a standalone executable)

Install dependencies:
```bash
pip install -r Requirements.txt
```
 
## Running
 
```bash
cd src
python main.py
```
 
## Building a Standalone Executable
 
A Windows standalone executable can be built using PyInstaller via the provided `build.bat` script and `4D-Object-Rotation.spec` file.
 
Run from the project root (where `Requirements.txt` lives):
 
```bash
build.bat
```
 
This will:
1. Install all dependencies from `Requirements.txt` (including PyInstaller).
2. Build a single-file, windowed executable named `4D-Object-Rotation.exe` using `src/main.py` as the entry point.
3. Output the executable to the `dist/` folder.
The build configuration itself lives in `4D-Object-Rotation.spec`, which PyInstaller uses to determine the entry script, packaging options (`--onefile`, `--windowed`), and output name. You can also invoke it directly with:
 
```bash
pyinstaller 4D-Object-Rotation.spec
```
 
Build artifacts (`build/`, `dist/`, `*.spec` outputs) are excluded from version control via `.gitignore`.

## Project Structure

```
.
├── .gitignore
├── .vscode/
│   └── launch.json
├── README.md
├── src/
│   ├── main.py
│   ├── app.py
│   ├── config.py
│   ├── polytopes.py
│   ├── rotation.py
│   ├── projection.py
│   ├── colouring.py
│   └── rendering.py
└── tests/
    └── ...            # earlier prototyping scripts leading up to src/
```

## Notes

- Polytopes are all pre-built once at launch (with a loading screen) rather than regenerated on switch, trading a slightly longer startup for smooth runtime switching.
- Math (rotation, projection, colouring) is cleanly separated from rendering and app state.
- The 5-Cell projection and the 120-Cell / 600-Cell vertex generation used AI assistance for the underlying math; this is noted directly in the source comments in `polytopes.py`.
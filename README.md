# Color Object Tracker

A beginner-friendly real-time Computer Vision application that detects and tracks
red, green, blue, and yellow objects through a webcam. It draws bounding boxes,
marks object centers, displays coordinates and FPS, and includes an interactive
HSV calibration mode for adapting thresholds to different cameras and lighting.

The project uses classical OpenCV image processing—no deep learning, model
downloads, cloud services, or external AI APIs are required.

## Features

- Real-time detection of red, green, blue, and yellow objects
- Bounding boxes, center markers, color labels, and `(X, Y)` coordinates
- FPS display
- Morphological noise removal and minimum-area filtering
- Interactive HSV calibration using six live trackbars
- Original, mask, and isolated-result calibration views
- Graceful webcam initialization and frame-read errors
- Small, beginner-friendly modules with clear responsibilities

## How it works

Each webcam frame is converted from OpenCV's default BGR color format to HSV.
HSV makes it easier to describe a color independently of much of its brightness.
The application selects pixels inside predefined HSV ranges, cleans the resulting
binary masks, and finds the outer contours of the remaining colored regions.

For every sufficiently large contour, the tracker draws a bounding box and center
point, then labels the object with its color and `(X, Y)` center coordinates.

```text
Webcam
  ↓
BGR Frame
  ↓
HSV Conversion
  ↓
Color Mask
  ↓
Noise Removal
  ↓
Contour Detection
  ↓
Bounding Box
  ↓
Object Center
  ↓
Live Visualization
```

## Computer Vision concepts used

- **BGR and HSV color spaces:** OpenCV captures BGR images; HSV is useful for
  selecting colors by hue.
- **Thresholding:** `cv2.inRange()` produces a binary mask containing pixels in a
  chosen HSV range. Red uses two ranges because hue wraps around at the ends of
  OpenCV's 0–179 hue scale.
- **Morphological operations:** Opening removes small specks and closing fills
  small holes in detected regions.
- **Contours:** Connected object boundaries are found in each cleaned mask.
- **Noise filtering:** Contours smaller than 500 pixels are ignored.
- **Bounding boxes and centers:** Each accepted contour is enclosed in a rectangle;
  the rectangle midpoint supplies the displayed coordinates.

## Tech stack

- Python 3
- OpenCV
- NumPy

## Quick start

```bash
git clone git@github.com:Aswin-Times/Color-Object-Tracker.git
cd Color-Object-Tracker
python -m venv .venv
```

Activate the environment, install the requirements, and run the tracker:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/main.py
```

## Installation

1. Clone or download this repository and open a terminal in its root folder.
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate it:

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   macOS or Linux:

   ```bash
   source .venv/bin/activate
   ```

4. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

## How to run

From the project root, run:

```bash
python src/main.py
```

Hold a red, green, blue, or yellow object in front of the default webcam. Good,
even lighting and strongly colored objects produce the best results.

To open the interactive HSV calibration mode instead, run:

```bash
python src/main.py --calibrate
```

### HSV calibration mode

Calibration helps you discover HSV thresholds that suit a particular object,
camera, and lighting setup. It displays three live views:

1. **Original** — the unchanged webcam frame.
2. **HSV Mask** — a black-and-white image where white pixels are inside the
   selected HSV range.
3. **Result** — the original color image with everything outside the selected
   range hidden.

The control window contains six trackbars:

- **H Min / H Max:** Select the hue, or basic color. OpenCV represents hue from
  0 to 179. Red lies at both ends of this circular scale, so it may require two
  separate ranges in a detector.
- **S Min / S Max:** Select saturation, or color intensity. Low saturation is
  gray or pale; high saturation is vivid.
- **V Min / V Max:** Select value, or brightness. Low values are dark and high
  values are bright.

Move one trackbar at a time while holding the target object in view. Adjust the
minimum and maximum values until the object is white in the mask and most of the
background is black. The mask and result update immediately after every change.

Lighting affects both how bright and how vivid a camera sees a color. Sunlight,
indoor bulbs, shadows, reflections, and automatic camera exposure can therefore
change the useful S and V thresholds—and sometimes the apparent hue. Recalibrate
when the camera or lighting conditions change.

The calibration values help you discover useful HSV ranges. To make a tuned
range part of the default detector, update the relevant `COLOR_RANGES` entry in
`src/color_detection.py`.

## Keyboard controls

| Key | Action |
| --- | --- |
| `Q` | Close the tracker or calibration mode |

The key works while the webcam window is focused. Uppercase and lowercase use the
same physical key in this application.

## Example output

The live window shows:

- A colored bounding box around every detected object
- A dot at each object's center
- A label such as `Blue (320, 240)`
- The current frames-per-second value in the top-left corner

Add a screenshot of your own result to the `screenshots/` folder after running
the tracker. Webcam results vary with the camera, lighting, and objects used.

## Project structure

```text
color-object-tracker/
├── src/
│   ├── main.py              # Webcam loop and on-screen display
│   ├── color_detection.py   # HSV masks, contours, and drawing
│   ├── calibration.py       # Interactive HSV trackbars and preview windows
│   └── utils.py             # FPS calculation
├── screenshots/             # Place example captures here
├── requirements.txt
├── README.md
└── .gitignore
```

## Configuration

The main settings are deliberately kept near the top of
`src/color_detection.py`:

- `COLOR_RANGES` contains the lower and upper HSV thresholds.
- `DISPLAY_COLORS` controls bounding-box and label colors.
- `minimum_area` in `detect_objects()` controls how much small noise is ignored.

OpenCV uses a hue range of `0–179`, rather than `0–360`. Red wraps around the
ends of that scale, which is why the default red detector combines two masks.

## Troubleshooting

### The webcam does not open

- Close other applications that may be using the camera.
- Check the operating system's camera privacy permissions.
- Confirm that the default camera is available as device index `0`.

### The correct object is not detected

- Use calibration mode to inspect the live mask.
- Improve lighting and avoid strong shadows or reflections.
- Prefer vivid, solid-colored objects over pale or patterned surfaces.
- Adjust the saturation and value minimums for the environment.

### Too much background is detected

- Narrow the hue range.
- Increase the saturation or value minimum.
- Increase the minimum contour area if small regions remain.

## Learning outcomes

After working through this project, you should understand how to:

- Read live frames from a webcam with OpenCV
- Convert BGR images to HSV
- Segment colors with binary threshold masks
- Clean masks using opening and closing operations
- Extract and filter contours
- Calculate bounding boxes and center coordinates
- Measure and display real-time FPS
- Build interactive OpenCV trackbar controls

## Future improvements

- Save calibrated HSV ranges for later tracking sessions
- Let the user select a different webcam
- Show the individual binary masks for learning and debugging
- Track an object's path over time
- Smooth coordinates between frames to reduce jitter
- Save screenshots or short recordings
- Move HSV settings into a small configuration file

These are natural next steps after understanding this intentionally simple first
version.

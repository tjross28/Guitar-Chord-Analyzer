🎸 Virtual Guitar Chord Detector

This project uses computer vision and hand-tracking AI to recognize common open guitar chords in real-time from a webcam feed. It draws a virtual fretboard overlay on the screen and displays the detected chord name.

🚀 Features

Webcam-based chord recognition using MediaPipe Hands

Rule-based chord detection for common open chords (C, G, D, A, E major/minor, etc.)

Virtual fretboard overlay with strings and frets drawn on screen

Interactive fretboard setup: click and drag with your mouse to select your real guitar fretboard once, then the program maps your fingers onto it

Live feedback showing:

Finger positions (string + fret)

Detected chord name

🛠️ Tech Stack

Python

OpenCV (for webcam and drawing overlays)

MediaPipe (for hand + finger landmark detection)

📷 How It Works

Launch the program.

Use your mouse to select the area of the screen where your guitar fretboard is.

Place your hand on the guitar — finger positions are detected and mapped to strings/frets.

The program matches these positions to stored chord shapes and displays the chord name in real time.

🎯 Example Use Cases

Beginner guitar players learning chord shapes

Interactive music/AI demos

CV + ML project portfolio piece for recruiters

✅ Roadmap / Future Ideas

Save fretboard calibration for reuse (no need to redraw every session)

Expand chord library (barre chords, 7th chords, etc.)

Audio-based chord verification with microphone input

Full auto fretboard detection using contour/edge detection

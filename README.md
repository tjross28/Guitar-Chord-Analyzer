🎸 Virtual Guitar Chord Detector

A computer vision project that detects guitar chord shapes in real time using a webcam.
Built with OpenCV and MediaPipe Hands, the program tracks fingertip positions, maps them onto a virtual fretboard, and identifies common open chords (C, G, D, E, A, etc.).

🔑 Features

Real-time hand tracking with MediaPipe.

Virtual fretboard overlay (strings + frets).

Fingertip detection with labels showing string & fret.

Rule-based chord recognition for common open chords.

On-screen display of the detected chord.

🛠️ Tech Stack

Python 3

OpenCV for webcam + visualization.

MediaPipe for hand landmark tracking.

🚀 How It Works

The webcam feed is captured and flipped for a mirror view.

A fretboard grid (6 strings × 4 frets) is drawn on-screen.

Fingertip coordinates are tracked and mapped to strings/frets.

The program compares the detected finger positions to a set of predefined chord shapes.

The current chord is displayed in real time.

🎯 Example Use Cases

Visual learning tool for beginners learning chords.

Fun demo project combining computer vision + music.

Showcase of real-time pattern recognition in Python.

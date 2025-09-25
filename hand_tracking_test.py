import cv2
import mediapipe as mp

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Rule-based open chord definitions
open_chords = {
    "C major": [(2, 1), (4, 2), (5, 3)],
    "G major": [(5, 2), (6, 3), (1, 3)],
    "E minor": [(5, 2), (4, 2)],
    "D major": [(3, 2), (1, 2), (2, 3)],
    "A major": [(4, 2), (3, 2), (2, 2)],
    "E major": [(5, 2), (4, 2), (3, 1)]
}

# Webcam setup
cap = cv2.VideoCapture(0)
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Fretboard area (virtual box on screen)
fretboard_x1, fretboard_y1 = 100, 100
fretboard_x2, fretboard_y2 = 500, 350
num_strings = 6
num_frets = 4

def detect_chord(finger_positions):
    """Match finger positions against known chords."""
    for chord, positions in open_chords.items():
        if all(pos in finger_positions for pos in positions):
            return chord
    return "Unknown"

def draw_virtual_fretboard(frame):
    """Draw fretboard overlay (strings & frets)."""
    for i in range(num_strings + 1):
        x = int(fretboard_x1 + i * (fretboard_x2 - fretboard_x1) / num_strings)
        cv2.line(frame, (x, fretboard_y1), (x, fretboard_y2), (200, 200, 200), 2)

    for j in range(num_frets + 1):
        y = int(fretboard_y1 + j * (fretboard_y2 - fretboard_y1) / num_frets)
        cv2.line(frame, (fretboard_x1, y), (fretboard_x2, y), (180, 180, 180), 2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    finger_positions = []

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            for idx in [8, 12, 16, 20]:  # Fingertips
                x = int(hand_landmarks.landmark[idx].x * frame.shape[1])
                y = int(hand_landmarks.landmark[idx].y * frame.shape[0])

                if fretboard_x1 < x < fretboard_x2 and fretboard_y1 < y < fretboard_y2:
                    string = int(((x - fretboard_x1) / (fretboard_x2 - fretboard_x1)) * num_strings) + 1
                    fret = int(((y - fretboard_y1) / (fretboard_y2 - fretboard_y1)) * num_frets) + 1
                    finger_positions.append((string, fret))

                    cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)

    # Detect chord
    chord = detect_chord(finger_positions)

    # Show chord name on screen
    cv2.putText(frame, f"Chord: {chord}", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Draw fretboard
    draw_virtual_fretboard(frame)

    cv2.imshow("Virtual Guitar Chord Detector", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()

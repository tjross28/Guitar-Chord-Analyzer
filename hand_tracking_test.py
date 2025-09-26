import cv2
import mediapipe as mp

# Mediapipe setup
mp_hands = mp.solutions.hands

# Rule-based open chord definitions
open_chords = {
    "C major": [(2, 1), (4, 2), (5, 3)],
    "G major": [(5, 2), (6, 3), (1, 3)],
    "E minor": [(5, 2), (4, 2)],
    "D major": [(3, 2), (1, 2), (2, 3)],
    "A major": [(4, 2), (3, 2), (2, 2)],
    "E major": [(5, 2), (4, 2), (3, 1)]
}

# Webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Could not open webcam")
    exit()

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# --- Smaller fretboard box ---
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

box_width = int(frame_width * 0.4)   # narrower (40% of screen width)
box_height = int(frame_height * 0.18) # shorter (18% of screen height)
x1 = int(frame_width * 0.1)          # still left aligned
y1 = int(frame_height * 0.65)        # shifted lower
x2 = x1 + box_width
y2 = y1 + box_height

# Virtual fretboard setup
num_strings = 6
num_frets = 4

def detect_chord(finger_positions):
    for chord, positions in open_chords.items():
        if all(pos in finger_positions for pos in positions):
            return chord
    return "Unknown"

def draw_virtual_fretboard(frame):
    # Draw frets (vertical lines)
    for j in range(num_frets + 1):
        x = int(x1 + j * (x2 - x1) / num_frets)
        cv2.line(frame, (x, y1), (x, y2), (200, 200, 200), 2)

    # Draw strings (horizontal lines, 6 = top, 1 = bottom)
    for i in range(num_strings + 1):
        y = int(y1 + i * (y2 - y1) / num_strings)
        cv2.line(frame, (x1, y), (x2, y), (180, 180, 180), 2)

    # Label string numbers (6 at top → 1 at bottom)
    for i in range(num_strings):
        y = int(y1 + i * (y2 - y1) / num_strings + (y2 - y1) / (2 * num_strings))
        string_num = num_strings - i  # flip numbering
        cv2.putText(frame, str(string_num), (x1 - 25, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Always flip video (mirror)
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    finger_positions = []

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Only draw fingertip dots, no skeleton
            for idx in [8, 12, 16, 20]:  # fingertips
                x = int(hand_landmarks.landmark[idx].x * frame.shape[1])
                y = int(hand_landmarks.landmark[idx].y * frame.shape[0])

                if x1 < x < x2 and y1 < y < y2:
                    # Map x → fret, y → string (6 on top, 1 on bottom)
                    fret = int(((x - x1) / (x2 - x1)) * num_frets) + 1
                    string = num_strings - int(((y - y1) / (y2 - y1)) * num_strings)
                    finger_positions.append((string, fret))

                    cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)
                    cv2.putText(frame, f"S{string}F{fret}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    chord = detect_chord(finger_positions)
    draw_virtual_fretboard(frame)
    cv2.putText(frame, f"Chord: {chord}", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Virtual Guitar Chord Detector", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()

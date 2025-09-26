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

# Variables for mouse selection
drawing = False
ix, iy = -1, -1
fretboard_box = None

def draw_box(event, x, y, flags, param):
    global ix, iy, drawing, fretboard_box
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        fretboard_box = (ix, iy, x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        fretboard_box = (ix, iy, x, y)

cv2.namedWindow("Select Fretboard")
cv2.setMouseCallback("Select Fretboard", draw_box)

# Step 1: Select fretboard box
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Always flip the live feed
    frame = cv2.flip(frame, 1)
    temp_frame = frame.copy()

    if fretboard_box:
        x1, y1, x2, y2 = fretboard_box
        cv2.rectangle(temp_frame, (ix, iy), (x2, y2), (0, 255, 0), 2)

    cv2.putText(temp_frame, "Drag to select fretboard, press SPACE to confirm",
                (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Select Fretboard", temp_frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 32 and fretboard_box:  # SPACE to confirm
        break
    elif key == 27:  # ESC to quit
        cap.release()
        cv2.destroyAllWindows()
        exit()

# Normalize box coordinates so x1 < x2 and y1 < y2
x1, y1, x2, y2 = fretboard_box
x1, x2 = min(x1, x2), max(x1, x2)
y1, y2 = min(y1, y2), max(y1, y2)
cv2.destroyWindow("Select Fretboard")

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

    # Draw strings (horizontal lines, top = string 1, bottom = string 6)
    for i in range(num_strings + 1):
        y = int(y1 + i * (y2 - y1) / num_strings)
        cv2.line(frame, (x1, y), (x2, y), (180, 180, 180), 2)

    # Label string numbers (1–6, top to bottom)
    for i in range(num_strings):
        y = int(y1 + i * (y2 - y1) / num_strings + (y2 - y1) / (2 * num_strings))
        string_num = i + 1
        cv2.putText(frame, str(string_num), (x1 - 25, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Always flip video
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
                    # Map x → fret, y → string (1 on top, 6 on bottom)
                    fret = int(((x - x1) / (x2 - x1)) * num_frets) + 1
                    string = int(((y - y1) / (y2 - y1)) * num_strings) + 1
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

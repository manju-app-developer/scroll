import cv2
import mediapipe as mp
import time
import ctypes
import threading

# Key control
KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002
VK_DOWN = 0x28
VK_UP = 0x26

def press_key(key):
    ctypes.windll.user32.keybd_event(key, 0, KEYEVENTF_KEYDOWN, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(key, 0, KEYEVENTF_KEYUP, 0)

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.75)
mp_draw = mp.solutions.drawing_utils

TIP_IDS = [4, 8, 12, 16, 20]
SCROLL_COOLDOWN = 1.5
last_scroll_time = 0
enabled = False
thread_running = False

def count_fingers(hand_landmarks):
    fingers = []
    lm = hand_landmarks.landmark
    fingers.append(int(lm[TIP_IDS[0]].x < lm[TIP_IDS[0] - 1].x))
    for i in range(1, 5):
        fingers.append(int(lm[TIP_IDS[i]].y < lm[TIP_IDS[i] - 2].y))
    return sum(fingers)

def gesture_loop():
    global last_scroll_time, thread_running
    print("🖐️ Gesture loop started.")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while thread_running:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        now = time.time()

        if enabled and results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                fingers_up = count_fingers(hand_landmarks)
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if fingers_up == 5 and now - last_scroll_time > SCROLL_COOLDOWN:
                    print("🖐️ Open Palm → Scroll Down")
                    press_key(VK_DOWN)
                    last_scroll_time = now
                elif fingers_up == 0 and now - last_scroll_time > SCROLL_COOLDOWN:
                    print("✊ Fist → Scroll Up")
                    press_key(VK_UP)
                    last_scroll_time = now

        cv2.putText(frame, f"Gesture Scroll: {'ON' if enabled else 'OFF'}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0) if enabled else (0, 0, 255), 2)

        cv2.imshow("Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    thread_running = False
    print("🛑 Gesture loop ended.")

def start_loop():
    global thread_running
    if not thread_running:
        thread_running = True
        threading.Thread(target=gesture_loop, daemon=True).start()

def toggle_enabled():
    global enabled
    enabled = not enabled
    return enabled

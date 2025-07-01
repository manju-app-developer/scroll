import cv2, mediapipe as mp, time, ctypes, threading

KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002
VK_DOWN = 0x28
VK_UP = 0x26

def press_key(key):
    ctypes.windll.user32.keybd_event(key, 0, KEYEVENTF_KEYDOWN, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(key, 0, KEYEVENTF_KEYUP, 0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.75)
mp_draw = mp.solutions.drawing_utils

TIP_IDS = [4, 8, 12, 16, 20]
SCROLL_COOLDOWN = 1.5

enabled = False
thread_running = False
last_scroll_time = 0

def count_fingers(lm):
    tips = [4, 8, 12, 16, 20]
    fingers = [int(lm[tips[0]].x < lm[tips[0] - 1].x)]
    for i in range(1, 5):
        fingers.append(int(lm[tips[i]].y < lm[tips[i] - 2].y))
    return sum(fingers)

def gesture_loop():
    global thread_running, last_scroll_time
    print("Gesture detection started")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while thread_running:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        now = time.time()

        if enabled and results.multi_hand_landmarks:
            for hm in results.multi_hand_landmarks:
                fingers = count_fingers(hm.landmark)
                mp_draw.draw_landmarks(frame, hm, mp_hands.HAND_CONNECTIONS)
                if fingers == 5 and now - last_scroll_time > SCROLL_COOLDOWN:
                    print("Scroll Down")
                    press_key(VK_DOWN)
                    last_scroll_time = now
                elif fingers == 0 and now - last_scroll_time > SCROLL_COOLDOWN:
                    print("Scroll Up")
                    press_key(VK_UP)
                    last_scroll_time = now

        cv2.putText(frame, f"Gesture: {'ON' if enabled else 'OFF'}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0) if enabled else (0,0,255), 2)
        cv2.imshow("Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    thread_running = False
    print("Gesture detection stopped")

def start_loop():
    global thread_running
    if not thread_running:
        thread_running = True
        threading.Thread(target=gesture_loop, daemon=True).start()

def toggle_enabled():
    global enabled
    enabled = not enabled
    return enabled

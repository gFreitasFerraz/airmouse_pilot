import cv2
import time
import math
import mediapipe as mp
import pyautogui

# =========================
# CONFIGURAÇÕES
# =========================
MODEL_PATH = "/seu-caminho/para/gesture_recognizer.task"
CAMERA_INDEX = 1   # se não abrir, troque para 0

SMOOTHING = 0.2
CLICK_DISTANCE = 35        # distância em pixels entre polegar e indicador para clicar
CLICK_COOLDOWN = 0.45      # intervalo mínimo entre cliques
FRAME_REDUCTION = 100      # margem da área ativa para melhorar precisão

# Segurança do PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01
    
screen_w, screen_h = pyautogui.size()

# =========================
# MEDIAPIPE
# =========================
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

gesture_text = "Sem gesto"
hand_landmarks_list = []

# conexões visuais da mão
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]

def result_callback(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global gesture_text, hand_landmarks_list

    hand_landmarks_list = result.hand_landmarks

    if result.gestures and len(result.gestures) > 0 and len(result.gestures[0]) > 0:
        top_gesture = result.gestures[0][0]
        gesture_text = f"{top_gesture.category_name} ({top_gesture.score:.2f})"
    else:
        gesture_text = "Sem gesto"

def draw_hand(frame, landmarks_list):
    h, w, _ = frame.shape

    for hand_landmarks in landmarks_list:
        # linhas
        for start_idx, end_idx in HAND_CONNECTIONS:
            x1 = int(hand_landmarks[start_idx].x * w)
            y1 = int(hand_landmarks[start_idx].y * h)
            x2 = int(hand_landmarks[end_idx].x * w)
            y2 = int(hand_landmarks[end_idx].y * h)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # pontos
        for lm in hand_landmarks:
            cx = int(lm.x * w)
            cy = int(lm.y * h)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def map_range(value, in_min, in_max, out_min, out_max):
    if in_max - in_min == 0:
        return out_min
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=1,
    result_callback=result_callback
)

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print("Não foi possível abrir a webcam.")
    raise SystemExit

prev_mouse_x, prev_mouse_y = pyautogui.position()
last_click_time = 0

window_name = "AirMouse"

with GestureRecognizer.create_from_options(options) as recognizer:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar frame.")
            break

        # desespelha a câmera
        frame = cv2.flip(frame, 1)

        frame_h, frame_w, _ = frame.shape

        # área ativa de controle
        x1 = FRAME_REDUCTION
        y1 = FRAME_REDUCTION
        x2 = frame_w - FRAME_REDUCTION
        y2 = frame_h - FRAME_REDUCTION

        # envia frame para o MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        timestamp_ms = int(time.time() * 1000)
        recognizer.recognize_async(mp_image, timestamp_ms)

        # desenha área ativa
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

        # desenha mão
        draw_hand(frame, hand_landmarks_list)

        if hand_landmarks_list:
            hand = hand_landmarks_list[0]

            # landmark 8 = ponta do indicador
            index_tip = hand[8]

            # landmark 4 = ponta do polegar
            thumb_tip = hand[4]

            ix = int(index_tip.x * frame_w)
            iy = int(index_tip.y * frame_h)

            tx = int(thumb_tip.x * frame_w)
            ty = int(thumb_tip.y * frame_h)

            # ponto visual do indicador
            cv2.circle(frame, (ix, iy), 10, (0, 0, 255), -1)

            # mapeia indicador da área ativa da câmera para a tela
            ix_clamped = clamp(ix, x1, x2)
            iy_clamped = clamp(iy, y1, y2)

            target_mouse_x = map_range(ix_clamped, x1, x2, 0, screen_w)
            target_mouse_y = map_range(iy_clamped, y1, y2, 0, screen_h)

            # suavização
            smooth_mouse_x = prev_mouse_x + (target_mouse_x - prev_mouse_x) * SMOOTHING
            smooth_mouse_y = prev_mouse_y + (target_mouse_y - prev_mouse_y) * SMOOTHING

            pyautogui.moveTo(smooth_mouse_x, smooth_mouse_y)

            prev_mouse_x, prev_mouse_y = smooth_mouse_x, smooth_mouse_y

            # distância entre polegar e indicador
            pinch_distance = math.hypot(ix - tx, iy - ty)

            # linha visual da pinça
            cv2.line(frame, (ix, iy), (tx, ty), (255, 0, 255), 2)
            cv2.putText(
                frame,
                f"Pinch: {int(pinch_distance)}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            # clique com cooldown
            now = time.time()
            if pinch_distance < CLICK_DISTANCE and (now - last_click_time) > CLICK_COOLDOWN:
                pyautogui.click()
                last_click_time = now

                cv2.putText(
                    frame,
                    "CLICK!",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

        # texto do gesto
        cv2.putText(
            frame,
            gesture_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.imshow(window_name, frame)

        # sair com q
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # sair fechando a janela
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

cap.release()
cv2.destroyAllWindows()
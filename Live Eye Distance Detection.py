
import cv2
import mediapipe as mp
import math

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)

# الطول الحقيقي للبطاقة (سم)
CARD_WIDTH_CM = 8.56

cap = cv2.VideoCapture(0)

clicked_points = []

def mouse_callback(event, x, y, flags, param):
    global clicked_points
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        print("Point selected:", (x, y))

cv2.namedWindow("Calibrate")
cv2.setMouseCallback("Calibrate", mouse_callback)

calibrated = False
cm_per_pixel = None

print("  click points   ")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    display = frame.copy()

    # لو جمعنا نقطتين → نحسب المعايرة
    if len(clicked_points) == 2 and not calibrated:
        p1, p2 = clicked_points
        pixel_distance = math.dist(p1, p2)
        cm_per_pixel = CARD_WIDTH_CM / pixel_distance
        calibrated = True
        print("Calibration complete → cm per pixel =", cm_per_pixel)

    # نعرض النقاط للمستخدم
    for p in clicked_points:
        cv2.circle(display, p, 5, (0, 255, 0), -1)

    cv2.putText(display, "Click 2 points on VISA card", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Calibrate", display)

    if calibrated:
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ---------------------- بعد المعايرة نبدأ قياس العينين ----------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    eye_distance_px = None

    if results.multi_face_landmarks:
        face = results.multi_face_landmarks[0]

        r_eye = face.landmark[33]
        l_eye = face.landmark[263]

        x1, y1 = int(r_eye.x * w), int(r_eye.y * h)
        x2, y2 = int(l_eye.x * w), int(l_eye.y * h)

        cv2.circle(frame, (x1, y1), 4, (0, 255, 0), -1)
        cv2.circle(frame, (x2, y2), 4, (0, 255, 0), -1)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 200, 0), 2)

        eye_distance_px = math.dist((x1, y1), (x2, y2))

    if eye_distance_px and calibrated:
        eye_cm = eye_distance_px * cm_per_pixel

        cv2.putText(frame, f"Eye Distance: {int(eye_distance_px)} px", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame, f"Eye Distance: {eye_cm:.2f} cm", (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Eye Distance (CM)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

from imutils import face_utils
from utils import *
import numpy as np
import pyautogui
import imutils
import dlib
import cv2

# Пороги и последовательная длина кадра для запуска действия мыши
mouth_array_threshold = 0.6
mouth_array_consecutive_frames = 15
eye_array_threshold = 0.19
eye_array_consecutive_frames = 15
blink_array_different_threshold = 0.04
blink_array_close_threshold = 0.19
blink_consecutive_frames = 10

# Инициализировать счетчики кадров для каждого действия и логические значения
mouth_counter = 0
eye_counter = 0
blink_counter = 0
input_mode = False
eye_click = False
left_blink = False
right_blink = False
scroll_mode = False
anchor_point = (0, 0)
white_color = (255, 255, 255)
yellow_color = (17, 255, 255)
red_color = (36, 48, 238)
green_color = (80, 255, 15)
blue_color = (217, 87, 0)
black_color = (48, 40, 0)

# Инициализировать детектор лица Dlib, затем создать предиктор лицевых ориентиров
shape_predictor = "model/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor)

# Взять индексы лицевых ориентиров
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# Захват видео
vid = cv2.VideoCapture(0)
resolution_w = 1600
resolution_h = 800
cam_w = 840
cam_h = 640
unit_w = resolution_w / cam_w
unit_h = resolution_h / cam_h

while True:
    # Захватить кадр, изменить размер, преобразовать его в серые оттенки
    _, frame = vid.read()
    frame = cv2.flip(frame, 1)
    frame = imutils.resize(frame, width=cam_w, height=cam_h)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Обнаружение лица в серых оттенках
    rects = detector(gray, 0)

    # Цикл по обнаружению лица
    if len(rects) > 0:
        rect = rects[0]
    else:
        # cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        continue

    # Определить лицевые ориентиры, преобразовать координаты (x, y) в множество NumPy
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)

    # Извлечь координаты левого и правого глаза для вычисления соотношения сторон
    mouth = shape[mStart:mEnd]
    left_eye = shape[lStart:lEnd]
    right_eye = shape[rStart:rEnd]
    nose = shape[nStart:nEnd]

    # Отзеркалить изображение
    temp = left_eye
    left_eye = right_eye
    right_eye = temp

    # Среднее соотношение сторон рта для обоих глаз
    mar = mouth_aspect_ratio(mouth)
    left_ear = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)
    ear = (left_ear + right_ear) / 2.0
    different_ear = np.abs(left_ear - right_ear)

    nose_point = (nose[3, 0], nose[3, 1])

    # Вычислить и визуализировать оболочку глаз
    mouth_hull = cv2.convexHull(mouth)
    left_eye_hull = cv2.convexHull(left_eye)
    right_eye_hull = cv2.convexHull(right_eye)
    cv2.drawContours(frame, [mouth_hull], -1, yellow_color, 1)
    cv2.drawContours(frame, [left_eye_hull], -1, yellow_color, 1)
    cv2.drawContours(frame, [right_eye_hull], -1, yellow_color, 1)

    for (x, y) in np.concatenate((mouth, left_eye, right_eye), axis=0):
        cv2.circle(frame, (x, y), 2, green_color, -1)

    # Проверка соотношения глаз и счетчика
    if different_ear > blink_array_different_threshold:

        if left_ear < right_ear:
            if left_ear < eye_array_threshold:
                blink_counter += 1

                if blink_counter > blink_consecutive_frames:
                    pyautogui.doubleClick()

                    blink_counter = 0

        elif left_ear > right_ear:
            if right_ear < eye_array_threshold:
                blink_counter += 1

                if blink_counter > blink_consecutive_frames:
                    pyautogui.rightClick()

                    blink_counter = 0
        else:
            blink_counter = 0
    else:
        if ear <= eye_array_threshold:
            eye_counter += 1

            if eye_counter > eye_array_consecutive_frames:
                scroll_mode = not scroll_mode
                eye_counter = 0

        else:
            eye_counter = 0
            blink_counter = 0

    if mar > mouth_array_threshold:
        mouth_counter += 1

        if mouth_counter >= mouth_array_consecutive_frames:
            input_mode = not input_mode
            mouth_counter = 0
            anchor_point = nose_point

    else:
        mouth_counter = 0

    if input_mode:
        cv2.putText(frame, "Reading Input", (590, 30), cv2.FONT_HERSHEY_PLAIN, 2, red_color, 2)
        x, y = anchor_point
        nx, ny = nose_point
        w, h = 60, 35
        multiple = 1
        cv2.rectangle(frame, (x - w, y - h), (x + w, y + h), (255, 255, 0), 2)
        cv2.line(frame, anchor_point, nose_point, green_color, 2)

        directions = direction(nose_point, anchor_point, w, h)
        cv2.putText(frame, directions.capitalize(), (665, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, blue_color, 2)
        drag = 18
        if directions == 'Right':
            pyautogui.moveRel(drag, 0)
        elif directions == 'Left':
            pyautogui.moveRel(-drag, 0)
        if directions == 'Up':
            if scroll_mode:
                pyautogui.hscroll(40)
            else:
                pyautogui.moveRel(0, -drag)
        elif directions == 'Down':
            if scroll_mode:
                pyautogui.hscroll(-40)
            else:
                pyautogui.moveRel(0, drag)

    if scroll_mode:
        cv2.putText(frame, 'Scrolling Mode', (590, 150), cv2.FONT_HERSHEY_PLAIN, 2, red_color, 2)

    cv2.putText(frame, "MAR: {:.2f}".format(mar), (30, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, blue_color, 2)
    cv2.putText(frame, "Right EAR: {:.2f}".format(right_ear), (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, blue_color, 2)
    cv2.putText(frame, "Left EAR: {:.2f}".format(left_ear), (30, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, blue_color, 2)
    # cv2.putText(frame, "Diff EAR: {:.2f}".format(np.abs(left_ear - right_ear)), (460, 80),
    # cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Показать окно
    cv2.imshow("Head Control", frame)
    key = cv2.waitKey(1) & 0xFF

    # При нажатии `Esc` выход
    if key == 27:
        break

# Очистить
cv2.destroyAllWindows()
vid.release()

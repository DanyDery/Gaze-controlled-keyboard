import numpy as np


# Возвращает EAR с заданными ориентирами для глаз
def eye_aspect_ratio(eye):
    # Вычислить евклидовы расстояния между двумя наборами вертикальных ориентиров глаза
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])

    # Вычислить евклидово расстояние между горизонтальными глазными ориентирами
    C = np.linalg.norm(eye[0] - eye[3])

    # Вычислить соотношение сторон глаза
    ear = (A + B) / (2.0 * C)

    # Вернуть соотношение сторон глаза
    return ear


# Возвращает MAR с учетом ориентиров глаза
def mouth_aspect_ratio(mouth):
    # Вычислить евклидовы расстояния между тремя наборами вертикальных ориентиров
    A = np.linalg.norm(mouth[13] - mouth[19])
    B = np.linalg.norm(mouth[14] - mouth[18])
    C = np.linalg.norm(mouth[15] - mouth[17])

    # Вычислить евклидово расстояние между горизонтальными ориентирами области
    D = np.linalg.norm(mouth[12] - mouth[16])

    # Вычислить соотношение сторон рта
    mar = (A + B + C) / (2 * D)

    # Вернуть соотношение сторон рта
    return mar


# Направление с учетом позиции носа и опорных точек.
def direction(nose_point, anchor_point, w, h, multiple=1):
    nx, ny = nose_point
    x, y = anchor_point

    if nx > x + multiple * w:
        return 'Right'
    elif nx < x - multiple * w:
        return 'Left'

    if ny > y + multiple * h:
        return 'Down'
    elif ny < y - multiple * h:
        return 'Up'

    return 'None'

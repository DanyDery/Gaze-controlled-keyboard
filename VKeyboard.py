import cv2
import numpy as np
import cvzone
from pynput.keyboard import Controller

keyboard = np.zeros((1000, 1500, 3), np.uint8) + 100
keyboard[:] = (121, 4, 66)

width = 85
height = 85
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 2
font_thickness = 2


def draw_all(image, list_of_button, letter_light):
    for letter in list_of_button:
        x, y = letter.pos
        w, h = letter.size

        if letter_light is True:
            cv2.rectangle(image, letter.pos, (x + w, y + h), (147, 54, 106), -1)
        else:
            cv2.rectangle(image, letter.pos, (x + w, y + h), (147, 54, 106), 2)

        text_size = cv2.getTextSize(letter.letter, font, font_scale, font)
        width_text, height_text = text_size[0], text_size[1]
        text_x = int((width - width_text[0]) / 2) + x
        text_y = int((height + height_text) / 2) + y + 10
        cv2.putText(image, letter.letter, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

    return image


class Button:
    pos: object

    def __init__(self, pos, letter, size=[85, 85]):
        self.pos = pos
        self.letter = letter
        self.size = size

    def __repr__(self):
        return "Letter {a}, Pos {b}".format(a=self.letter, b=self.pos)


keys = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '+', '*', '/'],
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '(', ')'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', "'", '#'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '!', '?', '@']]

final_text = ""
button_list = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        button_list.append(Button([100 * j + 50, 100 * i + 50], key))

cvzone.cornerRect(keyboard, (button_list[20].pos[0], button_list[20].pos[1],
                             button_list[20].size[0], button_list[20].size[0]), 1, rt=3)

cv2.rectangle(keyboard, (50, 500), (1250, 600), (147, 54, 106), -1)
cv2.putText(keyboard, "Final Text", (60, 565), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 1)

if __name__ == "__main__":
    draw_all(keyboard, button_list, False)
    cv2.imshow("Keyboard", keyboard)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

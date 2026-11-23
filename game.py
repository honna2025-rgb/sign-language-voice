import cv2
import numpy as np

class Game:

    def __init__(self):
        self.prev_x = None
        self.prev_y = None
        self.canvas = None

    def update(self, img, finger_x, finger_y, erase):

        if self.canvas is None:
            self.canvas = np.zeros_like(img)

        if finger_x is not None and finger_y is not None:

            if self.prev_x is None:
                self.prev_x = finger_x
                self.prev_y = finger_y

            if erase:
                # eraser
                cv2.circle(self.canvas, (finger_x, finger_y), 40, (0,0,0), -1)
            else:
                # draw line
                cv2.line(self.canvas,
                         (self.prev_x, self.prev_y),
                         (finger_x, finger_y),
                         (255,0,0), 5)

            self.prev_x = finger_x
            self.prev_y = finger_y

        img = cv2.add(img, self.canvas)

        return img
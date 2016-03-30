import copy
import random

from parameters import ROTATION, BRIGHTNESS, FRAME, PARAMETERS


class Figure:
    def __init__(self, parameters):
        self.number = parameters[0]
        self.rotation = parameters[1][0]
        self.rotation_possible_change = parameters[1][1]
        self.brightness = parameters[2][0]
        self.brightness_possible_change = parameters[2][1]
        self.frame = parameters[3][0]
        self.frame_possible_change = parameters[3][1]
        self.elements_changed = []

    def __str__(self):
        return "{} {} {} {} {}".format(self.number, self.rotation, self.brightness, self.frame, self.elements_changed)

    def return_parameters(self):
        return {
            "figure": self.number,
            "rotation": ROTATION[self.rotation],
            "brightness": BRIGHTNESS[self.brightness],
            "frame": FRAME[self.frame],
            "elements_changed": self.elements_changed
        }

    def change_rotation(self):
        self.rotation = (self.rotation + self.rotation_possible_change)
        assert (self.rotation >= 0), "rotation = {}".format(self.rotation)
        assert (self.rotation < len(ROTATION)), "rotation = {}".format(self.rotation)
        self.elements_changed.append(['rotation', self.rotation_possible_change])

    def change_brightness(self):
        self.brightness = (self.brightness + self.brightness_possible_change)
        assert (self.brightness >= 0), "brightness = {}".format(self.brightness)
        assert (self.brightness < len(BRIGHTNESS)), "brightness = {}".format(self.brightness)
        self.elements_changed.append(['brightness', self.brightness_possible_change])

    def change_frame(self):
        self.frame = (self.frame + self.frame_possible_change)
        assert (self.frame >= 0), "frame = {}".format(self.frame)
        assert (self.frame < len(FRAME)), "frame = {}".format(self.frame)
        self.elements_changed.append(['frame', self.frame_possible_change])

    def change_parameter(self, name):
        if name == 'rotation':
            self.change_rotation()
        elif name == 'brightness':
            self.change_brightness()
        elif name == 'frame':
            self.change_frame()

    def change_parameters(self, elements_to_change):
        parameters = copy.deepcopy(PARAMETERS)
        random.shuffle(parameters)

        for idx in range(elements_to_change):
            self.change_parameter(parameters[idx])
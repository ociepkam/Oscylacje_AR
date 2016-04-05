from enum import Enum

FIGURES = range(1, 21)
ROTATION = [0, 90, 180, 270]
BRIGHTNESS = ['white', 'gray', 'slate']
FRAME = ['thin', 'narrow', 'wide']
PARAMETERS = ['rotation', 'brightness', 'frame']
PARAMETERS_DICT = {'rotation': ROTATION, 'brightness': BRIGHTNESS, 'frame': FRAME}
CHANGES_LVL = [-2, -1, 1, 2]


class Instruction_type (Enum):
    text = "text"
    image = "image"


class Trial_type (Enum):
    instruction = 'instruction'
    experiment = 'experiment'
    training = 'training'


class Per(Enum):
    small = (2, 2)
    big = (3, 2)


def create_changes_pairs(parameter):
    possible_changes_pair = []
    possible_first_arguments = range(len(parameter))
    for elem in possible_first_arguments:
        for change_lvl in CHANGES_LVL:
            if 0 <= change_lvl + elem < len(parameter):
                possible_changes_pair.append([elem, change_lvl])
    return possible_changes_pair


FRAME_CHANGES_PAIRS = create_changes_pairs(PARAMETERS_DICT['frame'])
BRIGHTNESS_CHANGES_PAIRS = create_changes_pairs(PARAMETERS_DICT['brightness'])
ROTATION_CHANGES_PAIRS = create_changes_pairs(PARAMETERS_DICT['rotation'])
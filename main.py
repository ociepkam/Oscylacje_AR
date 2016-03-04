__author__ = 'Michal Ociepka'

import random
from enum import Enum
import copy
import yaml

FIGURES = range(16)
ROTATION = [0, 90, 180, 270]
BRIGHTNESS = ['white', 'gray', 'slate']
FRAME = ['thin', 'narrow', 'wide']
PARAMETERS = ['rotation', 'brightness', 'frame']
PARAMETERS_DICT = {'rotation': ROTATION, 'brightness': BRIGHTNESS, 'frame': FRAME}
CHANGES_LVL = [-2, -1, 1, 2]


class Instruction_type (Enum):
    text = "text"
    image = "image"


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


class Matrix:
    def __init__(self, figure_list):
        self.figures_list = figure_list
        self.name = None

    def __str__(self):
        a = self.name
        for x in self.figures_list:
            a += "\n"
            a += x.__str__()
        return a

    def return_figure_list(self):
        parameters = []
        for figure in self.figures_list:
            parameters += [figure.return_parameters()]
        all_informations = {'name': self.name, 'parameters': parameters}
        return all_informations

    def shuffle_matrix(self):
        random.shuffle(self.figures_list)

    def change_figures_b(self, number_of_figures_to_change):
        figures_position = range(len(self.figures_list))
        random.shuffle(figures_position)
        figures_position = figures_position[:number_of_figures_to_change]
        list_of_parameters_to_change = [2]
        for i in range(number_of_figures_to_change - 1):
            list_of_parameters_to_change += [random.choice(range(1, 4))]

        for i in range(number_of_figures_to_change):
            self.figures_list[figures_position[i]].change_parameters(list_of_parameters_to_change[i])

    def change_figures_d1(self, list_of_changes):
        for idx in range(len(self.figures_list)):
            for parameter in list_of_changes[idx]:
                self.figures_list[idx].change_parameter(parameter[0])
        self.name = "D1"

    def change_figures_d2(self, list_of_changes):
        changes_2_or_shorter = [x for x in list_of_changes if 0 < len(x) <= 2]
        figure_parameters = random.choice(changes_2_or_shorter)
        parameter_to_change = random.choice(figure_parameters)

        possible_new_parameters = copy.deepcopy(PARAMETERS)
        for parameter, _ in figure_parameters:
            possible_new_parameters.remove(parameter)

        new_parameter = random.choice(possible_new_parameters)
        change_lvl = random.choice(range(len(PARAMETERS_DICT[new_parameter]) - 1)) + 1

        for idx_f, figure in enumerate(list_of_changes):
            if figure == figure_parameters:
                for idx_p, parameter in enumerate(figure):
                    if parameter == parameter_to_change:
                        figure[idx_p] = [new_parameter, change_lvl]
                        list_of_changes[idx_f] = figure
                        self.change_figures_d1(list_of_changes)
        self.name = "D2"

    def change_figures_d3(self, list_of_changes):
        changes_2_or_1 = [x for x in list_of_changes if len(x) >= 2]
        figure_parameters = random.choice(changes_2_or_1)
        parameter_to_remove = random.choice(figure_parameters)

        for idx_f, figure in enumerate(list_of_changes):
            if figure == figure_parameters:
                for idx_p, parameter in enumerate(figure):
                    if parameter == parameter_to_remove:
                        del figure[idx_p]
                        list_of_changes[idx_f] = figure
                        self.change_figures_d1(list_of_changes)
        self.name = "D3"

    def change_figures_d4(self, list_of_changes):
        changes_2_or_1 = [x for x in list_of_changes if 2 <= len(x) <= 3]
        figure_elements_to_change = random.choice(changes_2_or_1)
        for idx, figure in enumerate(list_of_changes):
            if figure == figure_elements_to_change:
                for name, _ in figure_elements_to_change:
                    self.figures_list[idx].change_parameter(name)
                break
        self.name = "D4"

    def change_figures_d5(self, list_of_changes):
        changes_2_or_1 = [x for x in list_of_changes if 0 < len(x) <= 2]
        figure_elements_to_change = random.choice(changes_2_or_1)
        figure_element_to_change = random.choice(figure_elements_to_change)
        for idx, figure in enumerate(list_of_changes):
            if figure == figure_elements_to_change:
                for name, _ in figure:
                    if name == figure_element_to_change[0]:
                        self.figures_list[idx].change_parameter(name)
                        break
                break

        self.name = "D5"


class Trial:
    def __init__(self, time, per, rel, feedb, wait, exp):
        self.type = 'trial'
        self.time = time
        self.per = per
        self.rel = rel
        self.feedb = feedb
        self.wait = wait
        self.exp = exp
        self.figures_list_len = per[0] * per[1]
        self.figures = FIGURES
        random.shuffle(self.figures)
        self.list_of_changes = []

        self.matrix_list = None
        self.matrix_a = None
        self.matrix_b = None
        self.matrix_c = None
        self.matrix_d1 = None
        self.matrix_d2 = None
        self.matrix_d3 = None
        self.matrix_d4 = None
        self.matrix_d5 = None
        self.matrix_d6 = None

        self.create_all_matrix()

    def create_all_matrix(self):
        self.create_matrix_a()
        self.create_matrix_b()
        self.create_matrix_c()
        self.create_matrix_d6()
        self.create_matrix_d1()
        self.create_matrix_d2()
        self.create_matrix_d3()
        self.create_matrix_d4()
        self.create_matrix_d5()

        self.matrix_list = [self.matrix_d1.return_figure_list(), self.matrix_d2.return_figure_list(),
                            self.matrix_d3.return_figure_list(), self.matrix_d4.return_figure_list(),
                            self.matrix_d5.return_figure_list(), self.matrix_d6.return_figure_list()]
        random.shuffle(self.matrix_list)

    def create_matrix_a(self):
        matrix_frame_changes_pairs = FRAME_CHANGES_PAIRS
        matrix_brightness_changes_pairs = BRIGHTNESS_CHANGES_PAIRS
        matrix_rotation_changes_pairs = ROTATION_CHANGES_PAIRS
        figures_list = []
        for name in self.figures[:self.figures_list_len]:
            figure_frame = random.choice(matrix_frame_changes_pairs)
            matrix_frame_changes_pairs = [x for x in matrix_frame_changes_pairs if x[1] != figure_frame[1]]

            figure_brightness = random.choice(matrix_brightness_changes_pairs)
            matrix_brightness_changes_pairs = [x for x in matrix_brightness_changes_pairs if
                                               x[1] != figure_brightness[1]]

            figure_rotation = random.choice(matrix_rotation_changes_pairs)
            matrix_rotation_changes_pairs = [x for x in matrix_rotation_changes_pairs if x[1] != figure_rotation[1]]

            figures_list += [Figure([name, figure_rotation, figure_brightness, figure_frame])]

        self.figures = self.figures[self.figures_list_len:]
        self.matrix_a = Matrix(figures_list)
        self.matrix_a.name = "A"

    def create_matrix_b(self):
        self.matrix_b = copy.deepcopy(self.matrix_a)
        self.matrix_b.change_figures_b(self.rel)
        self.matrix_b.shuffle_matrix()
        for figure in self.matrix_b.figures_list:
            self.list_of_changes.append(figure.elements_changed)
        random.shuffle(self.list_of_changes)
        self.matrix_b.name = "B"

    def create_matrix_c(self):
        matrix_frame_changes_pairs = FRAME_CHANGES_PAIRS
        matrix_brightness_changes_pairs = BRIGHTNESS_CHANGES_PAIRS
        matrix_rotation_changes_pairs = ROTATION_CHANGES_PAIRS
        figures_list_c = []
        for idx, name in enumerate(self.figures[:self.figures_list_len]):
            a_frame_possible_change = self.matrix_a.figures_list[idx].frame_possible_change
            figure_frame_changes_pairs = [x for x in matrix_frame_changes_pairs if x[1] == a_frame_possible_change]
            c_figure_frame = random.choice(figure_frame_changes_pairs)

            a_brightness_possible_change = self.matrix_a.figures_list[idx].brightness_possible_change
            figure_brightness_changes_pairs = [x for x in matrix_brightness_changes_pairs if
                                               x[1] == a_brightness_possible_change]
            c_figure_brightness = random.choice(figure_brightness_changes_pairs)

            a_rotation_possible_change = self.matrix_a.figures_list[idx].rotation_possible_change
            figure_rotation_changes_pairs = [x for x in matrix_rotation_changes_pairs if
                                             x[1] == a_rotation_possible_change]
            c_figure_rotation = random.choice(figure_rotation_changes_pairs)

            figures_list_c += [Figure([name, c_figure_rotation, c_figure_brightness, c_figure_frame])]

        self.figures = self.figures[self.figures_list_len:]
        self.matrix_c = Matrix(figures_list_c)
        self.matrix_c.name = "C"

    def create_matrix_d1(self):
        self.matrix_d1 = copy.deepcopy(self.matrix_d6)
        self.matrix_d1.change_figures_d1(self.list_of_changes)

    def create_matrix_d2(self):
        self.matrix_d2 = copy.deepcopy(self.matrix_d6)
        list_of_changes = copy.deepcopy(self.list_of_changes)
        self.matrix_d2.change_figures_d2(list_of_changes)

    def create_matrix_d3(self):
        self.matrix_d3 = copy.deepcopy(self.matrix_d6)
        list_of_changes = copy.deepcopy(self.list_of_changes)
        self.matrix_d3.change_figures_d3(list_of_changes)

    def create_matrix_d4(self):
        self.matrix_d4 = copy.deepcopy(self.matrix_d6)
        list_of_changes = copy.deepcopy(self.list_of_changes)
        self.matrix_d4.change_figures_d4(list_of_changes)

    def create_matrix_d5(self):
        self.matrix_d5 = copy.deepcopy(self.matrix_d6)
        list_of_changes = copy.deepcopy(self.list_of_changes)
        self.matrix_d5.change_figures_d5(list_of_changes)

    def create_matrix_d6(self):
        self.matrix_d6 = copy.deepcopy(self.matrix_c)
        self.matrix_d6.name = "D6"
        self.matrix_d6.shuffle_matrix()

    def prepare(self):
        trial_info = {
            "type": self.type,
            "time": self.time,
            "per": self.per,
            "rel": self.rel,
            "feedb": self.feedb,
            "wait": self.wait,
            "exp": self.exp,
            "matrix_info": self.matrix_list
        }
        return trial_info


class Instruction:
    def __init__(self, file_path, instruction_type, time):
        with open(file_path, 'r') as instruction_file:
            self.instruction = yaml.load(instruction_file)
        self.instruction_type = instruction_type
        self.time = time
        self.type = "instruction"

    def prepare(self):
        instruction_info = {
            "type": self.type,
            "time": self.time,
            "instruction_type": self.instruction_type,
            "path": self.instruction
        }
        return instruction_info


class Block:
    def __init__(self, rand, list_of_experiment_elements):
        self.list_of_experiment_elements = list_of_experiment_elements
        self.rand = rand

        if self.rand:
            self.randomize_block()

    def randomize_block(self):
        block_trials = [x for x in self.list_of_experiment_elements if x.type == 'trial']
        experiment_elements_to_randomize = [x for x in block_trials if x.exp]
        random.shuffle(experiment_elements_to_randomize)
        i = 0

        for idx, element in enumerate(self.list_of_experiment_elements):
            if element.type == 'trial':
                if element.exp:
                    self.list_of_experiment_elements[idx] = experiment_elements_to_randomize[i]
                    i += 1

    def prepare(self):
        elements_list = []
        for element in self.list_of_experiment_elements:
            elements_list.append(element.prepare())

        block_info = {
            "rand": self.rand,
            "experiment_elements": elements_list
        }
        return block_info


class Experiment:
    def __init__(self, list_of_blocks, id, sex, age):
        self.name = str(id) + sex + str(age)
        self.list_of_blocks = list_of_blocks

    def prepare(self):
        elements_list = []
        for element in self.list_of_blocks:
            elements_list.append(element.prepare())
        info = {
            "name": self.name,
            "list_of_blocks": elements_list
        }
        return info

    def save(self):
        info = self.prepare()
        with open(self.name + ".yaml", 'w') as save_file:
            save_file.write(yaml.dump(info))


trial = Trial(0, Per.small, 2, 0, 0, 0)
trial2 = Trial(12, Per.small, 2, 1, 5, 1)
instrukcja = Instruction("instrukcja.yaml", Instruction_type.text, 3)
blok = Block(False, [instrukcja, trial, trial2])
eksperyment = Experiment([blok], "as", "K", 25)
print eksperyment.prepare()
eksperyment.save()

# print trial.matrix_a
# print trial.matrix_b
# print trial.matrix_c
# print trial.matrix_d1
# print trial.matrix_d2
# print trial.matrix_d3
# print trial.matrix_d3
# print trial.matrix_d4
# print trial.matrix_d5
# print trial.matrix_d6

#print trial.prepare_trial()




"""
TODO:
wskazowka tekstowa
"""
